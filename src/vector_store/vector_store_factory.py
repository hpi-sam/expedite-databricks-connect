from pathlib import Path
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

# from vector_store.huggingface_embeddings_GPU import HuggingFaceEmbeddings
from openai import OpenAI
from vector_store.code_loader import vector_store_from_repos
from vector_store.doc_loader import vector_store_from_docs
from vector_store.api_ref_loader import vector_store_from_api_ref
from langchain_openai import OpenAIEmbeddings
from transformers import AutoTokenizer
import os


class VectorStoreFactory:
    """
    Factory class to create VectorStores based on a given configuration.

    Supported types:
        - 'docs': Document-based VectorStore.
        - 'code': Code-based VectorStore from GitHub repositories.
        - 'api_ref': VectorStore based on API references.
    """

    @staticmethod
    def initialize(
        vectorstore_type: str, embedding_model_name: str, **kwargs
    ) -> Chroma | None:
        """
        Creates a VectorStore based on the specified type.

        Args:
            vectorstore_type (str): The type of the VectorStore ('docs', 'code', 'api_ref').
            kwargs: Additional arguments for specific VectorStore types.

        Returns:
            Chroma | None: The created VectorStore or None if the type is unknown.
        """

        embedding_function = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            show_progress=True,
            model_kwargs={
                "trust_remote_code": True,
            },
            encode_kwargs={"device": "cpu"},
        )

        if vectorstore_type == "docs":
            docs = kwargs.get("docs", [])
            return vector_store_from_docs(docs, embedding_function)

        elif vectorstore_type == "code":
            vector_store_path = Path(
                kwargs.get("vector_store_path")
            ) / embedding_model_name.replace("/", "_")
            data_path = kwargs.get("data_path")
            from_json = kwargs.get("from_json")
            from_store = kwargs.get("from_vect")

            return vector_store_from_repos(
                data_path, vector_store_path, embedding_function, from_json, from_store
            )

        elif vectorstore_type == "api_ref":
            vector_store_path = Path(kwargs.get("vector_store_path"))
            return vector_store_from_api_ref(vector_store_path, embedding_function)

        else:
            raise ValueError(f"Unknown VectorStore-Type: {vectorstore_type}")
