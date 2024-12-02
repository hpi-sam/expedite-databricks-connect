import os
from groq import Groq
from dotenv import load_dotenv
from run_with_spark_connect import run_example_sc
from evaluate import evaluate

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def groq_example(code: str, example_function):
    successful, error = run_example_sc(example_function)

    if not successful:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please fix this code. Only output the corrected code and no additional explanations.\nCode: {code}\nError: {error}",
                }
            ],
            model="llama3-70b-8192",
            temperature=0.3,
        )
        output = chat_completion.choices[0].message.content

        return output


evaluate(groq_example)
