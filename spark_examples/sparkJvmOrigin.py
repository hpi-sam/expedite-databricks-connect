from pyspark.sql import SparkSession
from typing import Any, Callable
import functools
import inspect
import os
from pyspark.sql import SparkSession

def setJVMOrigin(spark):
    def _capture_call_site(
        spark_session: "SparkSession"
    ) -> str:
        """
        Capture the call site information including file name, line number, and function name.
        This function updates the thread-local storage from JVM side (PySparkCurrentOrigin)
        with the current call site information when a PySpark API function is called.

        Parameters
        ----------
        spark_session : SparkSession
            Current active Spark session.
        pyspark_origin : py4j.JavaClass
            PySparkCurrentOrigin from current active Spark session.
        fragment : str
            The name of the PySpark API function being captured.

        Notes
        -----
        The call site information is used to enhance error messages with the exact location
        in the user code that led to the error.
        """
        stack = list(reversed(inspect.stack()))
        depth = int(
            spark_session.conf.get("spark.sql.stackTracesInDataFrameContext", '1')  # type: ignore[arg-type]
        )
        selected_frames = stack[:depth]
        call_sites = [
            f"{os.path.relpath(frame.filename)}:{frame.lineno}" for frame in selected_frames
        ]        
        call_sites_str = "\n".join(call_sites)
        return call_sites_str
        




    def _with_origin(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        A decorator to capture and provide the call site information to the server side
        when PySpark API functions are invoked, only handling the non-remote case.
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            origin = None
            spark = SparkSession.getActiveSession()
            if spark is not None and hasattr(func, "__name__"):
                assert spark._jvm is not None
                jvm_pyspark_origin = spark._jvm.org.apache.spark.sql.catalyst.trees.CurrentOrigin
                
                call_sites_str = _capture_call_site(spark)

                fragment_option = spark._jvm.scala.Some.apply(func.__name__)
                call_sites_option = spark._jvm.scala.Some.apply(call_sites_str)
                origin = spark._jvm.org.apache.spark.sql.catalyst.trees.Origin(fragment_option, call_sites_option)                
                jvm_pyspark_origin.set(origin)

                try:
                    return func(*args, **kwargs)
                finally:
                    pass
                    jvm_pyspark_origin.reset()
            else:
                return func(*args, **kwargs)

        return wrapper


    @_with_origin
    def sample_function():
        return "Function executed"

    wrapper = sample_function()
    spark = SparkSession.getActiveSession()
    origin = spark._jvm.org.apache.spark.sql.catalyst.trees.CurrentOrigin.get()
    result_with_session = [(origin.line(), origin.startPosition()), [wrapper]]
    return result_with_session
