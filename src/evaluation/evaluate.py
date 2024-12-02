from .map import mapExample
from .flatMap import flatMapExample
from .mapPartitions import mapPartitionsExample
from .mapReduce import mapReduceExample
from .readJson import readJsonExample
from .sparkContext import sparkContextExample
from .run_with_spark_connect import run_example_sc
from .sparkJvmOrigin import setJVMOrigin
from .quinnRddSparkContext import quinn_rdd_spark_Context
from .frequentWords import frequentWordsExample
import pandas as pd
from typing import Callable


examples = [
    ("map", mapExample),
    ("mapPartitions", mapPartitionsExample),
    ("flatMap", flatMapExample),
    ("mapReduce", mapReduceExample),
    ("readJson", readJsonExample),
    ("sparkContext", sparkContextExample),
    ("sparkJvmOrigin", setJVMOrigin),
    ("quinnRddSparkContext", quinn_rdd_spark_Context),
    ("frequentWords", frequentWordsExample),
]


def postprocess(result: str):
    if "```" in result:
        result = result.split("```")[1]
        if result and result.startswith("python"):
            result = result[6:]
    return result


def compare(file_name: str, result) -> bool:
    result_df = result_to_df(file_name, result)

    output_file = f"evaluation/output/{file_name}.csv"
    true_df = pd.read_csv(output_file, header=None, index_col=None)
    if result_df.equals(true_df):
        print("Correct result.")
        return True
    else:
        print("False result.")
        print(f"True:\n{true_df}")
        print(f"False:\n{result_df}")
        return False


def result_to_df(file_name: str, result: pd.DataFrame):
    # This is necessary because the outputs of the example functions needed to be formatted differently before saving them to a csv
    reformatted_result = result

    if file_name in ["map", "flatMap", "frequentWords"]:
        reformatted_result = pd.DataFrame(result)
    elif file_name == "mapReduce":
        reformatted_result = pd.DataFrame([result])
    elif file_name in ["mapPartitions", "readJson"]:
        reformatted_result = result.toPandas()
    elif file_name == "sparkContext":
        reformatted_result = pd.DataFrame(result.items())

    return reformatted_result


def generate(
    file_name: str,
    example_function: Callable,
    model_generate: Callable,
    metrics: dict[str, int],
):
    with open(f"evaluation/{file_name}.py", "r") as file:
        code = file.read()

    print(f"Old code: \n{code}")

    output = model_generate(code, example_function)

    print(f"New code:\n{postprocess(output)}")

    # Execute updated function
    scope = {}
    try:
        exec(postprocess(output), scope)

        # Try if code is now compatible with Spark Connect and compare results
        successful, example_result = run_example_sc(scope[example_function.__name__])
        if successful:
            if compare(file_name, example_result):
                metrics["score"] += 1
            else:
                metrics["different_output"] += 1
        else:
            print("Error:", example_result)
            metrics["code_error"] += 1

    except Exception as e:
        print("Generated code produces error: ", e)
        metrics["invalid_output"] += 1
    return metrics


def evaluate(model_generation_function: Callable):
    metrics = {"score": 0, "invalid_output": 0, "code_error": 0, "different_output": 0}

    for file_name, example_function in examples:
        metrics = generate(
            file_name, example_function, model_generation_function, metrics
        )

    print("\nSucces Rate:", metrics["score"], "/9")
    print("Model output cannot be executed:", metrics["invalid_output"], "/9")
    print("Generated function throws error: ", metrics["code_error"], "/9")
    print("Different output: ", metrics["different_output"], "/9")
