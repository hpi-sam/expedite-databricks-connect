import re
import os
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


GITHUB_ACCESS_KEY = os.environ[
    "GITHUB_ACCESS_TOKEN"
]  # go to github developer settings and create token


def vector_store_from_repos(repo_branch_list: list[dict]) -> Chroma | None:
    """
    Create a Chroma vector store from a list of GitHub repositories and branches.

    Args:
        repo_branch_list (list[dict]): A list of dictionaries, each with "repo" and "branch" keys.
    """
    docs = []

    for entry in repo_branch_list:
        repo = entry.get("repo")
        branch = entry.get("branch")
        doc_relative_path = entry.get("docstring") or ""

        if not repo or not branch:
            print(f"Invalid entry: {entry}")
            continue

        def file_filter(file_path):
            # Filter files based on the current `docstring`
            return (
                re.match(f".*{re.escape(doc_relative_path)}.*\\.py$", file_path)
                is not None
            )

        loader = GithubFileLoader(
            repo=repo,
            branch=branch,
            access_token=GITHUB_ACCESS_KEY,
            github_api_url="https://api.github.com",
            file_filter=file_filter,
        )

        try:
            repo_docs = loader.load()
            docs.extend(repo_docs)
        except Exception as e:
            print(f"Failed to load documents from {repo} on branch {branch}: {e}")

    if len(docs) == 0:
        print("No documents updated")
        return

    for doc in docs:
        doc.metadata["source"] = str(doc.metadata["source"])

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=50
    )

    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(splits, embedding=hf_embeddings)

    return vectorstore
