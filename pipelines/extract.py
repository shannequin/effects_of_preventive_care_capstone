import json
import os
import pandas as pd
from sqlalchemy import text

from database.connection import get_db_connection


def get_file_names(path: str) -> list:
    """
    Get a list of file names in the specified directory.
    """
    file_names = [file.name for file in os.scandir(path=path) if file.is_file()]

    print(f"Found {len(file_names)} files in '{path}'")

    return file_names


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

    print(f"Extracted data from {len(df_list)} files.")

    return df_list

def merge_dataframes(df_list: list) -> pd.DataFrame:
    """
    Merge a list of dataframes into a single dataframe.
    """
    df = pd.concat(df_list, ignore_index=True)

    print(f"Merged dataframes into a single dataframe with shape: {df.shape}")

    return df

def extract_all_from_raw(table_name: str) -> pd.DataFrame:
    """
    Extract all records from the specified table in the raw schema of the database.
    """
    # Import list of allowed tables
    with open("config/tables.json") as f:
        tables_config = json.load(f)

    # Validate if the table name is in the allowed list
    if table_name not in tables_config["ALLOWED_RAW_TABLES"]:
        raise ValueError(f"Table '{table_name}' is not in the allowed list.")

    else:
        # Connect to the database
        engine = get_db_connection()

        # Fetch all records from the specified table
        with engine.begin() as conn:
            query = text(f"SELECT * FROM raw.{table_name}")
            df = pd.read_sql_query(query, conn)

        print(f"Extracted {len(df)} records from 'raw.{table_name}'")

        return df