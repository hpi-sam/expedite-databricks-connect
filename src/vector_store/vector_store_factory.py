from langchain_chroma import Chroma
from vector_store.code_loader import vector_store_from_repos
from vector_store.doc_loader import vector_store_from_docs
from vector_store.api_ref_loader import vector_store_from_api_ref


class VectorStoreFactory:
    """
    Factory class to create VectorStores based on a given configuration.

    Supported types:
        - 'docs': Document-based VectorStore.
        - 'code': Code-based VectorStore from GitHub repositories.
        - 'api_ref': VectorStore based on API references.
    """

    @staticmethod
    def initialize(vectorstore_type: str, **kwargs) -> Chroma | None:
        """
        Creates a VectorStore based on the specified type.

        Args:
            vectorstore_type (str): The type of the VectorStore ('docs', 'code', 'api_ref').
            kwargs: Additional arguments for specific VectorStore types.

        Returns:
            Chroma | None: The created VectorStore or None if the type is unknown.
        """
        if vectorstore_type == "docs":
            docs = kwargs.get("docs", [])
            return vector_store_from_docs(docs)

        elif vectorstore_type == "code":
            repo_branch_list = kwargs.get("repo_branch_list", [])
            return vector_store_from_repos()

        elif vectorstore_type == "api_ref":
            vector_store_path = kwargs.get("vector_store_path")
            return vector_store_from_api_ref(vector_store_path)

        else:
            raise ValueError(f"Unknown VectorStore-Type: {vectorstore_type}")
