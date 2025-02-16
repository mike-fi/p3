import logging
from contextlib import contextmanager
import pytest
from pyspark.sql.types import StructType
from p3.generator import Generator
from typing import Callable

logger = logging.getLogger(__name__)


@contextmanager
def can_execute():
    try:
        yield
    except Exception as e:
        raise pytest.fail(f"Wasn't able to execute function due to error: {e}")


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f'Did raise unwanted {exception}')


class Transformation:
    """Context manager to use within a test.

    possible usage:
    with Transformation(func) as test_logic:
        assert test_logic.runs_on_schema(schema)

    Usage as context manager should guarantee free memory after usage.
    """

    def __init__(self, func: Callable) -> None:
        self.func = func

    def __enter__(self):
        logger.info(f'Will test execution of transformation {self.func.__name__}.')
        yield self

    def runs_on_schema(self, schema: StructType):
        empty_df = Generator.create_empty_dataframe(schema)
        try:
            self.func(empty_df)
            return True
        except Exception as e:
            logger.error(f'Failed execution of function {self.func.__name__}: {e}')
            logger.debug(f'Tried execution on schema: {empty_df.printSchema()}')
            pytest.fail(str(e))

    def __exit__(self):
        logger.info(f'CleanUp test setup of transformation {self.func.__name__}.')
