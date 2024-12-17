from typing import Iterator, List, Dict
import ast


class Matcher:
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        """
        Analyze a node and yield diagnostics as dictionaries.
        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement 'lint'")

class RddAttributeMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Attribute) and node.attr == "rdd":
            yield {
                "message_id": "E9009",
                "message": "Accessing 'rdd' from a DataFrame is not allowed. Use DataFrame APIs instead.",
                "line": node.lineno,
                "col": node.col_offset,
            }

class JvmAccessMatcher(Matcher):
    _FIELDS = [
        "_jvm",
        "_jcol",
        "_jdf",
        "_jspark",
        "_jsparkSession",
    ]

    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Attribute) and node.attr in self._FIELDS:
            yield {
                "message_id": "E9010",
                "message": f"Cannot access Spark Driver JVM field '{node.attr}' in shared clusters.",
                "line": node.lineno,
                "col": node.col_offset,
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

    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in self._SC_METHODS:
                yield {
                    "message_id": "E9008",
                    "message": f"Usage of SparkContext method '{node.func.attr}' is not allowed. "
                    f"Use DataFrame APIs instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }


class SparkSqlContextMatcher(Matcher):
    _ATTRIBUTES = ["sc", "sqlContext", "sparkContext"]
    _KNOWN_REPLACEMENTS = {"getConf": "conf", "_conf": "conf"}

    def lint(self, node: ast.AST) -> Iterator[Dict]:
        """
        Analyze the AST node and yield diagnostics for legacy context usage.
        """
        # Check for direct usage of `sc`, `sqlContext`, or `sparkContext`
        if isinstance(node, ast.Attribute):
            # Case: sc.getConf or sqlContext.getConf
            if isinstance(node.value, ast.Name) and node.value.id in self._ATTRIBUTES:
                yield self._get_advice(node, node.value.id, node.attr)

            # Case: df.sparkContext.getConf
            if (
                isinstance(node.value, ast.Attribute)
                and node.value.attr in self._ATTRIBUTES
            ):
                yield self._get_advice(node, node.value.attr, node.attr)

    def _get_advice(self, node: ast.Attribute, base: str, attr: str) -> Dict:
        """
        Generate advice message for prohibited usage.
        """
        if attr in self._KNOWN_REPLACEMENTS:
            replacement = self._KNOWN_REPLACEMENTS[attr]
            return {
                "message_id": "E9011",
                "message": f"'{base}.{attr}' is not supported. Rewrite it using 'spark.{replacement}' instead.",
                "line": node.lineno,
                "col": node.col_offset,
            }
        return {
            "message_id": "E9011",
            "message": f"'{base}' is not supported. Rewrite it using 'spark' instead.",
            "line": node.lineno,
            "col": node.col_offset,
        }


class MapPartitionsMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "mapPartitions":
                yield {
                    "message_id": "E9002",
                    "message": "Usage of 'mapPartitions' is not allowed. Use 'mapInArrow' or Pandas UDFs instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
                }


class SetLogLevelMatcher(Matcher):
    def lint(self, node: ast.AST) -> Iterator[Dict]:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "setLogLevel":
                yield {
                    "message_id": "E9004",
                    "message": "Setting Spark log level from code is not allowed. "
                    "Use Spark configuration instead.",
                    "line": node.lineno,
                    "col": node.col_offset,
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
