from huggingface_hub import login
from spark_examples.evaluate import evaluate
from openai import OpenAI
from rag_approach.doc_loader import DOCS, vector_store_from_docs
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
    temperature=0.1
    )

    return completion.choices[0].message.content




def generate_example(code: str, example_function):
    login(token="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")

    vectorstore = vector_store_from_docs(DOCS)

    return generate_answer(vectorstore, code, example_function)


evaluate(generate_example)
