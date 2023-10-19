import pandas as pd
import numpy as np
import streamlit as st
from typing import Union, Dict

def read_in_intensities(file: str) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an Excel file and extracts intensity data from specified columns.

    Parameters:
        file (str): The path to the Excel file.

    Returns:
        pandas.DataFrame or dict: A pandas DataFrame object containing the intensities read from the file.
            If the Excel file contains multiple sheets, a dictionary is returned, where each key represents
            the sheet name and the corresponding value is a DataFrame containing the intensities for that sheet.

    """
    return pd.read_excel(file,
                         sheet_name=None,
                         usecols='AD:BF',
                         skiprows=1
                        )

def read_in_scores(file: str) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an Excel file and extracts score data from specified columns.

    Parameters:
        file (str): The path to the Excel file.

    Returns:
        pandas.DataFrame or dict: A pandas DataFrame object containing the scores read from the file.
            If the Excel file contains multiple sheets, a dictionary is returned, where each key represents
            the sheet name and the corresponding value is a DataFrame containing the scores for that sheet.

    """
    return pd.read_excel(file,
                         sheet_name=None,
                         usecols='A:AC',
                         skiprows=1
                        )

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
        df_name = ['formula', 'Cl', 'intensities']
        df = pd.DataFrame(columns=df_name)
        row_index = 0
        
        for index, row in item.iterrows():
            for i, j in zip(row, row.index):
                df.loc[row_index, 'formula'] = row.Intensities
                df.loc[row_index, 'Cl'] = j
                df.loc[row_index, 'intensities'] = i
                row_index += 1

        df = df[df.Cl != 'Intensities']
        df['formula'] = df['formula'] + df['Cl']
        df = df.drop(columns='Cl')
        intensities_dict[key] = df   
        
    intensities = pd.concat(intensities_dict, axis=1)
    intensities.columns = intensities.columns.droplevel(1)
    intensities.index = intensities.iloc[:, 0]
    intensities.index = intensities.index.str.replace('.1', '', regex=False)
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
        df_name = ['formula', 'Cl', 'intensities']
        df = pd.DataFrame(columns=df_name)
        row_index = 0
        
        for index, row in item.iterrows():
            for i, j in zip(row, row.index):
                df.loc[row_index, 'formula'] = row.Score
                df.loc[row_index, 'Cl'] = j
                df.loc[row_index, 'intensities'] = i
                row_index += 1

        df = df[df.Cl != 'Score']
        df['formula'] = df['formula'] + df['Cl']
        df = df.drop(columns='Cl')
        scores_dict[key] = df   

    scores = pd.concat(scores_dict, axis=1)
    scores.columns = scores.columns.droplevel(1)
    scores.index = scores.iloc[:, 0]
    scores = scores.iloc[:, 1::2]
    scores = scores.convert_dtypes()
    
    return scores

def data_cleanup(uploaded_files, threshold = 80):

    dataframe_intensities = [read_in_intensities(file) for file in uploaded_files]
    extracted_intensities = [extract_intensities(file) for file in dataframe_intensities]

    dataframe_scores = [read_in_scores(file) for file in uploaded_files]
    extracted_scores = [extract_scores(file) for file in dataframe_scores]

    if not extracted_intensities or not extracted_scores:
        # Handle the case where no data is available
        st.error("No data available for processing.")
        return pd.DataFrame()  # Return an empty DataFrame or None

    return pd.concat(extracted_intensities)[pd.concat(extracted_scores) > threshold].dropna(how='all')

def convert_df(df):
   return df.to_csv(index=True).encode('utf-8')