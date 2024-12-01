import ast
from typing import List, Dict
from pylint.checkers import BaseChecker
from pylint.lint.pylinter import PyLinter
from pylint.interfaces import HIGH
from linter.python_linter.matcher import (
    Matcher,
    RDDApiMatcher,
    MapPartitionsMatcher,
    JvmAccessMatcher,
    SparkSqlContextMatcher,
    SetLogLevelMatcher,
    Log4JMatcher,
    CommandContextMatcher,
)

class PythonLinter:
    def __init__(self):
        self.matchers: List[Matcher] = []

    def add_matcher(self, matcher: Matcher):
        """Add a matcher to the linter."""
        self.matchers.append(matcher)

    def lint(self, code: str) -> List[Dict]:
        """Parse code and run all matchers on the AST."""
        tree = ast.parse(code)
        diagnostics = []

        for node in ast.walk(tree):
            for matcher in self.matchers:
                diagnostics.extend(matcher.lint(node))

        return diagnostics



"""
EXPERIMENTAL CODE PLEASE IGNORE CODE BELOW


"""
def register(linter: PyLinter):
    """SPOLER DOES NOT WORK YET IN PRACTICE, Register the custom linter matchers with pylint."""
    custom_linter = PythonLinter()

    # Add custom matchers
    custom_linter.add_matcher(RDDMatcher())
    custom_linter.add_matcher(MapPartitionsMatcher())

    class CustomChecker(BaseChecker):
        """A custom checker to integrate the PythonLinter with pylint."""
        __implements__ = BaseChecker  # Use BaseChecker directly instead of IAstroidChecker

        name = "custom_checker"
        msgs = {
            "W9001": (
                "Usage of '.rdd' is discouraged. Consider using DataFrame APIs instead.",
                "discouraged-rdd",
                "Warns about discouraged usage of .rdd",
            ),
            "W9002": (
                "Usage of 'mapPartitions' is discouraged. Use 'mapInArrow' or Pandas UDFs instead.",
                "discouraged-mapPartitions",
                "Warns about discouraged usage of mapPartitions",
            ),
        }
        priority = HIGH  # Set the priority for this checker

        def __init__(self, linter):
            super().__init__(linter)
            self.custom_linter = custom_linter

        def visit_module(self, node):
            """Process a Python module and report issues."""
            code = node.stream().read()
            diagnostics = self.custom_linter.lint(code)
            for diag in diagnostics:
                message_id = diag.get("message_id")
                if message_id not in self.msgs:
                    # Skip invalid message IDs
                    continue
                self.add_message(
                    message_id,
                    line=diag.get("line", 0),
                    col_offset=diag.get("column", 0),
                )


    # Register the custom checker with pylint
    linter.register_checker(CustomChecker(linter))
