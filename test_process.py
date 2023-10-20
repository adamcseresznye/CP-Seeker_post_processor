from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import process


@pytest.fixture
def get_test_output_10_percent():
    return Path.cwd().joinpath(r"data/CPSeeker0.1_test_output_10_percent.xlsx")


@pytest.fixture
def get_test_output_50_percent():
    return Path.cwd().joinpath(r"data/CPSeeker0.1_test_output_50_percent.xlsx")


@pytest.fixture
def get_test_output_80_percent():
    return Path.cwd().joinpath(r"data/CPSeeker0.1_test_output_80_percent.xlsx")


def test_read_in_intensities_column_number(get_test_output_80_percent):
    """This test confirms that the number of columns read in equals to 29"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    assert dicts["test_80"].shape[1] == 29


def test_read_in_intensities_column_starts_with_intensities(get_test_output_80_percent):
    """This test confirms that the first column read in is called Intensities"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    assert dicts["test_80"].iloc[:, 0].name == "Intensities"


def test_read_in_intensities_sum_values(get_test_output_80_percent):
    """This test confirms that the sum of intensities equal to 868 (31 rows x 28 columns)"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    assert dicts["test_80"].iloc[:, 1:].sum().sum() == 868


def test_read_in_intensities_shape(get_test_output_80_percent):
    """This test confirms the shape of the dataframe (31,29)"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    assert dicts["test_80"].shape[0] == 31 and dicts["test_80"].shape[1] == 29


def test_read_in_scores_column_number(get_test_output_80_percent):
    """This test confirms that the number of columns read in equals to 29"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    assert dicts["test_80"].shape[1] == 29


def test_read_in_scores_column_starts_with_intensities(get_test_output_80_percent):
    """This test confirms that the first column read in is called Score"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    assert dicts["test_80"].iloc[:, 0].name == "Score"


def test_read_in_scores_sum_values(get_test_output_80_percent):
    """This test confirms that the sum of intensities equal to 69440 (31 rows x 28 columns x 80)"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    assert dicts["test_80"].iloc[:, 1:].sum().sum() == 69440


def test_read_in_scores_shape(get_test_output_80_percent):
    """This test confirms that the shape of the dataframe is (31,29)"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    assert dicts["test_80"].shape[0] == 31 and dicts["test_80"].shape[1] == 29


def test_extract_intensities_shape(get_test_output_80_percent):
    """This test confirms that the shape of processed series is (868,1)"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    processed_df = process.extract_intensities(dicts)
    assert processed_df.shape[0] == 868 and processed_df.shape[1] == 1


def test_extract_intensities_sum(get_test_output_80_percent):
    """This test confirms that the sum of intensities is 868 (31 rows x 28 columns)"""
    dicts = process.read_in_intensities(get_test_output_80_percent)
    processed_df = process.extract_intensities(dicts)
    assert processed_df.sum().values[0] == 868


def test_extract_scores_shape(get_test_output_80_percent):
    """This test confirms that the shape of processed series is (868,1)"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    processed_df = process.extract_scores(dicts)
    assert processed_df.shape[0] == 868 and processed_df.shape[1] == 1


def test_extract_scores_sum(get_test_output_80_percent):
    """This test confirms that the sum of intensities is 868 (31 rows x 28 columns)"""
    dicts = process.read_in_scores(get_test_output_80_percent)
    processed_df = process.extract_scores(dicts)
    assert processed_df.sum().values[0] == 69440


def test_data_cleanup_shape_confidence_10_threshold_5(get_test_output_10_percent):
    """This test confirms that all the values are returned when confidence values are 10 and threshold = 5"""
    df = process.data_cleanup(get_test_output_10_percent, threshold=5)
    assert df.shape[0] == 868 and df.shape[1] == 1


def test_data_cleanup_shape_confidence_10_threshold_80(get_test_output_10_percent):
    """This test confirms that no values are returned when confidence values are 10 and threshold = 80"""
    df = process.data_cleanup(get_test_output_10_percent, threshold=80)
    assert df.shape[0] == 0 and df.shape[1] == 1


def test_data_cleanup_shape_confidence_50_threshold_80(get_test_output_50_percent):
    """This test confirms that no values are returned when confidence values are 50 and threshold = 80"""
    df = process.data_cleanup(get_test_output_50_percent, threshold=80)
    assert df.shape[0] == 0 and df.shape[1] == 1


def test_data_cleanup_shape_confidence_80_threshold_80(get_test_output_80_percent):
    """This test confirms that all values are returned when confidence values are 80 and threshold = 80"""
    df = process.data_cleanup(get_test_output_80_percent, threshold=80)
    assert df.shape[0] == 868 and df.shape[1] == 1
