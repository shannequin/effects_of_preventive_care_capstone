import pandas as pd

from extract import fetch_raw_data_map, extract_all_from_raw
from load import create_and_load_table, update_config_tables
from transform import clean_column_names


def create_additional_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create statistic type and cancer type field based on the source_file column.
    """

    # Split the source_file into multiple variables on the underscore
    source_file_split = df['source_file'].str.split('_', expand=True)

    # Create a statistic type field and populate it with source_file_split column 0 (replace dash with space)
    df['statistic_type'] = source_file_split.iloc[:, 0].str.replace("-", " ")

    print("Field created and populated: statistic_type")

    # Group by statistic_type and create a cancer_type field based on the source_file column.
    df['cancer_type'] = source_file_split.apply(
        lambda row: row[2].replace("-", " ") if "united-states" in row[1] else row[1].replace("-", " "), axis=1
    )

    print("Field created and populated: cancer_type")

    # Create a year field based on the uscs_year_map
    uscs_year_map = {
        "uscs_incidence_chart": "2018-2022",
        "uscs_mortality_chart": "2019-2023",
        "uscs_preliminary_estimates_chart": "2022",
        "uscs_prevalence_chart": "2017-2022",
        "uscs_stage_at_diagnosis_chart": "2018-2022",
        "uscs_trends_chart": "1999-2022"
    }
    df['year'] = df['source_file'].map(uscs_year_map)

    print("Field created and populated: year")

    return df

def fill_missing_sex_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in the sex column based on the source_file column.
    """
    df = df.copy()

    # Fill in missing sex values based on the source_file column and the sex_map
    sex_map = {
        "male-and-female": "Male and Female",
        "female": "Female",
        "male": "Male"
    }

    for k, v in sex_map.items():
        mask = (
            df['sex'].isna()
            & df['source_file'].str.contains(k)
        )

        df.loc[mask, 'sex'] = v

        print(f"Number of rows to be updated to {v}: {mask.sum()}")

    return df

def split_dataframe_by_statistic_type(df: pd.DataFrame) -> dict:
    """
    Split the dataframe into multiple dataframes based on the statistic_type column.
    Drop any columns that are all null values in each dataframe. Update column data types as needed.
    Returns a dictionary of dataframes with statistic_type as keys.
    """

    # Split the dataframe into a dictionary of dataframes based on the statistic type
    df_dict = {"_".join(stat_type.split()).lower(): sub_df for stat_type, sub_df in df.groupby('statistic_type')}

    for stat_type, df in df_dict.items():
        # Drop unnecessary columns
        df = df.drop(columns="source_file")
        df = df.dropna(axis=1, how='all')

        # Set list of keywords for columns needing a data type conversion
        column_map = ["count", "population", "year"]

        for col in df.columns:
            # Find column names containing any of the keywords
            if any(keyword in col.lower() for keyword in column_map):
                # Except columns containing 'pct'
                if "pct" in col:
                    break

                # Convert column data type to an int
                df[col] = df[col].astype("Int64")

        # Sort columns
        first_cols = ["statistic_type", "cancer_type", "sex"]
        remaining_cols = [col for col in df.columns if col not in first_cols]
        df = df[first_cols + remaining_cols]
        
        # Update the dataframe dictionary
        df_dict[stat_type] = df

    print(f"Dataframe split into {len(df_dict)} dataframes based on statistic_type.")

    return df_dict

def run_staging_etl_pipeline(dataset: str) -> None:
    """
    Run the staging USCS ETL pipeline to fetch data from a raw table, transform, and load it into the staging schema.
    """
    _, table_name = fetch_raw_data_map(dataset=dataset)

    # Generic extraction logic
    df = extract_all_from_raw(table_name=table_name)

    # Generic cleaning logic
    df = clean_column_names(df=df)

    # Dataset-specific transforming logic
    df = create_additional_fields(df=df)
    df = fill_missing_sex_values(df=df)
    df_dict = split_dataframe_by_statistic_type(df=df)

    # Generic loading logic
    for df_name, df in df_dict.items():
        create_and_load_table(
            df=df,
            table_name=df_name,
            schema="staging",
            if_exists="replace"
        )

        # Update the allowed tables configuration
        update_config_tables(table_name=df_name, schema="staging")

    print("Staging ETL pipeline completed.")


if __name__ == "__main__":

    DATASET = 'uscs'

    try:
        run_staging_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f"Error during staging ETL pipeline: {e}")
    