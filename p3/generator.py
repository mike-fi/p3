import logging
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


class Generator:
    @staticmethod
    def create_empty_dataframe(schema: StructType) -> DataFrame:
        spark = SparkSession.builder.getOrCreate()  # type: ignore
        logger.debug(f'Creating empty df with schema {schema}')
        empty_df = spark.createDataFrame([], schema)

        logger.debug('Empty df created successfully')
        return empty_df

    @staticmethod
    def create_dataframe(schema: StructType) -> DataFrame:
        raise NotImplementedError('Synthetic Data Generation is currently not supported')
