import logging
import pytest
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


@pytest.mark.spark
def test_spark_fixture(spark):
    """Assert fixture has correct type."""
    assert isinstance(spark, SparkSession)
