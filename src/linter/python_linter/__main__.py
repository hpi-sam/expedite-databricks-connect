import sys
import json
import subprocess
import hydra
from linter.python_linter.linter import PythonLinter
from linter.python_linter.spark_connect_matcher import (
    RDDApiMatcher,
    MapPartitionsMatcher,
    JvmAccessMatcher,
    SparkSqlContextMatcher,
    SetLogLevelMatcher,
    Log4JMatcher,
    CommandContextMatcher,
    RddAttributeMatcher,
)
from omegaconf import DictConfig

"""
IMPORTANT

How to call this file from another file:

from python_linter.__main__ import lint_file

# Example usage
file_path = "file_to_lint.py"
results = lint_file(file_path)
print(results)
"""


def filter_diagnostics(diagnostics, lint_config):
    """
    Filters diagnostics to only contain entries with type in config.LINTER_CONFIG["feedback_types"].
    """
    feedback_types = lint_config.feedback_types
    return [diag for diag in diagnostics if diag["type"] in feedback_types]


def format_diagnostics(diagnostics, linter_type):
    """
    Formats a diagnostic object to match the expected output structure.
    """
    formatted_diagnostics = []
    for diag in diagnostics:
        formatted_diagnostics.append(
            {
                "message": diag.get("message", ""),
                "line": diag.get("line", 0),
                "col": diag.get("col", 0),
                "type": diag.get("type", "error"),
                "linter": linter_type,
            }
        )
    return formatted_diagnostics


def annotate_code_with_diagnostics(code, diagnostics):
    """
    Annotates the given code with comments based on the diagnostics provided.

    Parameters:
        code (str): The original code as a string.
        diagnostics (list): A list of diagnostic dictionaries containing:
            - message (str): The diagnostic message.
            - line (int): The line number of the diagnostic (1-based).
            - col (int): The column number of the diagnostic.
            - type (str): The type of diagnostic (e.g., "error").
            - linter (str): The linter name.

    Returns:
        str: The annotated code as a string.
    """
    # Split the code into lines
    code_lines = code.split("\n")

    # Group diagnostics by line number
    diagnostics_by_line = {}
    for diag in diagnostics:
        line = diag["line"] - 2  # Convert to 0-based index
        if line not in diagnostics_by_line:
            diagnostics_by_line[line] = []
        diagnostics_by_line[line].append(diag)

    # Annotate code lines with diagnostics
    annotaded_code = ""
    for i, line in enumerate(code_lines):
        annotaded_code += line + "\n"
        if i in diagnostics_by_line:
            for diag in diagnostics_by_line[i]:
                annotaded_code += (
                    f"# {diag['type'].upper()}({diag['linter']}): {diag['message']}\n"
                )
    return annotaded_code


def print_diagnostics(diagnostics):
    """
    Makes the diagnostics more human-readable.
    """
    print("Linter diagnostics:")
    for diag in diagnostics:
        print(
            f"{diag['linter']} [{diag['type']}]: {diag['message']} (line {diag['line']}, col {diag['col']})"
        )


def run_pylint(code):
    """
    Run pylint on the given code string and return the diagnostics as a list of JSON objects.
    """
    with open("temp_lint_code.py", "w") as temp_file:
        temp_file.write(code)
    try:
        result = subprocess.run(
            ["pylint", "--output-format=json", "temp_lint_code.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        pylint_diagnostics = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        # Handle cases where pylint exits with errors
        pylint_diagnostics = json.loads(e.stdout) if e.stdout else []
    return pylint_diagnostics


def run_spark_connect_linter(code):
    """
    Run the Spark Connect linter on the given code string and return the diagnostics as a list of JSON objects.
    """
    # Instantiate the linter
    linter = PythonLinter()

    # Add matchers to the linter
    linter.add_matcher(RDDApiMatcher())
    linter.add_matcher(MapPartitionsMatcher())
    linter.add_matcher(JvmAccessMatcher())
    linter.add_matcher(SparkSqlContextMatcher())
    linter.add_matcher(SetLogLevelMatcher())
    linter.add_matcher(Log4JMatcher())
    linter.add_matcher(CommandContextMatcher())
    linter.add_matcher(RddAttributeMatcher())

    # Collect diagnostics from custom matchers
    spark_connect_diagnostics = linter.lint(code)

    return spark_connect_diagnostics


def run_mypy(code):
    """
    Run mypy on the given code string and return diagnostics as a list of JSON objects.
    """
    with open("temp_lint_code.py", "w") as temp_file:
        temp_file.write(code)
    try:
        result = subprocess.run(
            ["mypy", "--show-error-codes", "temp_lint_code.py"],
            capture_output=True,
            text=True,
            check=False,
        )
        diagnostics = []
        for line in result.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 4:
                diagnostics.append(
                    {
                        "line": int(parts[1]),
                        "col": int(parts[2]),
                        "message": ":".join(parts[3:]).strip(),
                        "type": "type_error",
                    }
                )
        return diagnostics
    except Exception as e:
        return []


def run_flake8(code):
    """
    Run flake8 on the given code string and return diagnostics as a list of JSON objects.
    """
    with open("temp_lint_code.py", "w") as temp_file:
        temp_file.write(code)
    try:
        result = subprocess.run(
            [
                "flake8",
                "--format=%(row)d:%(col)d:%(code)s:%(text)s",
                "temp_lint_code.py",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        diagnostics = []
        for line in result.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 4:
                diagnostics.append(
                    {
                        "line": int(parts[0]),
                        "col": int(parts[1]),
                        "message": parts[3].strip(),
                        "type": parts[2].strip(),
                    }
                )
        return diagnostics
    except Exception as e:
        return []


def lint_codestring(code, lint_config):
    """
    Lints the given code string and returns the diagnostics as a JSON object.
    """
    diagnostics = []

    if "spark_connect" in lint_config.enabled_linters:
        diagnostics += format_diagnostics(
            run_spark_connect_linter(code), "spark_connect"
        )
    if "pylint" in lint_config.enabled_linters:
        diagnostics += format_diagnostics(run_pylint(code), "pylint")
    if "mypy" in lint_config.enabled_linters:
        diagnostics += format_diagnostics(run_mypy(code), "mypy")
    if "flake8" in lint_config.enabled_linters:
        diagnostics += format_diagnostics(run_flake8(code), "flake8")

    diagnostics = filter_diagnostics(diagnostics, lint_config)
    diagnostics.sort(key=lambda x: (x["line"], x["col"]))

    # for some of the linters a temporary file is created, remove it if it exists
    try:
        subprocess.run(["rm", "temp_lint_code.py"])
    except Exception as e:
        pass

    return diagnostics


# def lint_file(file_path):
#     """
#     Lints the specified file and returns the diagnostics as a JSON object.
#     """
#     try:
#         with open(file_path, "r") as f:
#             code = f.read()
#     except Exception as e:
#         raise FileNotFoundError(f"Error reading file: {e}")

#     output = lint_codestring(code)

#     return output


# def main():
#     """
#     Main function to handle CLI execution.
#     """
#     if len(sys.argv) < 2:
#         print("Usage: python-linter <file>")
#         sys.exit(1)

#     file_path = sys.argv[1]

#     try:
#         diagnostics = lint_file(file_path)
#         # Print the diagnostics as a JSON string
#         print(json.dumps(diagnostics, indent=2))
#     except Exception as e:
#         print(f"Error: {e}")
#         sys.exit(1)

#     # Optionally, save the JSON to a file
#     # with open("lint_results.json", "w") as f:
#     #    json.dump(diagnostics, f, indent=2)

#     return diagnostics


# if __name__ == "__main__":
#     main()
