from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from spark_examples.evaluate import evaluate
from openai import OpenAI
from spark_examples.evaluate import run_example_sc
import wandb
from typing import Callable
import argparse


client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")

config = {
    "system_prompt": """You will be provided with PySpark Code that is not compatible with Spark Connect.
                        You will return an updated version of the code that has exactly the same output but is Spark Connect compatible.
                        Only return code blocks.""",
    "use_rag": True,
    "rag_store": "/raid/smilla.fox/vector_store_large",
    "number_of_examples": 9,
    "rag_num_docs": 1,
    "num_runs": 5,
}


def build_prompt(code: str, error: str, vectorstore: Chroma) -> list[dict[str, str]]:
    context_prompt = ""
    error_prompt = ""
    if config["use_rag"]:
        context = vectorstore.similarity_search(code, k=config["rag_num_docs"])

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
    avg_score = 0

    for _ in range(config["num_runs"]):
        metrics = evaluate(generate_example)
        wandb.log(metrics)
        avg_score += metrics["score"]

    avg_score /= config["num_runs"]

    wandb.log({"avg_score": avg_score})


def main():
    parser = argparse.ArgumentParser("Run RAG experiment.")
    parser.add_argument(
        "--no_rag",
        help="Should additional context information be used in the prompt?",
        action="store_false",
    )
    parser.add_argument(
        "--rag_store",
        help="Path to vector store.",
        nargs="?",
        default="/raid/smilla.fox/vector_store_large",
    )
    parser.add_argument(
        "--rag_num_docs",
        help="Number of documents to retrieve from the vector store.",
        type=int,
        default=1,
    )
    parser.add_argument("--run_name", help="Name of the wandb run.", nargs="?")

    args = parser.parse_args()
    print(args)
    config["use_rag"] = args.no_rag
    config["rag_store"] = args.rag_store
    config["rag_num_docs"] = args.rag_num_docs

    wandb.init(
        project="mp",
        config=config,
        settings=wandb.Settings(start_method="thread"),
        name=args.run_name,
    )

    run_experiment()


if __name__ == "__main__":
    main()
