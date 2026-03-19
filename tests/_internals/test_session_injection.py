import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, StructField, StructType
from p3._internals import Generator, Transformation


@pytest.mark.spark
def test_generator_uses_provided_session(spark) -> None:
    schema = StructType([StructField('value', StringType(), True)])
    df = Generator.create_empty_dataframe(schema, spark=spark)
    assert df.sparkSession is spark


@pytest.mark.spark
def test_transformation_uses_provided_session(spark) -> None:
    schema = StructType([StructField('value', StringType(), True)])

    def assert_session(df: DataFrame) -> DataFrame:
        assert df.sparkSession is spark
        return df

    transformation = Transformation(assert_session)
    assert transformation.runs_on_schema(schema, spark=spark) is True
