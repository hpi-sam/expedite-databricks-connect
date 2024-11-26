from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import requests
from bs4 import BeautifulSoup, SoupStrainer


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
    print(links)
    return links


def vector_store_from_api_ref():

    urls = get_urls()
    bs4_strainer = SoupStrainer("main")
    loader = WebBaseLoader(urls, bs_kwargs={"parse_only": bs4_strainer})
    data = loader.lazy_load()

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    # all_splits = text_splitter.split_documents(data)

    model_name = "mixedbread-ai/mxbai-embed-large-v1"
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    vectorstore = Chroma.from_documents(
        data,
        embedding=hf_embeddings,
        persist_directory="/raid/smilla.fox/vector_store_large",
    )

    return vectorstore


vector_store_from_api_ref()
