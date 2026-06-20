import os
import pandas as pd


def get_file_names(path: str) -> list:
    """
    Get a list of file names in the specified directory.
    """
    return [file.name for file in os.scandir(path=path) if file.is_file()]


def extract_data_from_file_list(path: str, file_name_list: list) -> list:
    """
    Create a list of dataframes by reading the data files.
    Add a column for the source file name to each dataframe for traceability.
    """
    df_list = []

    for file_name in file_name_list:
        df = pd.read_csv(filepath_or_buffer=os.path.join(path, file_name))
        df['source_file'] = file_name
        df_list.append(df)

    return df_list

def merge_dataframes(df_list: list) -> pd.DataFrame:
    """
    Merge a list of dataframes into a single dataframe.
    """
    return pd.concat(df_list, ignore_index=True)
