from typing import Iterator, Dict
from tree_sitter import Node
import ast


class Matcher:

    def lint(self, node) -> Iterator[Dict]:
        """
        Analyze a Tree-Sitter node and yield diagnostics as dictionaries.
        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement 'lint'")


class JvmAccessMatcher(Matcher):
    _FIELDS = [
        "_jvm",
        "_jcol",
        "_jdf",
        "_jspark",
        "_jsparkSession",
    ]

    def lint(self, node) -> Iterator[Dict]:
        # Original AST logic for checking Spark Driver JVM access
        if isinstance(node, ast.Attribute) and node.attr in self._FIELDS:
            yield {
                "message_id": "E9010",
                "message": f"Cannot access Spark Driver JVM field '{node.attr}' in shared clusters.",
                "line": node.lineno,
                "col": node.col_offset,
            }

        # Tree-Sitter logic for checking Spark Driver JVM access
        if isinstance(node, Node) and node.type == "attribute":
            for field in self._FIELDS:
                if field in node.text.decode("utf-8"):
                    yield {
                        "message_id": "E9010",
                        "message": f"Cannot access Spark Driver JVM field '{field}' in shared clusters.",
                        "line": node.start_point[0] + 1,
                        "col": node.start_point[1],
                    }


class RDDApiMatcher(Matcher):
    _SC_METHODS = [
        # RDD creation
        "emptyRDD",
        "parallelize",
        "range",
        "makeRDD",
        # file read methods
        "binaryFiles",
        "binaryRecords",
        "hadoopFile",
        "hadoopRDD",
        "newAPIHadoopFile",
        "newAPIHadoopRDD",
        "objectFile",
        "sequenceFile",
        "textFile",
        "wholeTextFiles",
    ]

    def lint(self, node) -> Iterator[Dict]:
        # Original AST logic for detecting SparkContext methods
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in self._SC_METHODS:
                yield {
                    "message_id": "E9008",
                    "message": f"Usage of SparkContext method '{node.func.attr}' is not allowed. "
                    f"Use DataFrame APIs instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }

        # Tree-Sitter logic: Detecting calls to SparkContext methods
        if isinstance(node, Node) and node.type == "call":
            function_node = node.child_by_field_name("function")
            if function_node:
                func_name = function_node.text.decode("utf-8").split(".")[-1]
                if func_name in self._SC_METHODS:
                    yield {
                        "message_id": "E9008",
                        "message": f"Usage of SparkContext method '{func_name}' is not allowed. "
                        f"Use DataFrame APIs instead.",
                        "line": node.start_point[0] + 1,
                        "col": node.start_point[1],
                    }


class RddAttributeMatcher(Matcher):

    def lint(self, node) -> Iterator[Dict]:
        # Original AST logic for 'rdd' access
        if isinstance(node, ast.Attribute) and node.attr == "rdd":
            yield {
                "message_id": "E9009",
                "message": "Accessing 'rdd' from a DataFrame is not allowed. Use DataFrame APIs instead.",
                "line": node.lineno,
                "col": node.col_offset,
            }

        # Tree-Sitter logic: Checking for '.rdd' attribute in Tree-Sitter nodes
        if isinstance(node, Node) and node.type == "attribute":
            if node.text.decode("utf-8").endswith(".rdd"):
                yield {
                    "message_id": "E9009",
                    "message": "Accessing 'rdd' from a DataFrame is not allowed. Use DataFrame APIs instead.",
                    "line": node.start_point[0] + 1,  # 0-based to 1-based
                    "col": node.start_point[1],
                }


class SparkSqlContextMatcher(Matcher):
    _ATTRIBUTES = ["sc", "sqlContext", "sparkContext"]
    _KNOWN_REPLACEMENTS = {"getConf": "conf", "_conf": "conf"}

    def lint(self, node) -> Iterator[Dict]:
        """
        Analyze the AST or Tree-Sitter node and yield diagnostics for legacy context usage.
        """
        # Handle Python's AST nodes
        if isinstance(node, ast.Attribute):
            # Case: sc.getConf or sqlContext.getConf
            if isinstance(node.value, ast.Name) and node.value.id in self._ATTRIBUTES:
                yield self._get_advice(
                    node, node.value.id, node.attr, node.lineno, node.col_offset
                )

            # Case: df.sparkContext.getConf
            if (
                isinstance(node.value, ast.Attribute)
                and node.value.attr in self._ATTRIBUTES
            ):
                yield self._get_advice(
                    node, node.value.attr, node.attr, node.lineno, node.col_offset
                )

        # Handle Tree-Sitter nodes
        if isinstance(node, Node) and node.type == "attribute":
            # Decode the base and attribute from Tree-Sitter node
            base_node = node.child_by_field_name("object")
            attr_node = node.child_by_field_name("attribute")
            if base_node and attr_node:
                base = base_node.text.decode("utf-8")
                attr = attr_node.text.decode("utf-8")
                if base in self._ATTRIBUTES:
                    yield self._get_advice(
                        node,
                        base,
                        attr,
                        node.start_point[0] + 1,  # Tree-Sitter's 0-based to 1-based
                        node.start_point[1],
                    )

    def _get_advice(self, node, base: str, attr: str, line: int, col: int) -> Dict:
        """
        Generate advice message for prohibited usage.
        """
        if attr in self._KNOWN_REPLACEMENTS:
            replacement = self._KNOWN_REPLACEMENTS[attr]
            return {
                "message_id": "E9011",
                "message": f"'{base}.{attr}' is not supported. Rewrite it using 'spark.{replacement}' instead.",
                "line": line,
                "col": col,
            }
        return {
            "message_id": "E9011",
            "message": f"'{base}' is not supported. Rewrite it using 'spark' instead.",
            "line": line,
            "col": col,
        }


class MapPartitionsMatcher(Matcher):

    def lint(self, node) -> Iterator[Dict]:
        # Original AST logic for detecting 'mapPartitions'
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "mapPartitions":
                yield {
                    "message_id": "E9002",
                    "message": "Usage of 'mapPartitions' is not allowed. Use 'mapInArrow' or Pandas UDFs instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }

        # Tree-Sitter logic: Detecting 'mapPartitions' usage
        if isinstance(node, Node) and node.type == "call":
            function_node = node.child_by_field_name("function")
            if function_node:
                if function_node.text.decode("utf-8").endswith("mapPartitions"):
                    yield {
                        "message_id": "E9002",
                        "message": "Usage of 'mapPartitions' is not allowed. Use 'mapInArrow' or Pandas UDFs instead.",
                        "line": node.start_point[0] + 1,
                        "col": node.start_point[1],
                    }


class SetLogLevelMatcher(Matcher):

    def lint(self, node) -> Iterator[Dict]:
        # Original AST logic for detecting 'setLogLevel'
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "setLogLevel":
                yield {
                    "message_id": "E9004",
                    "message": "Setting Spark log level from code is not allowed. Use Spark configuration instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }

        # Tree-Sitter logic: Detecting 'setLogLevel' usage
        if isinstance(node, Node) and node.type == "call":
            function_node = node.child_by_field_name("function")
            if function_node:
                if function_node.text.decode("utf-8").endswith("setLogLevel"):
                    yield {
                        "message_id": "E9004",
                        "message": "Setting Spark log level from code is not allowed. Use Spark configuration instead.",
                        "line": node.start_point[0] + 1,
                        "col": node.start_point[1],
                    }


class Log4JMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Attribute):
            if node.attr == "org.apache.log4j":
                yield {
                    "message_id": "E9005",
                    "message": "Accessing Log4J logger from Spark JVM is not allowed. "
                    "Use Python logging.getLogger() instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }

        if isinstance(node, Node) and node.type == "attribute":
            if node.text.decode("utf-8") == "org.apache.log4j":
                yield {
                    "message_id": "E9005",
                    "message": "Accessing Log4J logger from Spark JVM is not allowed. "
                    "Use Python logging.getLogger() instead.",
                    "line": node.start_point[0] + 1,  # Tree-Sitter's 0-based to 1-based
                    "col": node.start_point[1],
                }


class CommandContextMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "toJson":
                yield {
                    "message_id": "E9007",
                    "message": "Usage of 'toJson' is not allowed. Use 'toSafeJson' where supported.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }

        if isinstance(node, Node) and node.type == "call":
            # Traverse children to find if it's a `toJson` call
            for child in node.children:
                if child.type == "attribute" and child.text.decode("utf-8") == "toJson":
                    yield {
                        "message_id": "E9007",
                        "message": "Usage of 'toJson' is not allowed. Use 'toSafeJson' where supported.",
                        "line": child.start_point[0]
                        + 1,  # Tree-Sitter's 0-based to 1-based
                        "col": child.start_point[1],
                    }
