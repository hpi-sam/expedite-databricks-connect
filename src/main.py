from huggingface_hub import login
from openai import OpenAI
from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.__main__ import lint_codestring
from vector_store.vector_store_factory import VectorStoreFactory
import wandb
import hydra
from omegaconf import DictConfig, OmegaConf


def build_prompt(cfg: DictConfig, code: str, error: str, context: str, iterate: bool):
    if iterate:
        prompt = cfg.iterated_prompt + code
    else:
        prompt = cfg.initial_prompt + code
    if cfg.use_error:
        prompt += cfg.error_prompt + str(error)
    if cfg.use_rag:
        prompt += cfg.context_prompt + str(context)
    return prompt


def generate_answer(cfg: DictConfig, client, prompt: str) -> str:
    """
    Generates a response from the AI model based on the given prompt.

    Args:
        client: The OpenAI client used to call the AI model.
        prompt (str): The prompt to provide to the AI for generating a response.

    Returns:
        str: The generated response from the AI model.
    """
    messages = [
        {
            "role": "system",
            "content": cfg.system_prompt,
        },
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model=cfg.model_name,
        messages=messages,
        temperature=cfg.model_temperature,
    )

    return completion.choices[0].message.content


def migrate_code(code: str, cfg: DictConfig):
    """
    Try to migrate provided code from classic Spark to Spark Connect.

    Args:
        code (str): The input Spark code to be migrated.

    Returns:
        str: The migrated and potentially linted Spark Connect code.
    """
    login(token="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")
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")
    vectorstore_settings = cfg.vectorstore_setting.get(cfg.vectorstore_type, {})
    vectorstore = VectorStoreFactory.initialize(
        cfg.vectorstore_type, **vectorstore_settings
    )

    print(f"Iteration 1")
    print("----------------------------------------------")
    linter_feedback = lint_codestring(code, cfg.linter_feedback_types)

    if linter_feedback:
        print(f"Linting feedback: {linter_feedback}\n")
    else:
        print("DONE: No problems detected by the linter.\n")
        return code

    context = vectorstore.similarity_search(code, k=cfg.num_rag_docs)
    prompt = build_prompt(cfg, code, linter_feedback, context, False)

    # Generate initial migration suggestion
    code = postprocess(generate_answer(cfg, client, prompt))

    # Optional iterative improvement process based on config settings
    if cfg.iterate:
        for iteration in range(cfg.iteration_limit - 1):
            print(f"Iteration {iteration + 2} of {cfg.iteration_limit}")
            print("----------------------------------------------")
            linter_feedback = lint_codestring(code, cfg.linter_feedback_types)
            if not linter_feedback:
                print("DONE: No problems detected by the linter.\n")
                break
            print(f"Linting feedback: {linter_feedback}\n")
            prompt = build_prompt(cfg, code, linter_feedback, context, True)
            code = postprocess(generate_answer(cfg, client, prompt))

    return code


def run_experiment(cfg: DictConfig):

    wandb.init(
        project="mp",
        config=OmegaConf.to_container(cfg, resolve=True),
        settings=wandb.Settings(start_method="thread"),
        name=cfg.run_name,
    )

    avg_score = 0

    for iteration in range(cfg.eval_iterations):
        metrics = evaluate(migrate_code, cfg)
        metrics["iteration"] = iteration
        wandb.log(metrics)
        avg_score += metrics["score"]

    avg_score /= cfg.eval_iterations

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
