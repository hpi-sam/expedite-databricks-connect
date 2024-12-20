from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def vector_store_from_docs(
    docs: list[str], embedding_function: OpenAIEmbeddings
) -> Chroma | None:
    loader = WebBaseLoader(docs)

    data = loader.load()

    for doc in data:
        doc.metadata["type"] = "documentation"

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(all_splits, embedding=embedding_function)

    return vectorstore
