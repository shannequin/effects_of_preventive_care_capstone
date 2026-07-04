import json
import pandas as pd
from torch import chunk

from config.brfss_value_map import brfss_value_map
from database.connection import get_db_connection
from extract import fetch_raw_data_map, validate_table_name
from load import create_and_load_table, update_config_tables
from transform import clean_column_names


def determine_weight_measurement(weight):
    """
    Determine the weight measurement based on the weight value.
    """
    try:
        if int(weight) <= 776:
            return 'lbs'
        elif 9023 <= int(weight) <= 9352:
            return 'kg'
        else:
            return ''
    except:
        return ''

def determine_height_measurement(height):
    """
    Determine the height measurement based on the height value.
    """
    try:
        if int(height) <= 711:
            return 'inches'
        elif 9061 <= int(height) <= 9998:
            return 'cm'
        else:
            return ''
    except:
        return ''

def determine_alcday4_measurement(alcday4):
    """
    Determine the alcday4 measurement based on the alcday4 value.
    Strip the prefixed digit from the alcday4 value if applicable.
    """
    try:
        if 201 <= int(alcday4) <= 299:
            return alcday4[1:], 'Days in past 30 days'
        elif 101 <= int(alcday4) <= 199:
            return alcday4[1:], 'Days per week'
        else:
            return alcday4, ''

    except:
        return alcday4, ''

def run_staging_etl_pipeline(dataset: str) -> None:
    """
    raw PostgreSQL table
        ↓
    read in chunks
        ↓
    clean each chunk
        ↓
    append cleaned chunk to staging table
    ---
    For the first chunk, replace the staging table:

    if_exists='replace'

    For later chunks, append:

    if_exists='append'
    """
    _, table_name = fetch_raw_data_map(dataset=dataset)

    validate_table_name(table_name=table_name)

    engine = get_db_connection()

    with engine.begin() as conn:
        chunksize = 50000

        query = f"""SELECT "{'", "'.join(brfss_value_map.keys())}"
                    FROM raw.{table_name}"""

        print(f'TEST QUERY: {query}')

        for chunk_number, chunk in enumerate(pd.read_sql_query(sql=query, con=conn, chunksize=chunksize), start=1):
            if chunk_number == 2:
                break

            print(f'TEST CHUNK NUMBER: {chunk_number}')
            print(f'TEST CHUNK LENGTH: {len(chunk)}')


            # Generic cleaning logic


            # Dataset-specific transforming logic
            # Map values
            valid_value_maps = {
                key: value
                for key, value in brfss_value_map.items()
                if key in chunk.columns
            }

            chunk = chunk.replace(valid_value_maps)

            chunk = clean_column_names(df=chunk)

            # Combine ladult1 and cadult1
            chunk['adult1'] = chunk['ladult1'].combine_first(chunk['cadult1'])
            chunk = chunk.drop(columns=['ladult1', 'cadult1']).fillna("Not asked or missing")

            # Combine landsex3 and cellsex3
            chunk['sex3'] = chunk['landsex3'].combine_first(chunk['cellsex3'])
            chunk = chunk.drop(columns=['landsex3', 'cellsex3']).fillna('Not asked or missing')

            # Create column next to weight2 for measurement
            chunk.insert(
                loc=chunk.columns.get_loc('weight2') + 1,
                column='weight2_measurement',
                value=chunk['weight2'].apply(determine_weight_measurement)
            )

            # Create column next to height3 for measurement
            chunk.insert(
                loc=chunk.columns.get_loc('height3') + 1,
                column='height3_measurement',
                value=chunk['height3'].apply(determine_height_measurement)
            )

            # Create a column next to alcday4 to indicate the measurement
            chunk[['alcday4', 'alcday4_measurement']] = chunk['alcday4'].apply(
                lambda x: pd.Series(determine_alcday4_measurement(x))
            )

            print(f'TEST CHUNK SAMPLE:\n{chunk.sample(10)}')

            chunk.to_sql(
                name=table_name,
                con=conn,
                schema='staging',
                if_exists='replace' if chunk_number == 1 else 'append',
                index=False
            )

            print('----------')

    # Update the allowed tables configuration
    update_config_tables(table_name=table_name, schema='staging')

    print('Staging ETL pipeline completed.')


if __name__ == '__main__':

    DATASET = 'brfss'

    try:
        run_staging_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f'Error during staging ETL pipeline: {e}')
