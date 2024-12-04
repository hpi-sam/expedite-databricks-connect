import logging
from ast import literal_eval
from typing import Callable

import pandas as pd
from omegaconf import DictConfig

from .examples_pre_migration.flatMap import flatMapExample
from .examples_pre_migration.frequentWords import frequentWordsExample
from .examples_pre_migration.map import mapExample
from .examples_pre_migration.mapPartitions import mapPartitionsExample
from .examples_pre_migration.mapReduce import mapReduceExample
from .examples_pre_migration.mixedRDD import mixedRDDExample
from .examples_pre_migration.pi import test_python_pi_issue
from .examples_pre_migration.prefixSpan import test_prefix_span_example
from .examples_pre_migration.quinnRddSparkContext import quinn_rdd_spark_Context
from .examples_pre_migration.readJson import readJsonExample
from .examples_pre_migration.readJsonCsv import test_sql_dataframe_reader_api
from .examples_pre_migration.sparkContext import sparkContextExample
from .examples_pre_migration.sparkJvmOrigin import setJVMOrigin
from .examples_pre_migration.sumNumbers import sumNumbers

logger = logging.getLogger(__name__)

examples = [
    ("mixedRDD", mixedRDDExample),
    ("map", mapExample),
    ("mapPartitions", mapPartitionsExample),
    ("flatMap", flatMapExample),
    ("mapReduce", mapReduceExample),
    ("readJson", readJsonExample),
    ("sparkContext", sparkContextExample),
    ("sparkJvmOrigin", setJVMOrigin),
    ("quinnRddSparkContext", quinn_rdd_spark_Context),
    ("frequentWords", frequentWordsExample),
    ("sumNumbers", sumNumbers),
    ("readJsonCsv", test_sql_dataframe_reader_api),
    ("pi", test_python_pi_issue),
    ("prefixSpan", test_prefix_span_example),
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
    if file_name in ["mapPartitions", "readJson"]:
        true_df = pd.read_csv(output_file, index=False)
    else:
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

    if file_name in ["map", "flatMap", "frequentWords", "reduce", "pi", "readJsonCsv"]:
        reformatted_result = pd.DataFrame(result)
    elif file_name in ["mapReduce", "sumNumbers"]:
        reformatted_result = pd.DataFrame([result])
    elif file_name in ["mapPartitions", "readJson"]:
        reformatted_result = result.toPandas()
    elif file_name == "sparkContext":
        reformatted_result = pd.DataFrame(result.items())
    elif file_name == "prefixSpan":
        reformatted_result[0] = result[0].apply(literal_eval)  # make string to list
        reformatted_result = reformatted_result.drop(index=0).reset_index(drop=True)

    return reformatted_result


def generate(
        file_name: str,
        example_function: Callable,
        model_generate: Callable,
        metrics: dict[str, int],
        cfg: DictConfig,
):
    with open(f"evaluation/examples_pre_migration/{file_name}.py", "r") as file:
        code = file.read()

    output = model_generate(code, cfg)

    print(f"----------------- Old code ------------------")
    print(f"{code}")

    print(f"----------------- New code ------------------")
    print(f"{postprocess(output)}")

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


def evaluate(model_generation_function: Callable, cfg: DictConfig):
    metrics = {"score": 0, "invalid_output": 0, "code_error": 0, "different_output": 0}

    for i, (file_name, example_function) in enumerate(examples):
        print("\n")
        print(f"({i + 1}/{len(examples)}) Evaluating {file_name} example")
        print("==============================================")
        metrics = generate(
            file_name, example_function, model_generation_function, metrics, cfg
        )

    print("\nSucces Rate:", metrics["score"], "/", len(examples))
    print(
        "Model output cannot be executed:",
        metrics["invalid_output"],
        "/",
        len(examples),
    )
    print(
        "Generated function throws error: ", metrics["code_error"], "/", len(examples)
    )
    print("Different output: ", metrics["different_output"], "/", len(examples))

    return metrics
