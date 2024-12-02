from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from evaluation.evaluate import evaluate, postprocess, run_example_sc
from linter.python_linter.linter import PythonLinter
from openai import OpenAI
from document_store import DOCS, vector_store_from_docs


ITERATED_PROMPT = f"""
        We wanted to rewrite this code snippet to work with spark connect. 
        The rewritten code should have exactly the same functionality as the original code and should return exactly the same output. 
        This is your latest attempt to rewrite the code. Double check if the code is correct and adjust it if necessary:

        <code>
        {{code}}
        </code>

        When this code is executed, it produces the following error:
        {{error}}

        In case it is helpful you can use the following context to help you with the task:

        <context>
        {{context}}
        </context>

        Make sure to only return the rewritten code and nothing else.
    """


INITIAL_PROMPT = f"""

        This is code using classic spark that we want to rewrite to work with spark connect.
        The rewritten code should have exactly the same functionality as the original code and should return exactly the same output.
        This is the original code that does not work with spark connect:

        <code>
        {{code}}
        </code>

        When executed, the code produces the following error:
        {{error}}

        In case it is helpful you can use the following context to help you with the task:

        <context>
        {{context}}
        </context>

        Make sure to only return the rewritten code and nothing else.
    """

def generate_answer(client, prompt):

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
        temperature=0.2
    )

    return completion.choices[0].message.content





def migrate_code(code: str):
    login(token="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")
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")
    linter = PythonLinter()
    vectorstore = vector_store_from_docs(DOCS)

    linter_feedback = linter.lint(client, code)
    context=vectorstore.similarity_search(code, k=4)
    prompt = INITIAL_PROMPT.format(code=code, error=linter_feedback, context=context)
    code = postprocess(generate_answer(prompt))

    iterations = 5
    for i in range(iterations):
        linter_feedback = linter.lint(code)
        if not linter_feedback:
            print("Code is linted successfully")
            break
        prompt = ITERATED_PROMPT.format(code=code, error=linter_feedback, context=context)
        code = postprocess(generate_answer(client, prompt))
    return code


evaluate(migrate_code)
