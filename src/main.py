from huggingface_hub import login
from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.linter import PythonLinter
from openai import OpenAI
from vector_store.doc_loader import DOCS, vector_store_from_docs
import config


def generate_answer(client, prompt):
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
            "content": "You are an assistant to help migrating code from using classic spark to using spark connect.",
        },
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
        messages=messages,
        temperature=0.2,
    )

    return completion.choices[0].message.content


def migrate_code(code: str):
    """
    Try to migrate provided code from classic Spark to Spark Connect.

    Args:
        code (str): The input Spark code to be migrated.

    Returns:
        str: The migrated and potentially linted Spark Connect code.
    """
    login(token="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")
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")
    linter = PythonLinter()
    vectorstore = vector_store_from_docs(DOCS)

    # Lint the code and retrieve relevant context for the migration prompt
    linter_feedback = linter.lint(code)
    context = vectorstore.similarity_search(code, k=4)
    prompt = config.INITIAL_PROMPT.format(
        code=code, error=linter_feedback, context=context
    )

    # Generate initial migration suggestion
    code = postprocess(generate_answer(client, prompt))

    # Optional iterative improvement process based on config settings
    if config.ITERATE:
        for _ in range(config.ITERATION_LIMIT):
            linter_feedback = linter.lint(code)
            if not linter_feedback:
                print("Code is linted successfully")
                break
            prompt = config.ITERATED_PROMPT.format(
                code=code, error=linter_feedback, context=context
            )
            code = postprocess(generate_answer(client, prompt))

    return code


if __name__ == "__main__":
    """
    Entry point for the script. Evaluates the `migrate_code` function
    to test its performance on pre-defined code samples.
    """
    evaluate(migrate_code)
