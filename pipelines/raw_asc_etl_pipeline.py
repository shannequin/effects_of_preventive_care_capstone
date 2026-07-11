import os
import pandas as pd

from database.connection import get_db_connection
from extract import fetch_raw_data_map, fetch_asc_column_map
from load import update_config_tables


def extract_map_load_asc(path: str, table_name: str, dataset: str):
    """
    For each line in the ASC file, extract the data, map the columns, and load it into the specified raw table.
    """
    # Verify the path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f'The file at path \'{path}\' does not exist.')

    else:
        # Initialize the database connection
        engine = get_db_connection()

        with open(path) as f:
            for i, line in enumerate(f, start=1):
                row_dict = {}

                # Map the values to the columns
                for header, map in fetch_asc_column_map(dataset=dataset).items():
                    row_dict[header] = [line[map['column'] - 1 : map['column'] + map['length'] - 1]]

                # Create a DataFrame from the row dictionary
                df = pd.DataFrame(row_dict)

                # Create and load the table
                with engine.begin() as conn:
                    df.to_sql(
                        name=table_name,
                        con=conn,
                        schema='raw',
                        if_exists='append',
                        index=False
                    )

                print(f'Table \'raw.{table_name}\' appended with record number {i}.')

def run_raw_etl_pipeline(dataset: str) -> None:
    """
    ETL pipeline for raw ASC data.
    """
    path, table_name = fetch_raw_data_map(dataset=dataset)

    # ASC specific extraction, mapping, and loading logic
    extract_map_load_asc(path=path, table_name=table_name, dataset=dataset)

    # Update the allowed tables configuration
    update_config_tables(table_name=table_name, schema='raw')

    print('Raw ETL pipeline completed.')


if __name__ == '__main__':

    DATASET = 'brfss'

    try:
        run_raw_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f'Error during raw ETL pipeline: {e}')