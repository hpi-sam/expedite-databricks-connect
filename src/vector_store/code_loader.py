import re
import json
import os
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain.schema import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CODE_DATA_FILE_PATH = os.environ["CODE_DATA_FILE_PATH"]


def load_data_from_file():
    with open(CODE_DATA_FILE_PATH, "r") as f:
        data = json.load(f)

    code_docs = [
        Document(metadata=item["metadata"], page_content=item["page_content"])
        for item in data
    ]

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000
    )

    splits = text_splitter.split_documents(code_docs)[:5000]

    return splits


def vector_store_from_repos(
    data_path: str,
    vector_store_path: str,
    from_json: bool = False,
    from_store: bool = True,
):
    """
    Load the saved data from a JSON file and reconstruct documents.

    Args:
        filename (str): The filename to load the data from.

    Returns:
        list: A list of LangChain Document objects.
    """
    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    if os.path.exists(vector_store_path):
        return Chroma(
            persist_directory=vector_store_path,
            embedding_function=hf_embeddings,
        )

    splits = load_data_from_file()

    vectorstore = Chroma.from_documents(
        splits,
        embedding=hf_embeddings,
        persist_directory="/raid/shared/masterproject2024/vector_stores/code_vector_store_small",
    )

    return vectorstore
