import re
import os
import json
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from ..linter.python_linter.__main__ import lint_codestring


GITHUB_ACCESS_KEY = os.environ[
    "GITHUB_ACCESS_TOKEN"
]  # go to github developer settings and create token
CODE_DATA_FILE_PATH = os.environ["CODE_DATA_FILE_PATH"]

CONNECT_REPOS_BRANCHS = [
    {"repo": "mrpowers-io/quinn", "branch": "main"},
    {"repo": "joblib/joblib-spark", "branch": "master"},
    {"repo": "debugger24/pyspark-test", "branch": "main"},
    {"repo": "julioasotodv/spark-df-profiling", "branch": "master"},
    {"repo": "Labelbox/labelspark", "branch": "master"},
    {"repo": "lvhuyen/SparkAid", "branch": "master"},
    {"repo": "intel-analytics/BigDL-2.x", "branch": "main"},
    {"repo": "sb-ai-lab/RePlay", "branch": "main"},
    {"repo": "Nike-Inc/spark-expectations", "branch": "main"},
    {"repo": "ing-bank/EntityMatchingModel", "branch": "main"},
    {"repo": "apache/spark", "branch": "master"},
    {"repo": "data-science-on-aws/data-science-on-aws", "branch": "master"},
    {"repo": "awslabs/graphstorm", "branch": "main"},
    {"repo": "ssp-data/data-engineering-devops", "branch": "main"},
    {"repo": "pingcap/tidb-docker-compose", "branch": "master"},
    {"repo": "CrestOfWave/Spark-2.3.1", "branch": "master"},
    {
        "repo": "PacktPublishing/40-Algorithms-Every-Programmer-Should-Know",
        "branch": "master",
    },
    {"repo": "PacktPublishing/Advanced-Elasticsearch-7.0", "branch": "master"},
    {"repo": "Qihoo360/XSQL", "branch": "master"},
    {"repo": "TsinghuaDatabaseGroup/AI4DBCode", "branch": "master"},
    {"repo": "TsinghuaDatabaseGroup/DITA", "branch": "master"},
    {"repo": "amplab/drizzle-spark", "branch": "master"},
    {"repo": "cordon-thiago/airflow-spark", "branch": "main"},
    {"repo": "ibm-research-ireland/sparkoscope", "branch": "master"},
    {"repo": "qubole/spark-on-lambda", "branch": "master"},
    {"repo": "runawayhorse001/LearningApacheSpark", "branch": "master"},
    {"repo": "bhavink/databricks", "branch": "master"},
    {"repo": "h2oai/sparkling-water", "branch": "master"},
    {"repo": "graphframes/graphframes", "branch": "master"},
    {"repo": "emdgroup/foundry-dev-tools", "branch": "main"},
    {"repo": "ashkapsky/BigDatalog", "branch": "master"},
    {"repo": "kiszk/spark-gpu", "branch": "master"},
    {"repo": "tophua/spark1.52", "branch": "master"},
    {"repo": "NJUJYB/runData", "branch": "master"},
    {"repo": "ydataai/ydata-profiling", "branch": "master"},
    {"repo": "FaradayRF/Faraday-Software", "branch": "master"},
    {"repo": "adminho/trading-stock-thailand", "branch": "master"},
    {"repo": "databricks/dbt-databricks", "branch": "main"},
    {"repo": "groda/big_data", "branch": "master"},
    {"repo": "javadev/LeetCode-in-Java", "branch": "main"},
    {"repo": "javadev/LeetCode-in-Kotlin", "branch": "main"},
    {"repo": "GoogleCloudPlatform/dataproc-templates", "branch": "main"},
    {"repo": "ScienceStacks/SciSheets", "branch": "master"},
    {"repo": "mahmoudparsian/big-data-mapreduce-course", "branch": "master"},
    {"repo": "radicalbit/radicalbit-ai-monitoring", "branch": "main"},
    {"repo": "GoogleCloudPlatform/data-analytics-golden-demo", "branch": "main"},
    {"repo": "arthurprevot/yaetos", "branch": "master"},
    {"repo": "G-Research/spark-extension", "branch": "master"},
    {"repo": "dbt-labs/dbt-bigquery", "branch": "main"},
    {"repo": "dbt-labs/dbt-spark", "branch": "main"},
    {"repo": "CJones-Optics/ChiCurate", "branch": "main"},
    {"repo": "ChrisCummins/phd", "branch": "master"},
    {"repo": "Data-drone/ANZ_LLM_Bootcamp", "branch": "master"},
    {"repo": "Drecc/chromium-mojo", "branch": "master"},
    {"repo": "JakeKandell/NBA-Predict", "branch": "master"},
    {"repo": "broadinstitute/gnomad_methods", "branch": "main"},
    {"repo": "delta-io/delta-sharing", "branch": "main"},
    {"repo": "eakmanrq/sqlframe", "branch": "main"},
    {"repo": "evidentlyai/evidently", "branch": "master"},
    {
        "repo": "high-performance-spark/high-performance-spark-examples",
        "branch": "main",
    },
    {"repo": "hogan-tech/leetcode-solution", "branch": "master"},
    {"repo": "holdenk/spark-testing-base", "branch": "master"},
    {"repo": "logicalclocks/hopsworks", "branch": "master"},
    {"repo": "microsoftgraph/dataconnect-solutions", "branch": "master"},
    {"repo": "ovh/ai-training-examples", "branch": "master"},
]


def file_contains_pyspark(file_content: str) -> bool:
    """
    Check if a Python file contains PySpark imports.

    Args:
        file_content (str): The content of the Python file.

    Returns:
        bool: True if the file contains PySpark imports, False otherwise.
    """
    return re.search(r"\bimport pyspark\b|\bfrom pyspark\b", file_content) is not None


def is_connect(code: str) -> bool:
    """
    Checks if the given code has Spark Connect linting errors.

    Args:
        linter (PythonLinter): The linter object to use for linting.
        code (str): The Python code to lint.

    Returns:
        bool: True if there are no linting errors, False otherwise.
    """
    try:
        diagnostics = lint_codestring(code)
    except:
        return False

    return not diagnostics


def crawl_code(repo_branch_list: list[dict]) -> list | None:
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
            for doc in repo_docs:
                if file_contains_pyspark(doc.page_content):
                    docs.append(doc)
        except Exception as e:
            print(f"Failed to load documents from {repo} on branch {branch}: {e}")

    if len(docs) == 0:
        print("No documents updated")
        return

    for doc in docs:
        doc.metadata["source"] = str(doc.metadata["source"])
        if is_connect(doc.page_content):
            doc.metadata["type"] = "connect"
        else:
            doc.metadata["type"] = "deprecated"

    return docs


def save_data_to_file(data):
    """
    Save Document data to files

    Args:
        data: list of langchain Documents
    """
    with open(CODE_DATA_FILE_PATH, "w") as f:
        serializable_data = [
            {
                "metadata": doc.metadata,
                "page_content": doc.page_content,
            }
            for doc in data
        ]
        json.dump(serializable_data, f, indent=4)
    print(f"Data saved to {CODE_DATA_FILE_PATH}")


if __name__ == "__main__":
    code_data = crawl_code(CONNECT_REPOS_BRANCHS)
    save_data_to_file(code_data)
