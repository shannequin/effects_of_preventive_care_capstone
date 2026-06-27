from extract import extract_all_from_raw
from load import create_and_load_staging_tables
from transform import (clean_column_names,
                       create_additional_fields,
                       fill_missing_sex_values,
                       split_dataframe_by_statistic_type)


def run_staging_etl_pipeline(table_name: str) -> None:
    """
    Run the staging ETL pipeline to fetch data from a raw table, clean, and load it into the staging schema.
    """
    df = extract_all_from_raw(table_name=table_name)
    df = clean_column_names(df=df)
    df = create_additional_fields(df=df)
    df = fill_missing_sex_values(df=df)
    df_dict = split_dataframe_by_statistic_type(df=df)
    create_and_load_staging_tables(df_dict=df_dict)
    print(f"Staging ETL pipeline completed.")

if __name__ == "__main__":

    # Set the table name
    table_name = "" #"cdc_us_cancer_statistics"

    try:
        # If a table name is given, then run the pipeline
        if table_name:
            run_staging_etl_pipeline(table_name=table_name)

    except Exception as e:
        raise RuntimeError(f"Error during staging ETL pipeline: {e}")
    