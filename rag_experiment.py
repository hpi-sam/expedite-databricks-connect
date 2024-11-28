from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from spark_examples.evaluate import evaluate
from openai import OpenAI
from spark_examples.evaluate import run_example_sc
import wandb
from typing import Callable


client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")

config = {
    "system_prompt": "You are an expert at programming with Python and Spark. You only return code blocks.",
    "use_rag": True,
    "rag_store": "vector_store_large",
    "number_of_examples": 9,
}


def build_prompt(code: str, error: str, vectorstore: Chroma) -> list[dict[str, str]]:
    context_prompt = ""
    error_prompt = ""
    if config["use_rag"]:
        context = vectorstore.similarity_search(code, k=4)
        context_prompt = f"""
        Here is some context information: 

        {context}
        """

    if error:
        error_prompt = f"""
        This is the error my code produces:
        {error}
        """

    content = f"""
        Rewrite the given code so that it is compatible with Spark Connect. 
        {error_prompt}

        This is my code:
        
        {code}

        {context_prompt}
    """

    wandb.log({"user_prompt:": content})

    messages = [
        {
            "role": "system",
            "content": config["system_prompt"],
        },
        {"role": "user", "content": content},
    ]

    return messages


def generate_example(code: str, example_function: Callable):
    login(token="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")
    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    # Initialize vector Store
    vectorstore = Chroma(
        persist_directory=config["rag_store"],
        embedding_function=hf_embeddings,
    )

    # Get error
    _, error = run_example_sc(example_function)
    print(f"The error is: {error}")

    # Build Prompt
    messages = build_prompt(code, error, vectorstore)

    # Generate answer
    completion = client.chat.completions.create(
        model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
        messages=messages,
        temperature=0.2,
    )

    return completion.choices[0].message.content


def run_experiment():
    wandb.init(
        project="mp", config=config, settings=wandb.Settings(start_method="thread")
    )

    metrics = evaluate(generate_example)
    wandb.log(metrics)


if __name__ == "__main__":
    run_experiment()
