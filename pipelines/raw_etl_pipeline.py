from extract import (get_file_names,
                     extract_data_from_file_list,
                     merge_dataframes)
from load import create_and_load_raw_table


def run_raw_etl_pipeline(table_name: str) -> None:
    """
    Run the raw ETL pipeline to extract data from raw files and load it into the raw schema.
    """
    # Set the path for the raw data
    path = "data_to_ingest"

    # Pipeline functions
    file_name_list = get_file_names(path)
    dataframe_list = extract_data_from_file_list(path, file_name_list)
    merged_dataframe = merge_dataframes(dataframe_list)
    create_and_load_raw_table(df=merged_dataframe, table_name=table_name)

    print(f"Raw ETL pipeline completed for table '{table_name}'.")

if __name__ == "__main__":

    # Set table name
    table_name = "" #"cdc_us_cancer_statistics"

    try:
        # If a table name is given, run the pipeline
        if table_name:
            run_raw_etl_pipeline(table_name=table_name)

    except Exception as e:
        raise RuntimeError(f"Error during raw ETL pipeline: {e}")