from huggingface_hub import login
from openai import OpenAI
from evaluation.evaluate import evaluate, postprocess
from linter.python_linter.__main__ import lint_codestring, print_linter_diagnostics
from vector_store.vector_store_factory import VectorStoreFactory
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
        model=config.MODEL_NAME,
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
    vectorstore_settings = config.VECTORSTORE_SETTINGS.get(config.VECTORSTORE_TYPE, {})
    vectorstore = VectorStoreFactory.initialize(
        config.VECTORSTORE_TYPE, **vectorstore_settings
    )

    print(f"Iteration 1")
    print("----------------------------------------------")
    linter_feedback = lint_codestring(code)

    if linter_feedback:
        print_linter_diagnostics(linter_feedback)
    else:
        print("DONE: No problems detected by the linter.\n")
        return code

    context = vectorstore.similarity_search(code, k=4)
    prompt = config.INITIAL_PROMPT.format(
        code=code, error=linter_feedback, context=context
    )

    # Generate initial migration suggestion
    code = postprocess(generate_answer(client, prompt))

    # Optional iterative improvement process based on config settings
    if config.ITERATE:
        for iteration in range(config.ITERATION_LIMIT - 1):
            print(f"Iteration {iteration + 2} of {config.ITERATION_LIMIT}")
            print("----------------------------------------------")
            linter_feedback = lint_codestring(code)
            if not linter_feedback:
                print("DONE: No problems detected by the linter.\n")
                break
            print_linter_diagnostics(linter_feedback)
            print("\n")
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
