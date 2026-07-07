import pandas as pd
from torch import chunk

from config.brfss_value_map import brfss_value_map
from database.connection import get_db_connection
from extract import fetch_raw_data_map, validate_table_name
from load import update_config_tables
from transform import clean_column_names


SCHEMA = 'staging'

def transform_idate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the idate column to a standard format.
    """
    df['idate'] = pd.to_datetime(df['idate'], format='%m%d%Y', errors='coerce').dt.strftime('%m-%d-%Y')

    return df

def transform_adult1(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create adult1 column by combining ladult1 and cadult1.
    """
    df.insert(
        loc=df.columns.get_loc('ladult1') + 1,
        column='adult1',
        value=df['ladult1'].combine_first(df['cadult1'])
    )
    df = df.drop(columns=['ladult1', 'cadult1'])

    return df

def transform_sex3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create sex3 column by combining landsex3 and cellsex3.
    """
    df.insert(
        loc=df.columns.get_loc('landsex3') + 1,
        column='sex3',
        value=df['landsex3'].combine_first(df['cellsex3'])
    )
    df = df.drop(columns=['landsex3', 'cellsex3'])

    return df

def determine_weight2_measurement(weight: str) -> str:
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

def transform_weight2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create weight2 measurement column based on the weight2 value.
    """
    df.insert(
        loc=df.columns.get_loc('weight2') + 1,
        column='weight2_measurement',
        value=df['weight2'].apply(determine_weight2_measurement)
    )

    return df

def convert_height3(height: str) -> str:
    """
    Convert height3 value to inches or centimeters based on its range.
    """
    try:
        if int(height) <= 711:
            # Convert the first 2 characters to feet and the last 2 char to inches
            feet = int(height[:2])
            inches = int(height[2:])

            return str(feet * 12 + inches)

        elif 9061 <= int(height) <= 9998:
            # Convert the last 3 characters to centimeters
            return height[-3:]

        else:
            return height

    except:
        return height

def determine_height3_measurement(height: str) -> str:
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

def transform_height3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert height3 values to inches/cm and create a corresponding measurement column.
    """
    df.insert(
        loc=df.columns.get_loc('height3') + 1,
        column='height3_measurement',
        value=df['height3'].apply(determine_height3_measurement)
    )

    df['height3'] = df['height3'].apply(convert_height3)

    return df

def transform_flshtmy3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the flshtmy3 column to a standard format.
    """
    df['flshtmy3'] = pd.to_datetime(df['flshtmy3'], format='%m%Y', errors='coerce').dt.strftime('%m-%Y')

    return df

def transform_hivtstd3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the hivtstd3 column to a standard format.
    """
    df['hivtstd3'] = pd.to_datetime(df['hivtstd3'], format='%m%Y', errors='coerce').dt.strftime('%m-%Y')

    return df

def transform_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform missing values to a standard format.
    """
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    df = df.replace(r'^(?i:na|nan|none|null)$', pd.NA, regex=True)

    return df

def run_staging_etl_pipeline(dataset: str) -> None:
    """
    Run the staging ETL pipeline for the specified dataset.
    This involves extracting raw data, transforming it, and loading it into the staging table.
    """
    _, table_name = fetch_raw_data_map(dataset=dataset)

    validate_table_name(table_name=table_name)

    query = f"""SELECT "{'", "'.join(brfss_value_map.keys())}"
                FROM raw.{table_name}"""

    CHUNKSIZE = 50000

    engine = get_db_connection()

    with engine.begin() as conn:

        for chunk_number, chunk in enumerate(pd.read_sql_query(sql=query, con=conn, chunksize=CHUNKSIZE), start=1):
            print(f'TEST CHUNK NUMBER: {chunk_number}')
            print(f'TEST CHUNK LENGTH: {len(chunk)}')

            # Map integer values to strings
            valid_value_maps = {
                key: value
                for key, value in brfss_value_map.items()
                if key in chunk.columns
            }
            chunk = chunk.replace(valid_value_maps)

            # Clean column names
            chunk = clean_column_names(chunk)

            # Transform columns
            chunk = transform_idate(chunk)
            chunk = transform_adult1(chunk)
            chunk = transform_sex3(chunk)
            chunk = transform_weight2(chunk)
            chunk = transform_height3(chunk)
            chunk = transform_flshtmy3(chunk)
            chunk = transform_hivtstd3(chunk)
            chunk = transform_missing_values(chunk)

            print(f'TEST CHUNK SAMPLE:\n{chunk.sample(10)}')

            chunk.to_sql(
                name=table_name,
                con=conn,
                schema=SCHEMA,
                if_exists='replace' if chunk_number == 1 else 'append',
                index=False
            )

            print('----------')

        # Create a table for questions
        questions_df  = pd.DataFrame(data={
            'Field': list(brfss_value_map.keys()),
            'Question': [v['Question'] for v in brfss_value_map.values()]
        })

        questions_df.to_sql(
            name=f'{table_name}_questions',
            con=conn,
            schema=SCHEMA,
            if_exists='replace',
            index=False
        )

    # Update the allowed tables configuration
    update_config_tables(table_name=table_name, schema=SCHEMA)
    update_config_tables(table_name=f'{table_name}_questions', schema=SCHEMA)

    print(f'{SCHEMA} ETL pipeline completed.')


if __name__ == '__main__':

    DATASET = 'brfss'

    try:
        run_staging_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f'Error during {SCHEMA} ETL pipeline: {e}')
