from extract import fetch_raw_data_map, extract_from_csv_files
from load import create_and_load_table, update_config_tables


def run_raw_etl_pipeline(dataset: str) -> None:
    """
    ETL pipeline for raw CSV data.
    """
    path, table_name = fetch_raw_data_map(dataset=dataset)

    # Generic csv extraction logic
    df = extract_from_csv_files(path=path)

    # Generic loading logic
    create_and_load_table(
        df=df,
        table_name=table_name,
        schema="raw",
        if_exists="replace"
    )

    # Update the allowed tables configuration
    update_config_tables(table_name=table_name, schema="raw")

    print("Raw ETL pipeline completed.")


if __name__ == "__main__":

    DATASET = 'nhis' # uscs, nhis

    try:
        run_raw_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f"Error during raw ETL pipeline: {e}")