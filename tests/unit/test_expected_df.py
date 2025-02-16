import pytest
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
)
from p3.dataframe import equal_schema


@pytest.fixture(scope='class')
def base_schema():
    return StructType([StructField('string', StringType(), True)])


@pytest.fixture(
    params=[
        pytest.param(0, id='none', marks=pytest.mark.xfail),
        pytest.param(1, id='single', marks=pytest.mark.xfail),
        pytest.param(
            2,
            id='double',
        ),
        pytest.param(3, id='multiple', marks=pytest.mark.xfail),
    ]
)
def range(request):
    return request.param


def test_schema_equal(range, base_schema) -> None:
    schemas = [base_schema] * range
    assert equal_schema(*schemas)
