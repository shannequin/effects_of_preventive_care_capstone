import pandas as pd
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names using lowercase snake_case.
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
