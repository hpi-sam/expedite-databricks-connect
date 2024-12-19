import pprint
from typing import Dict, List

from huggingface_hub import login
from openai import OpenAI
from transformers import AutoTokenizer, PreTrainedTokenizerFast

from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.__main__ import lint_codestring
from vector_store.vector_store_factory import VectorStoreFactory
import hydra
import wandb
from omegaconf import DictConfig, OmegaConf
import os


def build_prompt(cfg: DictConfig, code: str, error: str, context: str):
    prompt = cfg.initial_prompt + code
    if cfg.use_error:
        prompt += cfg.error_prompt + str(error)
    if cfg.use_rag:
        prompt += cfg.context_prompt + str(context)
    return prompt


def build_linter_error_prompt(prompt, error):
    return prompt + str(error)


def format_messages(messages: List[Dict[str, str]]) -> str:
    formated_messages = []
    for message in messages:
        formated_message = {}
        for key, value in message.items():
            formated_message[key] = pprint.pformat(value)
        formated_messages.append(formated_message)
    return pprint.pformat(formated_messages)


class Assistant:
    model_name: str
    temperature: float
    _client: OpenAI
    _system_message: Dict[str, str]
    _messages: List[Dict[str, str]]
    _tokenizer: PreTrainedTokenizerFast

    def __init__(self, model_temperature: float, cfg: DictConfig):
        login(token="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")
        self._client = OpenAI(base_url=os.getenv("VLLM_BASE_URL"))
        self._system_message = {
            "role": "system",
            "content": cfg.system_prompt,
        }
        self._messages = []
        self.temperature = model_temperature
        self.model_name = cfg.model_name
        self._tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
        assert (
            self._tokenizer != False
        ), f"somthing went wrong when fetching the default tokenizer for model {cfg.model_name}"

    def _all_messages(self):
        return [self._system_message] + self._messages

    def _tokenized_messages(self):
        return self._tokenizer.apply_chat_template(self._all_messages(), tokenize=True)

    def generate_answer(self, prompt: str, cfg: DictConfig) -> str:
        self._messages += [
            {"role": "user", "content": prompt},
        ]
        num_tokens = len(self._tokenized_messages())
        while num_tokens > cfg.max_model_length - cfg.answer_token_length:
            self._messages.pop(0)
            num_tokens = len(self._tokenized_messages())

        # print(
        #     f"calling model with messages: \n {format_messages(self._all_messages())}"
        # )
        completion = self._client.completions.create(
            model=self.model_name,
            max_tokens=cfg.answer_token_length,
            prompt=self._tokenized_messages(),
            temperature=self.temperature,
        )
        answer = completion.choices.pop().text
        self._messages += [
            {
                "role": "assistant",
                "content": answer,
            }
        ]
        return answer


def migrate_code(code: str, cfg: DictConfig):
    """
    Try to migrate provided code from classic Spark to Spark Connect.

    Args:
        code (str): The input Spark code to be migrated.

    Returns:
        str: The migrated and potentially linted Spark Connect code.
    """
    assistant = Assistant(cfg.model_temperature, cfg)
    vectorstore_settings = cfg.vectorstore_settings.get(cfg.vectorstore_type, {})
    embedding_model_name = cfg.get("embedding_model_name")
    vectorstore = VectorStoreFactory.initialize(
        cfg.vectorstore_type, embedding_model_name, **vectorstore_settings
    )

    print(f"\nIteration 1")
    print("----------------------------------------------")
    linter_feedback = lint_codestring(code, cfg.linter_config)

    if linter_feedback:
        print("Linting feedback:")
        for str in linter_feedback:
            print(str)
    else:
        print("DONE: No problems detected by the linter.\n")
        return code

    filter = None
    if "type" in vectorstore_settings:
        if cfg.vectorstore_type == "code":
            filter = {"type": vectorstore_settings["type"]}

    context = vectorstore.similarity_search(code, k=cfg.num_rag_docs, filter=filter)
    context = [c.page_content for c in context]
    prompt = build_prompt(cfg, code, linter_feedback, context)

    # Generate initial migration suggestion
    code = postprocess(assistant.generate_answer(prompt, cfg))

    # Optional iterative improvement process based on config settings
    if cfg.iterate:
        for iteration in range(cfg.iteration_limit):
            print(f"\nIteration {iteration + 1} of {cfg.iteration_limit}")
            print("----------------------------------------------")
            linter_feedback = lint_codestring(code, cfg.linter_config)
            if not linter_feedback:
                print("DONE: No problems detected by the linter.\n")
                break
            print("Linting feedback:")
            for str in linter_feedback:
                print(str)
            prompt = build_linter_error_prompt(cfg.linter_error_prompt, linter_feedback)
            code = postprocess(assistant.generate_answer(prompt, cfg))

    return code


def run_experiment(cfg: DictConfig):

    wandb.init(
        project="mp",
        config=OmegaConf.to_container(cfg, resolve=True),
        settings=wandb.Settings(start_method="thread"),
        name=cfg.run_name,
        entity="conrad-halle-university-of-potsdam",
    )

    avg_score = 0
    individual_metrics = {}

    for iteration in range(cfg.eval_iterations):
        metrics = evaluate(migrate_code, cfg)
        metrics["iteration"] = iteration
        avg_score += metrics["score"]
        for key, value in metrics["individual_metrics"].items():
            if key not in individual_metrics:
                individual_metrics[key] = value
            else:
                individual_metrics[key] += value
        metrics.pop("individual_metrics", None)
        wandb.log(metrics)

    avg_score /= cfg.eval_iterations
    for key, value in individual_metrics.items():
        individual_metrics[key] = value / cfg.eval_iterations

    wandb.log({"avg_individual_metrics": individual_metrics})
    wandb.log({"avg_score": avg_score})


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    """
    Entry point for the script. Evaluates the `migrate_code` function
    to test its performance on pre-defined code samples.
    """
    if cfg.log_results:
        run_experiment(cfg)
    else:
        evaluate(migrate_code, cfg)


if __name__ == "__main__":
    main()
