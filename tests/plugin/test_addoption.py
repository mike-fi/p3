import pytest

COLLECTION_FILE = """
        import pytest
        from pyspark.conf import SparkConf
        from pyspark.sql import SparkSession

        @pytest.mark.spark
        def test_spark_config_fixture(spark):
            assert isinstance(spark, SparkSession)

        def test_marker_addition(spark):
            assert True

        def test_hello_name(name):
            assert hello(name) == "Hello {0}!".format(name)
    """

CONFTEST_FILE = """
        import pytest
        pytest_plugins = "p3"


        @pytest.fixture(params=[
            "Brianna",
            "Andreas",
            "Floris",
        ])
        def name(request):
            return request.param
    """


def test_active_plugin(pytester):
    # create a temporary conftest.py file
    res = pytester.runpytest()
    plugins_line = [s for s in res.outlines if s.startswith('plugins:')][0]
    assert 'pyspark-plugin' in plugins_line


def test_available_fixtures(pytester):
    # create a temporary conftest.py file
    pytester.makeconftest(CONFTEST_FILE)
    res = pytester.runpytest('--fixtures')
    assert any('spark [session scope]' in line for line in res.outlines)


def test_oppressing_plugin(pytester):
    # create a temporary conftest.py file
    pytester.makeconftest(CONFTEST_FILE)
    res = pytester.runpytest('-p no:p3')
    print(type(res.outlines))
    assert not any('spark [session scope]' in line for line in res.outlines)


def test_spark_marker(pytester):
    """Make sure that plugin works."""
    # create a temporary conftest.py file
    pytester.makeconftest(CONFTEST_FILE)

    # create a temporary pytest test file
    pytester.makepyfile(COLLECTION_FILE)

    # run all tests with spark marker
    result = pytester.runpytest('-m spark')

    # check that all 4 tests passed
    # We deselect the test that uses spark fixture tho, tbd.
    result.assert_outcomes(passed=1, deselected=4)


@pytest.mark.xfail(reason='still select tests using SparkSession fixture.')
def test_no_spark_marker(pytester):
    """Make sure that plugin works."""
    pytester.makeconftest(CONFTEST_FILE)
    pytester.makepyfile(COLLECTION_FILE)

    # run all tests without spark marker
    # Doesnt work at the moment due to string representation
    result = pytester.runpytest(r'-m "not spark"')

    # check that all 4 tests passed
    # Still problem with
    result.assert_outcomes(passed=4, deselected=1)
