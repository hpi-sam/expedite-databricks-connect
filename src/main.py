import datetime
import logging
import os
from pathlib import Path
from typing import Dict, List

from huggingface_hub import login
from openai import OpenAI
from transformers import AutoTokenizer, PreTrainedTokenizerFast

import config
from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.__main__ import lint_codestring
from vector_store.vector_store_factory import VectorStoreFactory

logger = logging.getLogger(__name__)


def log_messages(messages: List[Dict[str, str]]) -> None:
    num_messages = len(messages)
    logger_message = ""
    for i, message in enumerate(messages):
        logger_message += f"""
Message {i + 1}/{num_messages}
{"=" * 100}
Role: {message["role"]}
Content: {message["content"]}
{"=" * 100}
"""
    logger.info(logger_message)


class Assistant:
    model_name: str
    temperature: float
    _client: OpenAI
    _system_message: Dict[str, str]
    _messages: List[Dict[str, str]]
    _tokenizer: PreTrainedTokenizerFast

    def __init__(self, model_temperature: float):
        login(token="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")
        self._client = OpenAI(
            base_url="http://localhost:8000/v1", api_key="token-abc123"
        )
        self._system_message = {
            "role": "system",
            "content": config.SYSTEM_PROMPT,
        }
        self._messages = []
        self.temperature = model_temperature
        self.model_name = config.MODEL_NAME
        self._tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)
        assert (
                self._tokenizer != False
        ), f"somthing went wrong when fetching the default tokenizer for model {config.MODEL_NAME}"

    def _all_messages(self):
        return [self._system_message] + self._messages

    def _tokenized_messages(self):
        return self._tokenizer.apply_chat_template(self._all_messages(), tokenize=True)

    def generate_answer(self, prompt: str) -> str:
        self._messages += [
            {"role": "user", "content": prompt},
        ]
        num_tokens = len(self._tokenized_messages())
        while num_tokens > config.MAX_MODEL_LENGTH - config.ANSWER_TOKEN_LENGTH:
            self._messages.pop(0)
            num_tokens = len(self._tokenized_messages())

        log_messages(self._all_messages())
        completion = self._client.completions.create(
            model=self.model_name,
            max_tokens=config.ANSWER_TOKEN_LENGTH,
            prompt=self._tokenized_messages(),
            temperature=self.temperature,
        )
        answer = completion.choices.pop().text
        self._messages += [
            {
                "role": "assistant",
                "content": answer.replace(
                    "<|start_header_id|>assistant<|end_header_id|>", ""
                ),
            }
        ]
        return answer


def migrate_code(code: str):
    """
    Try to migrate provided code from classic Spark to Spark Connect.

    Args:
        code (str): The input Spark code to be migrated.

    Returns:
        str: The migrated and potentially linted Spark Connect code.
    """
    assistant = Assistant(0.2)
    vectorstore_settings = config.VECTORSTORE_SETTINGS.get(config.VECTORSTORE_TYPE, {})
    vectorstore = VectorStoreFactory.initialize(
        config.VECTORSTORE_TYPE, **vectorstore_settings
    )

    print(f"\nIteration 1")
    print("----------------------------------------------")
    linter_feedback = lint_codestring(code)

    if linter_feedback:
        print("Linting feedback:")
        for str in linter_feedback: print(str)
    else:
        print("DONE: No problems detected by the linter.\n")
        return code

    context = vectorstore.similarity_search(code, k=4)
    prompt = config.INITIAL_PROMPT.format(
        code=code, error=linter_feedback, context=context
    )

    # Generate initial migration suggestion
    code = postprocess(assistant.generate_answer(prompt))

    # Optional iterative improvement process based on config settings
    if config.ITERATE:
        for iteration in range(config.ITERATION_LIMIT):
            print(f"\nIteration {iteration + 1} of {config.ITERATION_LIMIT}")
            print("----------------------------------------------")
            linter_feedback = lint_codestring(code)
            if not linter_feedback:
                print("DONE: No problems detected by the linter.\n")
                break
            print("Linting feedback:")
            for str in linter_feedback: print(str)
            prompt = config.LINTER_ERROR_PROMPT.format(error=linter_feedback)
            code = postprocess(assistant.generate_answer(prompt))

    return code


if __name__ == "__main__":
    """
    Entry point for the script. Evaluates the `migrate_code` function
    to test its performance on pre-defined code samples.
    """
    logging_dir = Path("../logs/")
    logging_file = (
            logging_dir
            / f"{datetime.datetime.now().strftime(format="%Y-%m-%d_%H:%M:%S")}.log"
    )
    os.makedirs(logging_dir, exist_ok=True)
    logging.basicConfig(filename=logging_file, level=logging.INFO)
    logging.Filter()
    evaluate(migrate_code)
