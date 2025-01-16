import traceback
from .examples_pre_migration.map import mapExample
from .examples_pre_migration.flatMap import flatMapExample
from .examples_pre_migration.mapPartitions import mapPartitionsExample
from .examples_pre_migration.mapReduce import mapReduceExample
from .examples_pre_migration.readJson import readJsonExample
from .examples_pre_migration.sparkContext import sparkContextExample
from .run_with_spark_connect import run_example_sc
from .examples_pre_migration.sparkJvmOrigin import setJVMOrigin
from .examples_pre_migration.quinnRddSparkContext import quinn_rdd_spark_Context
from .examples_pre_migration.frequentWords import frequentWordsExample
from .examples_pre_migration.mixedRDD import mixedRDDExample
from .examples_pre_migration.sumNumbers import sumNumbers
from .examples_pre_migration.readJsonCsv import test_sql_dataframe_reader_api
from .examples_pre_migration.pi import test_python_pi_issue
from .examples_pre_migration.prefixSpan import test_prefix_span_example
import pandas as pd
from ast import literal_eval
import pandas as pd
from typing import Callable
from omegaconf import DictConfig
import wandb


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


def compare(file_name: str, result, return_comparison=False) -> str | bool:
    result_df = result_to_df(file_name, result)

    output_file = f"evaluation/output/{file_name}.csv"
    if file_name in ["mapPartitions", "readJson"]:
        true_df = pd.read_csv(output_file, index_col=None)
    elif file_name in ["readJsonCsv", "mixedRDD", "sparkJvmOrigin"]:
        true_df = pd.read_pickle(f"evaluation/output/{file_name}.pkl")
    else:
        true_df = pd.read_csv(output_file, header=None, index_col=None)
    if result_df.equals(true_df):
        print("Correct result.")
        return True
    else:
        print("False result.")
        print(f"True:\n{true_df}")
        print(f"False:\n{result_df}")
        if return_comparison:
            return f"GT:\n{str(true_df)}\nPredicted:\n{str(result_df)}"
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
    else:
        reformatted_result = pd.DataFrame(result)
    return reformatted_result


def generate(
    file_name: str,
    example_function: Callable,
    model_generate: Callable,
    metrics: dict[str, int],
    cfg: DictConfig,
    wandb_table: wandb.Table = None,
    current_iteration: str = "NOT_SPECIFIED",
):
    with open(f"evaluation/examples_pre_migration/{file_name}.py", "r") as file:
        code = file.read()

    output_code, metadata = model_generate(code, cfg)
    resulting_error_str = ""
    resulting_error_type = "NO ERROR"

    print(f"----------------- Old code ------------------")
    print(f"{code}")

    print(f"----------------- New code ------------------")
    print(f"{postprocess(output_code)}")

    # Execute updated function
    scope = {}
    try:
        exec(postprocess(output_code), scope)

        # Try if code is now compatible with Spark Connect and compare results
        successful, example_result = run_example_sc(scope[example_function.__name__])
        if successful:
            comparison = compare(file_name, example_result, return_comparison=True)
            if comparison != False:
                metrics["score"] += 1
                metrics["individual_metrics"][file_name] = 1
                metrics["iteration_solved"][file_name] = metadata["iteration"]
                metrics["iteration_failed"][file_name] = 0
            else:
                metrics["different_output"] += 1
                metrics["individual_metrics"][file_name] = 0
                metrics["iteration_solved"][file_name] = 0
                metrics["iteration_failed"][file_name] = metadata["iteration"]
                resulting_error_str = "Different output: \n" + comparison
                resulting_error_type = "Different output"
        else:
            print("Error:", example_result)
            resulting_error_type = "Code produces error"
            resulting_error_str = example_result
            metrics["code_error"] += 1
            metrics["individual_metrics"][file_name] = 0
            metrics["iteration_solved"][file_name] = 0
            metrics["iteration_failed"][file_name] = metadata["iteration"]

    except Exception as e:
        resulting_error_type = "Other error"
        resulting_error_str = traceback.format_exc()
        print("Generated code produces error: ", e)
        metrics["invalid_output"] += 1
        metrics["individual_metrics"][file_name] = 0
        metrics["iteration_solved"][file_name] = 0
        metrics["iteration_failed"][file_name] = metadata["iteration"]

    if wandb_table:
        wandb_table.add_data(
            current_iteration,
            file_name,
            code,
            postprocess(output_code),
            resulting_error_type,
            resulting_error_str,
        )
    return metrics


def evaluate(
    model_generation_function: Callable,
    cfg: DictConfig,
    current_iteration: str = "NOT_SPECIFIED",
):
    metrics = {
        "score": 0,
        "invalid_output": 0,
        "code_error": 0,
        "different_output": 0,
        "individual_metrics": {},
        "iteration_solved": {},
        "iteration_failed": {},
    }
    wandb_table = wandb.Table(
        columns=[
            "iteration",
            "example_name",
            "old_code",
            "new_code",
            "error_type",
            "error_message",
        ]
    )
    for i, (file_name, example_function) in enumerate(examples):
        print("\n")
        print(f"({i + 1}/{len(examples)}) Evaluating {file_name} example")
        print("==============================================")
        metrics = generate(
            file_name,
            example_function,
            model_generation_function,
            metrics,
            cfg,
            wandb_table,
            current_iteration,
        )
    wandb.log({"evaluation_table": wandb_table})
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
