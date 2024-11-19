from typing import Iterator, List, Dict
import ast


class Matcher:
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        """
        Analyze a node and yield diagnostics as dictionaries.
        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement 'lint'")
    
class RDDMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Attribute) and node.attr == 'rdd':
            yield {
                "message_id": "W9001",  # Add the message_id here
                "message": "Usage of '.rdd' is discouraged. Consider using DataFrame APIs instead.",
                "line": node.lineno,
                "col": node.col_offset,
            }

class MapPartitionsMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == 'mapPartitions':
                yield {
                    "message_id": "W9002",  # Add the message_id here
                    "message": "Usage of 'mapPartitions' is discouraged. Use 'mapInArrow' or Pandas UDFs instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }
