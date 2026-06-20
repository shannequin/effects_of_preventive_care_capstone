from extract import get_file_names, extract_data_from_file_list, merge_dataframes
from load_raw import create_raw_table_from_df

def run_raw_etl_pipeline(table_name: str) -> None:
    """
    Run the raw ETL pipeline to extract data from raw files and load it into the database.
    """
    path = "raw_data"
    
    file_name_list = get_file_names(path)
    dataframe_list = extract_data_from_file_list(path, file_name_list)
    merged_dataframe = merge_dataframes(dataframe_list)
    create_raw_table_from_df(df=merged_dataframe, table_name=table_name)

if __name__ == "__main__":

    table_name = "" #"cdc_us_cancer_statistics"

    try:
        if table_name:
            run_raw_etl_pipeline(table_name=table_name)

    except Exception as e:
        raise RuntimeError(f"Error during raw ETL pipeline: {e}")