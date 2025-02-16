from pyspark.sql import DataFrame


class DataFrameDiff:
    """Class to easily compare and pretty print difference of two DataFrames."""

    def __init__(self, left: DataFrame, right: DataFrame):
        self._left_df = left
        self._right_df = right
