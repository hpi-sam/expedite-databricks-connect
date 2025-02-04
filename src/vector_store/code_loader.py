from pathlib import Path
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
from linter.python_linter.__main__ import lint_codestring


CODE_DATA_FILE_PATH = os.environ["CODE_DATA_FILE_PATH"]


class LinterConfig:
    enabled_linters = ["spark_connect"]
    feedback_types = ["error"]


def is_connect(code: str) -> bool:
    """
    Checks if the given code has Spark Connect linting errors.

    Args:
        linter (PythonLinter): The linter object to use for linting.
        code (str): The Python code to lint.

    Returns:
        bool: True if there are no linting errors, False otherwise.
    """
    diagnostics = lint_codestring(code, LinterConfig())
    if diagnostics:
        print("hii", diagnostics)

    # return False

    return not diagnostics


def load_data_from_file(chunk_size=1000):
    with open(CODE_DATA_FILE_PATH, "r") as f:
        data = json.load(f)

    code_docs = [
        Document(metadata=item["metadata"], page_content=item["page_content"])
        for item in data
    ]

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=50
    )

    splits = text_splitter.split_documents(code_docs)

    count_dep = 0
    count_connect = 0

    for split in splits:
        if is_connect(split.page_content):
            split.metadata["type"] = "connect"
            count_connect += 1
        else:
            split.metadata["type"] = "deprecated"
            count_dep += 1

    print("there are connect", count_connect, "and not connect", count_dep)

    return splits


def vector_store_from_repos(
    data_path: str,
    vector_store_path: str | Path,
    embedding_function: HuggingFaceEmbeddings,
    from_json: bool = False,
    from_store: bool = True,
    chunk_size: int = 1000,
):
    """
    Load the saved data from a JSON file and reconstruct documents.

    Args:
        filename (str): The filename to load the data from.

    Returns:
        list: A list of LangChain Document objects.
    """

    if os.path.exists(vector_store_path):
        return Chroma(
            persist_directory=str(vector_store_path),
            embedding_function=embedding_function,
        )

    splits = load_data_from_file(chunk_size=chunk_size)

    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory=str(vector_store_path),
    )

    batch_size = 41666  # Maximum allowed batch size

    # Add documents in smaller batches using a simple for loop
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i + batch_size]  # Slice the list into batches
        vectorstore.add_documents(batch)

    return vectorstore
