# https://sourcegraph.com/github.com/apache/spark/-/commit/80bba4463eba29a56cdd90642f0681c3710ce87c
from pyspark.sql import SparkSession, DataFrame
from typing import Any, Callable, Dict, Match, TypeVar, Type, Optional, TYPE_CHECKING
import functools
import threading
from pyspark.sql.utils import is_remote
import inspect
import csv

_current_origin = threading.local()


def setThreadOrigin(spark):
    def _capture_call_site(spark_session: "SparkSession", depth: int) -> str:
        """
        Capture the call site information including file name, line number, and function name.
        This function updates the thread-local storage from JVM side (PySparkCurrentOrigin)
        with the current call site information when a PySpark API function is called.

        Parameters
        ----------
        spark_session : SparkSession
            Current active Spark session.

        Notes
        -----
        The call site information is used to enhance error messages with the exact location
        in the user code that led to the error.
        """
        stack = list(reversed(inspect.stack()))
        selected_frames = stack[:depth]
        call_sites = [f"{frame.filename}:{frame.lineno}" for frame in selected_frames]
        call_sites_str = "\n".join(call_sites)

        return call_sites_str

    def current_origin() -> threading.local:
        """Return the thread-local current origin, initializing if necessary."""
        global _current_origin

        if not hasattr(_current_origin, "fragment"):
            _current_origin.fragment = None
        if not hasattr(_current_origin, "call_site"):
            _current_origin.call_site = None
        return _current_origin

    def set_current_origin(fragment: Optional[str], call_site: Optional[str]) -> None:
        """Set the fragment and call_site attributes in _current_origin."""
        global _current_origin
        _current_origin.fragment = fragment
        _current_origin.call_site = call_site

    def toString():
        return f"Origin({current_origin().fragment},{current_origin().call_site})"

    def _with_origin(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        A decorator to capture and provide call site information to the server side
        only for Spark Connect (remote execution).
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from pyspark.sql import SparkSession
            from pyspark.sql.utils import is_remote

            # Check if the execution is in Spark Connect (remote)
            if is_remote():
                spark = SparkSession.getActiveSession()
                if spark is not None and hasattr(func, "__name__"):
                    global current_origin

                    depth = 1
                    set_current_origin(func.__name__, _capture_call_site(spark, depth))
                    try:
                        return func(*args, **kwargs)
                    finally:
                        set_current_origin(None, None)
                else:
                    return func(*args, **kwargs)

        return wrapper

    @_with_origin
    def sample_function():
        return "Function executed"

    wrapper = sample_function()

    result_with_session = [
        (current_origin().fragment, current_origin().call_site),
        [wrapper],
    ]

    return result_with_session
