from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from evaluation.evaluate import evaluate, postprocess, run_example_sc
from linter.python_linter.linter import PythonLinter
from openai import OpenAI

linter = PythonLinter()

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_iterated_prompt(context, original_code, iterated_code, error):
    return f"""
        We wanted to rewrite this code snippet to work with spark connect. 
        The rewritten code should have exactly the same functionality as the original code and should return exactly the same output. 
        This is the original code:
        <code>
        {original_code}
        </code>

        This is your latest attempt to rewrite the code. Double check if the code is correct and adjust it if necessary:

        <code>
        {iterated_code}
        </code>

        When this code is executed, it produces the following error:
        {error}

        In case it is helpful you can use the following context to help you with the task:

        <context>
        {context}
        </context>

        Make sure to only return the rewritten code and nothing else.
    """


def create_initial_prompt(context, original_code, error):
    return f"""

        This is code using classic spark that we want to rewrite to work with spark connect.
        The rewritten code should have exactly the same functionality as the original code and should return exactly the same output.
        This is the original code that does not work with spark connect:

        <code>
        {original_code}
        </code>

        When executed, the code produces the following error:
        {error}


        Use the given context to rewrite the given code to work with spark connect. Just return the rewritten code and nothing else. 

        <context>
        {context}
        </context>

        In case it is helpful you can use the following context to help you with the task:

        <context>
        {context}
        </context>

        Make sure to only return the rewritten code and nothing else.
        
    """


def generate_answer(vectorstore, original_code, iterated_code, error, iteration):
    if iteration == 0:
        context = vectorstore.similarity_search(original_code, k=4)
        content = create_initial_prompt(context, original_code, error)

    else:
        context = vectorstore.similarity_search(iterated_code, k=4)
        content = create_iterated_prompt(context, original_code, iterated_code, error)

    messages = [
        {
            "role": "system",
            "content": "You are an assistant to help migrating code from using classic spark to using spark connect.",
        },
        {"role": "user", "content": content},
    ]

    completion = client.chat.completions.create(
        model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
        messages=messages,
        temperature=0.2,
    )

    return completion.choices[0].message.content


def generate_example(code: str, example_function):
    login(token="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")

    # load documents from different sources:

    loader = WebBaseLoader(
        [
            "https://docs.databricks.com/en/dev-tools/databricks-connect/python/limitations.html",
            "https://docs.databricks.com/en/dev-tools/databricks-connect/index.html#pyspark-dataframe-api-limitations",
            "https://spark.apache.org/docs/latest/spark-connect-overview.html",
        ]
    )

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    model_output = ""
    vectorstore = Chroma.from_documents(all_splits, embedding=hf_embeddings)

    linter_feedback = linter.lint(code)

    iterations = 10
    for i in range(iterations):
        print(f"Iteration {i+1}")
        model_output = postprocess(
            generate_answer(vectorstore, code, model_output, linter_feedback, i)
        )
        # ONLY FOR TESTING
        # model_output = postprocess(code)

        linter_feedback = linter.lint(model_output)
        # check whether linter returns empty json
        if not linter_feedback:
            print("Code is linted successfully")
            break

        print("Code is not linted successfully")
        print("Current code:", model_output)
        print("Current feedback:", linter_feedback)
        print("\n")

    return model_output


evaluate(generate_example)
