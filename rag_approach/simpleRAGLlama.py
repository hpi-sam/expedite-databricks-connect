from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
from transformers import pipeline

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_answer(vectorstore, code):
    context =  vectorstore.similarity_search(code, k=4)
    retriever = vectorstore.as_retriever()
    content = """
        Use the given context to rewrite the given code to work with spark connect. Just return the rewritten code and nothing else. 

        <context>
        {context}
        </context>
        This is the code that does not work with spark connect:

        {code}
    """
    messages = [
        {
            "role": "system",
            "content": "You are an assistant to help migrating code from using classic spark to using spark connect.",
        },
        {
            "role": "user",
            "content":  content
        }
    ]

    qa_chain = (
        messages
        | llm_engine_hf.bind(skip_prompt=True)
        | StrOutputParser()
    )

    return qa_chain.invoke()


model_id = "neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16"
number_gpus = 4
max_model_len = 4096

sampling_params = SamplingParams(temperature=0.9, top_p=0.9, max_tokens=256)

tokenizer = AutoTokenizer.from_pretrained(model_id)


llm = LLM(model=model_id, tensor_parallel_size=number_gpus, max_model_len=max_model_len)

pipe = pipeline("text-generation", model=llm, tokenizer=tokenizer, max_new_tokens=100, top_k=50, temperature=0.1)
llm_pipeline_hf = HuggingFacePipeline(pipeline=pipe)

llm_engine_hf = ChatHuggingFace(llm=llm_pipeline_hf)
llm.pipeline.tokenizer.pad_token_id = llm.pipeline.tokenizer.eos_token_id

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

if __name__=="__main__":
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
    print(generate_answer(vectorstore, code))

