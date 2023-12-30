from typing import Dict, List, Union

import numpy as np
import pandas as pd
import streamlit as st


def read_in_intensities(
    file: str, cols_ints: str = "AD:BF"
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an Excel file and extracts intensity data from specified columns.

    Parameters:
        file (str): The path to the Excel file.
        cols_ints (str): Location of target columns.

    Returns:
        pandas.DataFrame or dict: A pandas DataFrame object containing the intensities read from the file.
            If the Excel file contains multiple sheets, a dictionary is returned, where each key represents
            the sheet name and the corresponding value is a DataFrame containing the intensities for that sheet.

    """
    return pd.read_excel(file, sheet_name=None, usecols=cols_ints, skiprows=1)


def read_in_scores(
    file: str, cols_scores: str = "A:AC"
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an Excel file and extracts score data from specified columns.

    Parameters:
        file (str): The path to the Excel file.
        cols_scores (str): Location of target columns.

    Returns:
        pandas.DataFrame or dict: A pandas DataFrame object containing the scores read from the file.
            If the Excel file contains multiple sheets, a dictionary is returned, where each key represents
            the sheet name and the corresponding value is a DataFrame containing the scores for that sheet.

    """
    return pd.read_excel(file, sheet_name=None, usecols=cols_scores, skiprows=1)


def extract_intensities(data: dict) -> pd.DataFrame:
    """
    Extracts intensities from a dictionary of pandas DataFrames.

    Parameters:
        data (dict): A dictionary where each key represents the sheet name and the corresponding value
            is a pandas DataFrame containing the intensities.

    Returns:
        pandas.DataFrame: A DataFrame containing the extracted intensities.

    """
    intensities_dict = {}

    for key, item in data.items():
        df_name = ["formula", "Cl", "intensities"]
        df = pd.DataFrame(columns=df_name)
        row_index = 0

        for index, row in item.iterrows():
            for i, j in zip(row, row.index):
                df.loc[row_index, "formula"] = row.Intensities
                df.loc[row_index, "Cl"] = j
                df.loc[row_index, "intensities"] = i
                row_index += 1

        df = df[df.Cl != "Intensities"]
        df["formula"] = df["formula"] + df["Cl"]
        df = df.drop(columns="Cl")
        intensities_dict[key] = df

    intensities = pd.concat(intensities_dict, axis=1)
    intensities.columns = intensities.columns.droplevel(1)
    intensities.index = intensities.iloc[:, 0]
    intensities.index = intensities.index.str.replace(".1", "", regex=False)
    intensities = intensities.iloc[:, 1::2]
    intensities = intensities.convert_dtypes()

    return intensities


def extract_scores(data: dict) -> pd.DataFrame:
    """
    Extracts scores from a dictionary of pandas DataFrames.

    Parameters:
        data (dict): A dictionary where each key represents the sheet name and the corresponding value
            is a pandas DataFrame containing the scores.

    Returns:
        pandas.DataFrame: A DataFrame containing the extracted scores.

    """
    scores_dict = {}

    for key, item in data.items():
        df_name = ["formula", "Cl", "intensities"]
        df = pd.DataFrame(columns=df_name)
        row_index = 0

        for index, row in item.iterrows():
            for i, j in zip(row, row.index):
                df.loc[row_index, "formula"] = row.Score
                df.loc[row_index, "Cl"] = j
                df.loc[row_index, "intensities"] = i
                row_index += 1

        df = df[df.Cl != "Score"]
        df["formula"] = df["formula"] + df["Cl"]
        df = df.drop(columns="Cl")
        scores_dict[key] = df

    scores = pd.concat(scores_dict, axis=1)
    scores.columns = scores.columns.droplevel(1)
    scores.index = scores.iloc[:, 0]
    scores = scores.iloc[:, 1::2]
    scores = scores.convert_dtypes()

    return scores


def data_cleanup(
    uploaded_files: Union[str, List[str]],
    threshold: int = 80,
    location_intensities: str = "AD:BF",
    location_scores: str = "A:AC",
) -> pd.DataFrame:
    """
    Perform data cleanup and filtering on uploaded files.

    Parameters:
        uploaded_files (Union[str, List[str]): A single file path or a list of file paths containing data.
        threshold (int, optional): The threshold for data filtering. Default is 80.
        location_intensities (str):
        location_scores (str):

    Returns:
        pd.DataFrame: A cleaned and filtered DataFrame.

    If no data is available or all data is below the threshold, the function returns None.

    Example:
        data = data_cleanup('data.csv', threshold=75)
        # or
        data = data_cleanup(['data1.csv', 'data2.csv'], threshold=80)
    """
    if not isinstance(uploaded_files, (list, tuple)):
        uploaded_files = [uploaded_files]

    dataframe_intensities = [
        read_in_intensities(file, cols_ints=location_intensities)
        for file in uploaded_files
    ]
    extracted_intensities = [
        extract_intensities(file) for file in dataframe_intensities
    ]

    dataframe_scores = [
        read_in_scores(file, cols_scores=location_scores) for file in uploaded_files
    ]
    extracted_scores = [extract_scores(file) for file in dataframe_scores]

    filtered_df = pd.concat(extracted_intensities, axis="columns")[
        pd.concat(extracted_scores, axis="columns") >= threshold
    ].dropna(how="all")

    return filtered_df


def convert_df(df: pd.DataFrame) -> bytes:
    """
    Convert a pandas DataFrame to a CSV format and encode it as UTF-8.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be converted to CSV.

    Returns:
        bytes: The CSV data as bytes encoded in UTF-8.

    This function takes a pandas DataFrame as input and converts it to a CSV (Comma-Separated Values) format.
    The resulting CSV data is then encoded using UTF-8 and returned as bytes.

    Example:
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        csv_bytes = convert_df(df)
    """
    return df.to_csv(index=True).encode("utf-8")
