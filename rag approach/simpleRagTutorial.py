"""Implementation of the Build a Local RAG Application tutorial from LangChain's documentation. 
(https://python.langchain.com/docs/tutorials/local_rag/)"""

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough
from huggingface_hub import login
import os

import torch

os.environ["HF_HOME"] = (
    "/hpi/fs00/share/fg/friedrich/ubc-ocean/masterProject/huggingface"
)

login(token="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")

# load documents from different sources:

loader = WebBaseLoader(
    [
        "https://docs.databricks.com/en/dev-tools/databricks-connect/python/limitations.html",
        "https://docs.databricks.com/en/dev-tools/databricks-connect/index.html#pyspark-dataframe-api-limitations",
        "https://spark.apache.org/docs/latest/spark-connect-overview.html",
    ]
)

data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

model_name = "mixedbread-ai/mxbai-embed-large-v1"
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
)
print("Model loaded")
vectorstore = Chroma.from_documents(all_splits, embedding=hf_embeddings)

llm = HuggingFacePipeline.from_model_id(
    model_id="meta-llama/Llama-3.2-3B-Instruct",
    task="text-generation",
    model_kwargs={"torch_dtype": torch.bfloat16},
    pipeline_kwargs={
        "max_new_tokens": 1024,
    },
    device_map="auto",
)

llm_engine_hf = ChatHuggingFace(llm=llm)
llm.pipeline.tokenizer.pad_token_id = llm.pipeline.tokenizer.eos_token_id


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


RAG_TEMPLATE = """
You are an assistant to help migrating code from using classic spark to using spark connect. Use the given context to rewrite the given code to work with spark connect. Just return the rewritten code and nothing else. 

<context>
{context}
</context>

This is the code that does not work with spark connect:

{code}"""

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
retriever = vectorstore.as_retriever()
qa_chain = (
    {
        "error": RunnablePassthrough(),
        "context": retriever | format_docs,
        "code": RunnablePassthrough(),
    }
    | rag_prompt
    | llm_engine_hf.bind(skip_prompt=True)
    | StrOutputParser()
)

code = """from pyspark.sql import SparkSession

def flatMapExample(spark):
    data = ["Project Gutenberg’s",
            "Alice’s Adventures in Wonderland",
            "Project Gutenberg’s",
            "Adventures in Wonderland",
            "Project Gutenberg’s"]
    rdd=spark.sparkContext.parallelize(data)
    

    #Flatmap    
    rdd2=rdd.flatMap(lambda x: x.split(" "))
    result = []
    for element in rdd2.collect():
        result.append(element)

    return result"""

docs = vectorstore.similarity_search(code)
print(format_docs(docs))

# Run
# print(qa_chain.invoke(code))
