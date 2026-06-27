import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names using lowercase snake_case.
    """
    # Create a copy of the dataframe
    df = df.copy()

    # Clean the column names
    df.columns = [
        re.sub(r"_+", "_", col)                         # Replace multiple underscores with a single underscore
        .strip("_")                                     # Remove leading or trailing underscores
        for col in (
            df.columns
            .str.strip()                                # Remove leading or trailing spaces
            .str.lower()                                # Change to all lowercase
            .str.replace("%", "pct", regex=False)       # Replace percent symbols with 'pct'
            .str.replace("&", "and", regex=False)       # Replace ampersand symbols with 'and'
            .str.replace(r"[^\w]+", "_", regex=True)    # Replace all other spaces and symbols with underscores
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
    # Create a copy of the dataframe
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
