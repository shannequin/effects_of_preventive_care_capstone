from extract import extract_all_from_raw
from load import create_and_load_table
from transform import (clean_column_names,
                       create_additional_fields,
                       fill_missing_sex_values,
                       split_dataframe_by_statistic_type)


#TODO: Add years to the datasets (leaning towards tablename over column)
#TODO: Update to handle different datasets like nhis


def run_staging_etl_pipeline(table_name: str) -> None:
    """
    Run the staging ETL pipeline to fetch data from a raw table, clean, and load it into the staging schema.
    """
    # Run generic cleaning logic
    df = extract_all_from_raw(table_name=table_name)
    df = clean_column_names(df=df)

    # Run dataset-specific transforming logic
    df = create_additional_fields(df=df)
    df = fill_missing_sex_values(df=df)
    df_dict = split_dataframe_by_statistic_type(df=df)

    # Run generic loading logic
    for df_name, df in df_dict.items():
        create_and_load_table(
            df=df,
            table_name=df_name,
            schema="staging",
            if_exists="replace"
        )

    print(f"Staging ETL pipeline completed.")

if __name__ == "__main__":

    # Set the table name for extract
    table_name = "cdc_us_cancer_statistics"

    try:
        # If a table name is given, then run the pipeline
        if table_name:
            run_staging_etl_pipeline(table_name=table_name)

    except Exception as e:
        raise RuntimeError(f"Error during staging ETL pipeline: {e}")
    