from extract import extract_all_from_raw
from transform import clean_column_names, create_statistic_type_field, fill_missing_sex_values


def run_staging_etl_pipeline(table_name: str) -> None:
    """
    Run the staging ETL pipeline to fetch data from a raw table, clean, and load it into the staging schema.
    """
    
    df = extract_all_from_raw(table_name=table_name)
    df = clean_column_names(df=df)
    df = create_statistic_type_field(df=df)
    df = fill_missing_sex_values(df=df)
    # TODO: Split the dataframe into multiple staging tables based on the statistic_type
    # TODO: Create and clean the cancer_type field based on the source_file column
    # TODO: Load the cleaned data into the staging schema in the database
    print(f"Staging ETL pipeline completed for table '{table_name}'.")

if __name__ == "__main__":

    table_name = "cdc_us_cancer_statistics"

    try:
        if table_name:
            run_staging_etl_pipeline(table_name=table_name)

    except Exception as e:
        raise RuntimeError(f"Error during staging ETL pipeline: {e}")
    