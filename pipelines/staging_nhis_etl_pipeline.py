import pandas as pd

from extract import fetch_raw_data_map, extract_all_from_raw
from load import create_and_load_table, update_config_tables
from transform import clean_column_names


TABLE_NAME_MAP = {
    'AHS-01': 'ahs01_health_insurance',
    'C-05': 'c05_breast_cancer_screenings',
    'C-07': 'c07_colorectal_cancer_screenings',
    'C-09': 'c09_cervical_cancer_screenings',
    'IID-09': 'iid09_flu_vaccinations',
    'OHM-01': 'ohm01_overall_well_being',
    'OHM-04': 'ohm04_life_expectancy_at_birth',
    'OHM-08': 'ohm08_respondent_assessed_health_status'
}

def pre_split_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform pre-split cleaning on the dataframe.
    """
    # Drop unnecessary columns and rows
    df = df.drop(columns=['source_file', 'locality'])
    df = df.dropna(subset=['code'])

    # Strip trailing caret (^), asterisk (*), or plus (+) characters from demographic group column
    if 'demographic_group' in df.columns:
        df['demographic_group'] = df['demographic_group'].str.replace(r'[\s\^\*\+]+$', '', regex=True)

    return df

def split_dataframe_by_code(df: pd.DataFrame) -> dict:
    """
    Split the dataframe into multiple dataframes based on the NHIS code column.
    Drop any unnecessary columns or rows.
    Returns a dictionary of dataframes with code as keys.
    """
    # Split the dataframe into a dictionary of dataframes based on the NHIS code
    df_dict = {code: sub_df for code, sub_df in df.groupby('code')}

    for code, df in df_dict.items():
        # Drop unnecessary columns
        df = df.dropna(axis=1, how='all')

        # Try to convert period column to int
        if 'period' in df.columns:
            df.loc[:, 'period'] = pd.to_numeric(df['period'], errors='coerce')

        # Sort columns
        first_cols = ['code', 'title', 'period']
        remaining_cols = [col for col in df.columns if col not in first_cols]
        df = df[first_cols + remaining_cols]

        # Update the dataframe dictionary
        df_dict[code] = df

    print(f'Dataframe split into {len(df_dict)} dataframes based on NHIS code.')

    return df_dict

def run_staging_etl_pipeline(dataset: str) -> None:
    """
    Run the staging NHIS ETL pipeline to fetch data from a raw table, transform, and load it into the staging schema.
    """
    _, table_name = fetch_raw_data_map(dataset=dataset)

    # Generic extraction logic
    df = extract_all_from_raw(table_name=table_name)

    # Generic cleaning logic
    df = clean_column_names(df=df)

    # Dataset-specific transforming logic
    df = pre_split_cleaning(df=df)
    df_dict = split_dataframe_by_code(df=df)

    # Generic loading logic
    for df_name, df in df_dict.items():

        create_and_load_table(
            df=df,
            table_name=TABLE_NAME_MAP.get(df_name, df_name),
            schema='staging',
            if_exists='replace'
        )

        # Update the allowed tables configuration
        update_config_tables(table_name=TABLE_NAME_MAP.get(df_name, df_name), schema='staging')

    print('Staging ETL pipeline completed.')


if __name__ == '__main__':

    DATASET = 'nhis'

    try:
        run_staging_etl_pipeline(dataset=DATASET)

    except Exception as e:
        raise RuntimeError(f'Error during staging ETL pipeline: {e}')
