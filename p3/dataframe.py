import logging
from functools import reduce
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType
from pyspark.testing import assertDataFrameEqual, assertSchemaEqual

logger = logging.getLogger(__name__)


class UnsupportedArgsLength(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return str(self)


class SchemaDiff: ...


class DataDiff: ...


def equal_schema(*args: StructType) -> bool:
    if len(args) > 2:
        raise NotImplementedError()

    if len(args) < 2:
        raise UnsupportedArgsLength("Can't compare schemas if only one argument is given")

    diff = reduce(lambda s1, s2: set(s1) ^ set(s2), args)  # type: ignore
    logger.info(f'Calculated diff: {diff}')
    if not diff:
        return True
    else:
        return False


def equal_content(df1: DataFrame, df2: DataFrame) -> bool:
    df1_rows = df1.collect()
    df2_rows = df2.collect()
    df2_row_dict = [row.asDict() for row in df2_rows]

    assert len(df1_rows) == len(df2_rows)
    for row in df1_rows:
        if row.asDict() not in df2_row_dict:
            logger.debug(row.asDict())
            logger.debug('--------------')
            logger.debug(df2_row_dict)
            logger.debug('Incorrect Content')
            return False

    return True


class ExpectedDataFrame:
    """Context manager to use within a test.

    possible usage:
    with ExpectedDataFrame(df) as expected_df:
    or
    with ExpectedDataFrame.from_path(path_to_csv, "csv") as expected_df:
        expected_df == actual_df

    Usage as context manager should guarantee free memory after usage.
    """

    def __init__(self, df: DataFrame) -> None:
        self.df = df

    @classmethod
    def from_path(cls, path, format: str):
        spark = SparkSession.builder.getOrCreate()  # type: ignore
        df = spark.read.format(format).load(path)
        return cls(df)

    def __enter__(self):
        yield self

    def __exit__(self):
        """Remove References from cache."""
        self.df.unpersist()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataFrame):
            return NotImplemented
        return all(
            [assertDataFrameEqual(self.df, other), assertSchemaEqual(self.df.schema, other.schema)]
        )
