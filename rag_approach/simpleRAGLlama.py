from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import VLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from transformers import pipeline
from doc_loader import vector_store_from_docs, DOCS

EXAMPLE_CODE = """from pyspark.sql import SparkSession

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


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def generate_answer(vectorstore, code):
    context = vectorstore.similarity_search(code, k=4)
    content = f"""
        Use the given context to rewrite the given code to work with spark connect. Just return the rewritten code and nothing else. 

        <context>
        {context}
        </context>

        This is the code that does not work with spark connect:
        
        <code>
        {code}
        </code>
    """
    messages = [
        {
            "role": "system",
            "content": "You are an assistant to help migrating code from using classic spark to using spark connect.",
        },
        {"role": "user", "content": content},
    ]

    model_id = "neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16"
    number_gpus = 8
    max_model_len = 4096

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )

    llm = VLLM(
        model=model_id,
        tensor_parallel_size=number_gpus,
        max_model_len=max_model_len,
        trust_remote_code=True,
    )

    return llm.invoke(prompt)


if __name__ == "__main__":
    login(token="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")
    vectorstore = vector_store_from_docs(DOCS)
    print(generate_answer(vectorstore, EXAMPLE_CODE))
