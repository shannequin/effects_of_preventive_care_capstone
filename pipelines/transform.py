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

def create_statistic_type_field(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create statistic type field based on the source_file column.
    """
    # Split the source_file into multiple variables on the underscore
    source_file_split = df['source_file'].str.split('_', expand=True)

    # Create a statistic type field and populate it with source_file_split column 0 (replace dash with space)
    df['statistic_type'] = source_file_split.iloc[:, 0].str.replace("-", " ")

    print("Field created and populated: statistic_type")

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
