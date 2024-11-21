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

def main():
    if len(sys.argv) < 2:
        print("Usage: python-linter <file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

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

    # Output diagnostics (for VSCode compatibility)
    output = []
    for diag in diagnostics:
        output.append({
            "line": diag['line'],
            "column": diag['col'],
            "message": diag['message'],
            "severity": "Error",  # Can also use "Error" or "Info"
        })

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
