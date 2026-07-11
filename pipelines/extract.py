import json
import os
import pandas as pd
from sqlalchemy import text

from database.connection import get_db_connection


def validate_table_name(table_name: str) -> None:
    """
    Validate that the given table name is in the list of allowed raw tables.
    """
    with open('config/allowed_tables.json') as f:
        tables_config = json.load(f)

    if table_name not in tables_config['ALLOWED_RAW_TABLES']:
        raise ValueError(f'Table \'{table_name}\' is not in the allowed list.')

def fetch_raw_data_map(dataset: str) -> tuple[str, str]:
    """
    Fetch the path and table name for the given dataset.
    """
    with open('config/raw_data_map.json') as f:
        raw_data_map = json.load(f)

    path = raw_data_map[dataset].get('path')
    table_name = raw_data_map[dataset].get('table_name')

    return path, table_name

def extract_from_csv_files(path: str) -> pd.DataFrame:
    """
    Extract data from all CSV files in the specified path and return a merged dataframe.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f'The file at path \'{path}\' does not exist.')

    else:
        df_list = []

        for file in os.scandir(path=path):
            df = pd.read_csv(filepath_or_buffer=os.path.join(path, file.name))
            df['source_file'] = file.name
            df_list.append(df)

        print(f'Extracted data from {len(df_list)} files.')

        df = pd.concat(df_list, ignore_index=True)

        print(f'Merged dataframes into a single dataframe with shape: {df.shape}')

        return df

def fetch_asc_column_map(dataset: str) -> json:
    """
    Fetch the asc column map for the given dataset.
    """
    with open(f'config/{dataset}_column_map.json') as f:
        return json.load(f)

def extract_all_from_raw(table_name: str) -> pd.DataFrame:
    """
    Extract all records from the specified table in the raw schema of the database.
    """
    validate_table_name(table_name=table_name)

    engine = get_db_connection()

    with engine.begin() as conn:
        query = text(f'SELECT * FROM raw.{table_name}')
        df = pd.read_sql_query(query, conn)

    print(f'Extracted {len(df)} records from \'raw.{table_name}\'')

    return df