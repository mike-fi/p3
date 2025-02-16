import logging
import _pytest  # noqa
import pytest
from pyspark.sql import SparkSession
from typing import Iterable

logger = logging.getLogger('p3')


@pytest.fixture(scope='session')
def spark():
    """Yield SparkSession for testing session scope."""
    logger.info('Creating SparkSession...')
    spark = SparkSession.builder.master('local[*]').appName('spark_testing').getOrCreate()  # type: ignore

    logger.info('Set logLevel of py4j logger to ERROR')
    logging.getLogger('py4j').setLevel(logging.ERROR)
    yield spark

    # stop session after usage
    logger.info('Stopping SparkSession...')
    spark.stop()


def pytest_addoption(parser):
    parser.addini('spark_remote_url', help='Remote URL for spark-connect')
    parser.addoption(
        '--spark-remote-url',
        dest='spark_remote_url',
        help='Remote URL for spark-connect',
    )

    parser.addini('spark_conf', help='Options to be used in SparkSession', type='linelist')


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'spark: signals that the respective test requires a SparkSession.',
    )


def pytest_collection_modifyitems(session, config, items: Iterable[pytest.Item]):  # pylint: disable=unused-argument
    """Mark tests that consume spark fixture with spark."""
    for item in items:
        logger.info(f'Collected Test: {item.name}')
        if item.iter_markers('spark'):
            logger.info('Encountered test marked with spark.')
            if 'spark' not in item.fixturenames:  # type: ignore
                logger.warning('Test marked with spark does not consume spark fixture.')

        if 'spark' in item.fixturenames and not item.iter_markers('spark'):  # type: ignore
            logger.info('Added spark marker to test with spark fixture')
            item.add_marker(pytest.mark.spark)
