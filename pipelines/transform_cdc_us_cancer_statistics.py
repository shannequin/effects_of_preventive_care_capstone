from database.connection import get_db_connection
from sqlalchemy import text
import pandas as pd

# Connect to the database
engine = get_db_connection()

# Select all records from the raw.cdc_us_cancer_statistics table as a pandas dataframe
with engine.begin() as conn:
    df = pd.read_sql_query(text("SELECT * FROM raw.cdc_us_cancer_statistics"), conn)

sex_map = {
    "male-and-female": "Male and Female",
    "female": "Female",
    "male": "Male"
}

for k, v in sex_map.items():
    mask = (
        df['Sex'].isna()
        & df['source_file'].str.contains(k)
    )

    df.loc[mask, 'Sex'] = v

    print(f"Number of rows to be updated to {v}: {mask.sum()}")
