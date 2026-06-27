import json

from extract import (get_file_names,
                     extract_data_from_file_list,
                     merge_dataframes)
from load import create_and_load_raw_table


def run_raw_etl_pipeline(path: str, table_name: str) -> None:
    """
    Run the raw ETL pipeline to extract data from raw files and load it into the raw schema.
    """
    # Pipeline functions
    file_name_list = get_file_names(path)
    dataframe_list = extract_data_from_file_list(path, file_name_list)
    merged_dataframe = merge_dataframes(dataframe_list)
    create_and_load_raw_table(df=merged_dataframe, table_name=table_name)

    print(f"Raw ETL pipeline completed for table '{table_name}'.")

if __name__ == "__main__":
    # Fetch the path and table name for the raw data
    with open("config/raw_data_map.json") as f:
        raw_data_map = json.load(f)

    # Set the data source
    source = raw_data_map['nhis']

    try:
        # Run the pipeline
        run_raw_etl_pipeline(path=source['path'], table_name=source['table_name'])

    except Exception as e:
        raise RuntimeError(f"Error during raw ETL pipeline: {e}")