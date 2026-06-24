import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names using lowercase snake_case.
    """
    df = df.copy()

    df.columns = [
        re.sub(r"_+", "_", col)          # replace multiple underscores with one
        .strip("_")                      # remove leading/trailing underscores
        for col in (
            df.columns
            .str.strip()                 # remove leading/trailing spaces
            .str.lower()                 # lowercase
            .str.replace("%", "pct", regex=False)
            .str.replace("&", "and", regex=False)
            .str.replace(r"[^\w]+", "_", regex=True)  # replace spaces/symbols
        )
    ]

    print(f"Cleaned column names: {df.columns.tolist()}")

    return df

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

    return df

def fill_missing_sex_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in the sex column based on the source_file column.
    """
    df = df.copy()

    # Create a mapping of source_file patterns
    sex_map = {
        "male-and-female": "Male and Female",
        "female": "Female",
        "male": "Male"
    }

    # Loop through the mapping and fill missing values
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
    Returns a dictionary of dataframes with statistic_type as keys.
    """
    df_dict = {"_".join(stat_type.split()).lower(): sub_df for stat_type, sub_df in df.groupby('statistic_type')}

    print(f"Dataframe split into {len(df_dict)} dataframes based on statistic_type.")

    return df_dict

def create_cancer_type_field(df_dict: dict) -> dict:
    """
    Create and clean the cancer_type field based on the source_file column for each dataframe in the dictionary.
    """
    # For each dataframe, split the source_file into multiple variables on the underscore and create a cancer_type field
    for stat_type, df in df_dict.items():
        source_file_split = df['source_file'].str.split('_', expand=True)

        # For each split, resolve which index contains the cancer type versus unnecessary information. Most cancer types are in index 2, but some are index 1.
        if source_file_split.shape[1] > 2:
            df['cancer_type'] = source_file_split.iloc[:, 2].str.replace("-", " ")
        else:
            df['cancer_type'] = source_file_split.iloc[:, 1].str.replace("-", " ")

        print(f"Field created and populated: cancer_type for statistic_type '{stat_type}'")

