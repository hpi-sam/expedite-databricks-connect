from datetime import datetime
import pprint
from typing import Dict, List

from huggingface_hub import login
from openai import OpenAI
from transformers import AutoTokenizer, PreTrainedTokenizerFast

from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.__main__ import lint_codestring, print_diagnostics
from vector_store.vector_store_factory import VectorStoreFactory
from prompt_generation.main import generate_initial_prompt, generate_iterated_prompt
from llm.assistant import Assistant
import hydra
import wandb
from omegaconf import DictConfig, OmegaConf
import os


def build_prompt(cfg: DictConfig, code: str, diagnostics: list[dict], context: str):
    prompt = cfg.initial_prompt + code
    if cfg.use_error:
        prompt += cfg.linter_prompt + str(diagnostics)
    if cfg.use_rag:
        prompt += cfg.context_prompt + str(context)
    return prompt


def build_iterated_prompt(
    cfg: DictConfig, code: str, diagnostics: list[dict], context: str
) -> str:
    prompt = cfg.iterated_prompt + code
    if cfg.use_error:
        prompt += cfg.linter_prompt + str(diagnostics)
    if cfg.use_rag:
        prompt += cfg.context_prompt + str(context)
    return prompt


def format_messages(messages: List[Dict[str, str]]) -> str:
    formated_messages = []
    for message in messages:
        formated_message = {}
        for key, value in message.items():
            formated_message[key] = pprint.pformat(value)
        formated_messages.append(formated_message)
    return pprint.pformat(formated_messages)


def migrate_code(code: str, cfg: DictConfig) -> str:
    """
    Try to migrate provided code from classic Spark to Spark Connect.

    Args:
        code (str): The input Spark code to be migrated.

    Returns:
        code (str): The migrated and potentially linted Spark Connect code.
        metadata (dict): Metadata about the migration process.
    """
    assistant = Assistant(cfg.model_temperature, cfg)
    vectorstore_settings = cfg.vectorstore_settings.get(cfg.vectorstore_type, {})
    embedding_model_name = cfg.get("embedding_model_name")
    vectorstore = VectorStoreFactory.initialize(
        cfg.vectorstore_type, embedding_model_name, **vectorstore_settings
    )
    metadata = {"iteration": 1}
    print(f"\nIteration 1")
    print("----------------------------------------------")
    linter_diagnostics = lint_codestring(code, cfg.linter_config)

    metadata["prompt"] = ""
    metadata["context"] = ""
    metadata["source"] = ""

    if linter_diagnostics:
        print_diagnostics(linter_diagnostics)
    else:
        print("DONE: No problems detected by the linter.\n")
        return code, metadata

    filter = None
    if "type" in vectorstore_settings:
        if cfg.vectorstore_type == "code":
            filter = {"type": vectorstore_settings["type"]}

    context = vectorstore.similarity_search(code, k=cfg.num_rag_docs, filter=filter)
    links = [c.metadata["source"] for c in context]

    context = [c.page_content for c in context]
    if cfg.generate_prompt:
        prompt = generate_initial_prompt(
            code, linter_diagnostics, context, cfg.model_name
        )
    else:
        prompt = build_prompt(cfg, code, linter_diagnostics, context)

    print(f"Prompt: {prompt}")

    metadata["prompt"] = prompt
    metadata["context"] = context
    metadata["source"] = links

    # Generate initial migration suggestion
    code = postprocess(assistant.generate_answer(prompt, cfg))

    # Optional iterative improvement process based on config settings
    if cfg.iterate:
        for iteration in range(cfg.iteration_limit):
            print(f"\nIteration {iteration + 1} of {cfg.iteration_limit}")
            print("----------------------------------------------")
            metadata["iteration"] = iteration + 1
            metadata["prompt"] = prompt
            metadata["context"] = context
            metadata["source"] = links
            linter_diagnostics = lint_codestring(code, cfg.linter_config)
            if not linter_diagnostics:
                print("DONE: No problems detected by the linter.\n")
                break
            print_diagnostics(linter_diagnostics)

            if not cfg.filter_in_iteration:
                filter = None
            context = vectorstore.similarity_search(
                code, k=cfg.num_rag_docs, filter=filter
            )
            context = [c.page_content for c in context]
            if cfg.generate_prompt:
                prompt = generate_iterated_prompt(
                    code, linter_diagnostics, context, cfg.model_name
                )
            else:
                prompt = build_iterated_prompt(cfg, code, linter_diagnostics, context)
            print(f"Iterated Prompt: {prompt}")
            code = postprocess(assistant.generate_answer(prompt, cfg))
    return code, metadata


def run_experiment(cfg: DictConfig):
    wandb.init(
        project="mp",
        config=OmegaConf.to_container(cfg, resolve=True),
        settings=wandb.Settings(start_method="thread"),
        name=cfg.run_name,
        entity="conrad-halle-university-of-potsdam",
    )
    wandb_table = wandb.Table(
        columns=[
            "iteration",
            "example_name",
            "old_code",
            "new_code",
            "error_type",
            "error_message",
            "source",
            "context",
            "prompt",
        ]
    )
    avg_score = 0
    individual_metrics = {}

    for iteration in range(cfg.eval_iterations):
        metrics = evaluate(migrate_code, cfg, wandb_table, iteration)
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

    wandb.log({"evaluation_table": wandb_table}, commit=False)
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
