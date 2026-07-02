import pandas as pd

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

    # Generic extraction logic
    with engine.connect() as conn:
        for chunk in pd.read_sql_query(query, conn, chunksize=50_000):
            cleaned_chunk = clean_chunk(chunk)

            cleaned_chunk.to_sql(
                staging_table,
                engine,
                schema="staging",
                if_exists="replace" if first_chunk else "append",
                index=False
            )

            first_chunk = False
            print(f"Processed {len(cleaned_chunk)} rows")

    # Generic cleaning logic
    df = clean_column_names(df=df)

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
