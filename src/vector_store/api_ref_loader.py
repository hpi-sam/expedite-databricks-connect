from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from pathlib import Path
import json


def load_documents():
    store_path = Path("/raid/shared/masterproject2024/rag/data/api_reference_new.json")
    with open(store_path, "r") as f:
        data = json.load(f)

    docs = [
        Document(metadata=item["metadata"], page_content=item["page_content"])
        for item in data
    ]

    return docs


def vector_store_from_api_ref(
    vector_store_path: str,
    split_documents: bool,
    chunk_size: int,
    chunk_overlap: int,
    embedding_function,
):

    if os.path.exists(vector_store_path):
        return Chroma(
            persist_directory=str(vector_store_path),
            embedding_function=embedding_function,
        )

    print("Creating vectorstore.")
    data = load_documents()

    if split_documents:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        data = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
        data,
        embedding=embedding_function,
        persist_directory=str(vector_store_path),
    )

    return vectorstore
