from langchain_community.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
from pathlib import Path


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


def save_documents():
    urls = get_urls()
    bs4_strainer = SoupStrainer("main")
    loader = WebBaseLoader(urls, bs_kwargs={"parse_only": bs4_strainer})
    data = loader.lazy_load()
    store_path = Path("/raid/shared/masterproject2024/rag/data/api_reference.json")

    with open(store_path, "w") as f:
        serializable_data = [
            {
                "metadata": doc.metadata,
                "page_content": doc.page_content,
            }
            for doc in data
        ]
        json.dump(serializable_data, f, indent=4)
    print(f"Data saved to {str(store_path)}")


if __name__ == "__main__":
    save_documents()
