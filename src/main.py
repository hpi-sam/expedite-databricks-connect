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
import re


def build_prompt(cfg: DictConfig, code: str, diagnostics: list[dict], context: str):
    prompt = cfg.first_step_prompt + code
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

    if linter_diagnostics:
        print_diagnostics(linter_diagnostics)
    else:
        print("DONE: No problems detected by the linter.\n")
        return code

    filter = None
    if "type" in vectorstore_settings:
        if cfg.vectorstore_type == "code":
            filter = {"type": vectorstore_settings["type"]}

    context = vectorstore.similarity_search(code, k=cfg.num_rag_docs, filter=filter)
    context = [c.page_content for c in context]
    if cfg.generate_prompt:
        prompt = generate_initial_prompt(
            code, linter_diagnostics, context, cfg.model_name
        )
    else:
        prompt = build_prompt(cfg, code, linter_diagnostics, context)

    print(f"Prompt: {prompt}")

    # Generate initial migration suggestion
    code = postprocess(assistant.generate_answer(prompt, cfg))

    # Optional iterative improvement process based on config settings
    if cfg.iterate:
        for iteration in range(cfg.iteration_limit):
            print(f"\nIteration {iteration + 1} of {cfg.iteration_limit}")
            print("----------------------------------------------")
            metadata["iteration"] = iteration + 1
            linter_diagnostics = lint_codestring(code, cfg.linter_config)
            if not linter_diagnostics:
                print("DONE: No problems detected by the linter.\n")
                break
            print_diagnostics(linter_diagnostics)
            context = vectorstore.similarity_search(code, k=cfg.num_rag_docs)
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


def migrate_code_steps(code: str, cfg: DictConfig) -> str:
    assistant = Assistant(cfg.model_temperature, cfg)
    vectorstore_settings = cfg.vectorstore_settings.get(cfg.vectorstore_type, {})
    embedding_model_name = cfg.get("embedding_model_name")
    vectorstore = VectorStoreFactory.initialize(
        cfg.vectorstore_type, embedding_model_name, **vectorstore_settings
    )
    linter_diagnostics = lint_codestring(code, cfg.linter_config)

    prompt = build_prompt(cfg, code, linter_diagnostics, "")
    solution_explanation = assistant.generate_answer(prompt, cfg)
    print(solution_explanation)

    second_prompt = "Could you now please only output the names of the functions you want to use and their imports as a enumerated list? The format should be '1. function1 2. function2 3. function3'."
    answer = assistant.generate_answer(second_prompt, cfg)
    print(answer)
    functions = postprocess_functions(answer)

    context_query_prefix = "Instruct: Given a function, retrieve the passage from the API reference that describe the function.\nQuery: "

    context = []
    for function in functions:
        print("Function: ", function)
        context_query = context_query_prefix + function
        function_ref = vectorstore.similarity_search(context_query, k=1)
        print("Context: ", function_ref[0].page_content)
        context.extend([c.page_content for c in function_ref])

    # Filter duplicates from list
    context = list(set(context))

    final_prompt = f"""Now please generate the updated code. It should have the exact same functionality as the original code. Only output a code block and no additional information.
This is the original code:
{code}                 

These are the errors:
{str(linter_diagnostics)}
In case you need it you can use these pages from the API reference:
"""

    for c in context:
        final_prompt += f"\n{c}"
    print(final_prompt)

    code = assistant.generate_answer(final_prompt, cfg)
    metadata = {"iteration": 1}

    return code, metadata


def postprocess_functions(llm_output: str) -> list[str]:
    llm_output = llm_output.split("\n")
    llm_output = [
        line.split(r"\d+\.")[-1]
        for line in llm_output
        if bool(re.search(r"\d+\.", line))
    ]
    return llm_output


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
        evaluate(migrate_code_steps, cfg)


if __name__ == "__main__":
    main()
