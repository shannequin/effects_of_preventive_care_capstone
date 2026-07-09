import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names.
    """
    df = df.copy()

    # Clean the column names
    df.columns = [
        re.sub(r'_+', '_', col)                         # Replace multiple underscores with a single underscore
        .strip('_')                                     # Remove leading or trailing underscores
        for col in (
            df.columns
            .str.strip()                                # Remove leading or trailing spaces
            .str.lower()                                # Change to all lowercase
            .str.replace('%', 'pct', regex=False)       # Replace percent symbols with 'pct'
            .str.replace('&', 'and', regex=False)       # Replace ampersand symbols with 'and'
            .str.replace(r'[^\w]+', '_', regex=True)    # Replace all other spaces and symbols with underscores
        )
    ]

    print(f'Cleaned column names: {df.columns.tolist()}')

    return df

def clean_values(value_list: list) -> list:
    """
    Standardize list of values like column names.
    """
    cleaned_values = []
    for value in value_list:
        print(f'Original value: {value}')
        cleaned_value = (
            re.sub(r'_+', '_', str(value)) # Replace multiple underscores with a single underscore
            .strip('_')                    # Remove leading or trailing underscores
            .strip()                       # Remove leading or trailing spaces
            .lower()                       # Change to all lowercase
            .replace('%', 'pct')           # Replace percent symbols with 'pct'
            .replace('&', 'and')           # Replace ampersand symbols with 'and'
            .replace(r'[^\w]+', '_')       # Replace all other spaces and symbols with underscores
        )
        cleaned_values.append(cleaned_value)

    print(f'Cleaned values: {cleaned_values}')

    return cleaned_values
