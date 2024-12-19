from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup, SoupStrainer
import os


def get_urls():
    links = []
    base_urls = [
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.html",
        "https://spark.apache.org/docs/latest/api/python/reference/pyspark.errors.html",
    ]

    for index, base_url in enumerate(base_urls):
        if index <= 2:
            website = base_url + "index.html"
        else:
            website = base_url
            base_url = "https://spark.apache.org/docs/latest/api/python/reference/"

        result = requests.get(website)
        content = result.text
        soup = BeautifulSoup(content, "lxml")

        box = soup.find("div", class_="toctree-wrapper compound")
        if not box:
            box = soup.find("main")
        links.extend([base_url + link["href"] for link in box.find_all("a", href=True)])
    return links


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

    urls = get_urls()
    bs4_strainer = SoupStrainer("main")
    loader = WebBaseLoader(urls, bs_kwargs={"parse_only": bs4_strainer})
    data = loader.lazy_load()

    if split_documents:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        data = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
        data,
        embedding=embedding_function,
        persist_directory=vector_store_path,
    )

    return vectorstore
