import os
from groq import Groq
from map import mapExample
from flatMap import flatMapExample
from mapPartitions import mapPartitionsExample
from mapReduce import mapReduceExample
from readJson import readJsonExample
from sparkContext import sparkContextExample
from run_with_spark_connect import run_example_sc
import pandas as pd

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

examples = [
    ("map", mapExample),
    ("mapPartitions", mapPartitionsExample),
    ("flatMap", flatMapExample),
    ("mapReduce", mapReduceExample),
    ("readJson", readJsonExample),
    ("sparkContext", sparkContextExample),
]

score = 0


def generate(file_name: str, example_function):
    with open(f"{file_name}.py", "r") as file:
        code = file.read()
    successful, error = run_example_sc(example_function)
    print(f"Error: {error}\n")
    print(f"Old code: \n{code}")
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

        print(f"New code:\n{output}")

        # Execute updated function
        scope = {}
        try:
            exec(postprocess(output), scope)
        except Exception as e:
            print("Generated code produces error: ", e)
        successful, example_result = run_example_sc(scope[example_function.__name__])
        if successful:
            compare(file_name, example_result)
        else:
            print("Error: ", example_result)


def postprocess(result: str):
    if "```" in result:
        result = result.split("```")[1]
    return result


def compare(file_name, result):
    result_df = result_to_df(file_name, result)

    output_file = f"output/{file_name}.csv"
    true_df = pd.read_csv(output_file, header=None, index_col=None)
    if result_df.equals(true_df):
        print("Correct result.")
        score += 1
    else:
        print("False result.")
        print(f"True:\n{true_df}")
        print(f"False:\n{result_df}")


def result_to_df(file_name, result):
    reformatted_result = result
    try:
        if file_name in ["map", "flatMap"]:
            reformatted_result = pd.DataFrame(result)
        elif file_name == "mapReduce.csv":
            reformatted_result = pd.DataFrame([result])
        elif file_name in ["mapPartitions", "readJson"]:
            reformatted_result = result.toPandas()
        elif file_name == "sparkContext":
            reformatted_result = pd.DataFrame(result.items())
    except:
        reformatted_result = pd.DataFrame([result])
    return reformatted_result


for file_name, example_function in examples:
    generate(file_name, example_function)

print(f"Succes Rate: {score}/6")
