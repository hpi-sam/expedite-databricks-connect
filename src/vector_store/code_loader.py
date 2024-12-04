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
from python_linter.__main__ import get_linter
from python_linter.linter import PythonLinter


CODE_DATA_FILE_PATH = os.environ["CODE_DATA_FILE_PATH"]


def vector_store_from_repos():
    """
    Load the saved data from a JSON file and reconstruct documents.

    Args:
        filename (str): The filename to load the data from.

    Returns:
        list: A list of LangChain Document objects.
    """
    with open(CODE_DATA_FILE_PATH, "r") as f:
        data = json.load(f)

    code_docs = [
        Document(metadata=item["metadata"], page_content=item["page_content"])
        for item in data
    ]

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=50
    )

    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    splits = text_splitter.split_documents(code_docs)

    vectorstore = Chroma.from_documents(splits, embedding=hf_embeddings)

    return vectorstore
