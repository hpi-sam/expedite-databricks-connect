import sys
import json
import subprocess
import hydra
from linter.python_linter.linter import PythonLinter
from linter.python_linter.matcher import (
    RDDApiMatcher,
    MapPartitionsMatcher,
    JvmAccessMatcher,
    SparkSqlContextMatcher,
    SetLogLevelMatcher,
    Log4JMatcher,
    CommandContextMatcher,
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


def lint_codestring(code, linter_feedback_types):
    """
    Lints the specified code string and returns the diagnostics as a JSON object.
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

    # Collect diagnostics from custom matchers
    diagnostics = linter.lint(code)

    # Collect diagnostics from pylint
    pylint_diagnostics = run_pylint(code)

    # Filter out "Conventions" from pylint diagnostics
    filtered_pylint_diagnostics = [
        diag
        for diag in pylint_diagnostics
        if diag.get("type", "").lower() in linter_feedback_types
    ]

    # Format pylint diagnostics to match the output structure
    for diag in filtered_pylint_diagnostics:
        diagnostics.append(
            {
                "line": diag.get("line", 0),  # Default to 0 if line key is missing
                "column": diag.get(
                    "column", 0
                ),  # Default to 0 if column key is missing
                "message": diag.get("message", "Unknown issue"),
                "severity": diag.get(
                    "type", "Error"
                ).capitalize(),  # Default to "Error"
            }
        )

    # Create a structured JSON response
    output = []
    for diag in diagnostics:
        output.append(
            {
                "line": diag.get("line", 0),  # Default to 0 if line is missing
                "column": diag.get("column", 0),  # Default to 0 if column is missing
                "message": diag.get("message", "No message provided"),
                "severity": diag.get("severity", "Error"),  # Default to "Error"
            }
        )

    return output


def lint_file(file_path, linter_feedback_types):
    """
    Lints the specified file and returns the diagnostics as a JSON object.
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()
    except Exception as e:
        raise FileNotFoundError(f"Error reading file: {e}")

    output = lint_codestring(code, linter_feedback_types)

    return output


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    """
    Main function to handle CLI execution.
    """
    if len(sys.argv) < 2:
        print("Usage: python-linter <file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        diagnostics = lint_file(file_path, cfg.linter_feedback_types)
        # Print the diagnostics as a JSON string
        print(json.dumps(diagnostics, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Optionally, save the JSON to a file
    # with open("lint_results.json", "w") as f:
    #    json.dump(diagnostics, f, indent=2)

    return diagnostics


if __name__ == "__main__":
    main()
