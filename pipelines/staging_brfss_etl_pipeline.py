import json
import pandas as pd

from config.brfss_value_map import brfss_value_map
from database.connection import get_db_connection
from extract import fetch_raw_data_map
from load import create_and_load_table, update_config_tables
from transform import clean_column_names


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

    if_exists="replace"

    For later chunks, append:

    if_exists="append"

    Small table      → read all at once
    Medium table     → pandas chunksize
    Large table      → chunksize + SQL filtering
    Very large table → consider SQL transformations, COPY, or a tool like dbt/Airflow
    """
    _, table_name = fetch_raw_data_map(dataset=dataset)

    with open("config/allowed_tables.json") as f:
        tables_config = json.load(f)

    if table_name not in tables_config["ALLOWED_RAW_TABLES"]:
        raise ValueError(f"Table '{table_name}' is not in the allowed list.")

    else:
        engine = get_db_connection()

        with engine.connect() as conn:
            chunksize = 50000
            is_first_chunk = True

            query = f"""SELECT "{'", "'.join(brfss_value_map.keys())}"
                      FROM raw.{table_name}"""
            
            print(f"TEST QUERY: {query}")

            for chunk_number, chunk in enumerate(pd.read_sql_query(sql=query, con=conn, chunksize=chunksize)):
                print(f"TEST CHUNK NUMBER: {chunk_number}")
                print(f"TEST CHUNK LENGTH: {len(chunk)}")
                print(f"TEST CHUNK HEAD:\n{chunk.head(1)}")
                
                chunk = clean_column_names(df=chunk)
                print(f"TEST CHUNK CLEANED COLUMNS:\n{chunk.columns}")

                if is_first_chunk:
                    # Replace the staging table with the first chunk
                    print(f"TEST IS FIRST CHUNK: {is_first_chunk}")
                    is_first_chunk = False
                    
                else:
                    # Append subsequent chunks to the staging table
                    print(f"TEST IS FIRST CHUNK: {is_first_chunk}")

                #     cleaned_chunk = clean_chunk(chunk)

                #     cleaned_chunk.to_sql(
                #         staging_table,
                #         engine,
                #         schema="staging",
                #         if_exists="replace" if first_chunk else "append",
                #         index=False
                #     )

                #     first_chunk = False
                #     print(f"Processed {len(cleaned_chunk)} rows")


                # Dataset-specific transforming logic
                # df = pre_split_cleaning(df=df)
                # df_dict = split_dataframe_by_code(df=df)

                # Generic loading logic
                # for df_name, df in df_dict.items():

                #     create_and_load_table(
                #         df=df,
                #         table_name=TABLE_NAME_MAP.get(df_name, df_name),
                #         schema="staging",
                #         if_exists="replace"
                #     )

                #     # Update the allowed tables configuration
                #     update_config_tables(table_name=TABLE_NAME_MAP.get(df_name, df_name), schema="staging")

    print("Staging ETL pipeline completed.")


if __name__ == "__main__":

    DATASET = 'brfss'

    try:
        run_staging_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f"Error during staging ETL pipeline: {e}")
