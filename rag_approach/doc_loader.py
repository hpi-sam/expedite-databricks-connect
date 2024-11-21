from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def vector_store_from_docs(docs:list[str]) -> Chroma | None:
    loader = WebBaseLoader(docs)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    all_splits = text_splitter.split_documents(data)

    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    vectorstore = Chroma.from_documents(all_splits, embedding=hf_embeddings)

    return vectorstore


DOCS = [
    "https://docs.databricks.com/en/dev-tools/databricks-connect/python/limitations.html",
    "https://docs.databricks.com/en/dev-tools/databricks-connect/index.html#pyspark-dataframe-api-limitations",
    "https://spark.apache.org/docs/latest/spark-connect-overview.html",
]