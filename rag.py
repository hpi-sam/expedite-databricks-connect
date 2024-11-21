from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from spark_examples.evaluate import evaluate
from openai import OpenAI
from spark_examples.evaluate import run_example_sc

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def generate_answer(vectorstore, code, example_function):
    _, error = run_example_sc(example_function)
    print(f"The error is: {error}")
    context = vectorstore.similarity_search(code, k=4)
    content = f"""
        Use the given context to rewrite the given code so that it is compatible with Spark Connect. 
        Currently the code produces this error:
        
        {code}

        This is the error:

        {error}
       
        <context>
        {context}
        </context>
    """
    messages = [
        {
            "role": "system",
            "content": "You are an expert at programming with Python and Spark. You only return code blocks.",
        },
        {"role": "user", "content": content},
    ]
    
   
   
    completion = client.chat.completions.create(
    model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
    messages=messages,
    temperature=0.2
    )

    return completion.choices[0].message.content




def generate_example(code: str, example_function):
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

    vectorstore = Chroma.from_documents(all_splits, embedding=hf_embeddings)

    return generate_answer(vectorstore, code, example_function)


evaluate(generate_example)
