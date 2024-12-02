import sys
import json
from python_linter.linter import PythonLinter
from python_linter.matcher import (
    RDDApiMatcher,
    MapPartitionsMatcher,
    JvmAccessMatcher,
    SparkSqlContextMatcher,
    SetLogLevelMatcher,
    Log4JMatcher,
    CommandContextMatcher,
)

"""
IMPORTANT

How to call this file from another file:

from python_linter.__main__ import lint_file

# Example usage
file_path = "file_to_lint.py"
results = lint_file(file_path)
print(results)
"""


def lint_file(file_path):
    """
    Lints the specified file and returns the diagnostics as a JSON object.
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()
    except Exception as e:
        raise FileNotFoundError(f"Error reading file: {e}")

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

    diagnostics = linter.lint(code)

    # Create a structured JSON response
    output = []
    for diag in diagnostics:
        output.append(
            {
                "line": diag["line"],
                "column": diag["col"],
                "message": diag["message"],
                "severity": "Error",  # Can also use "Error" or "Info"
            }
        )

    return output


def main():
    """
    Main function to handle CLI execution.
    """
    if len(sys.argv) < 2:
        print("Usage: python-linter <file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        diagnostics = lint_file(file_path)
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
