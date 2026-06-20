from database.connection import get_db_connection
from sqlalchemy import text
import pandas as pd

# Connect to the database
engine = get_db_connection()

# Select all records from the raw.cdc_us_cancer_statistics table as a pandas dataframe
with engine.begin() as conn:
    df = pd.read_sql_query(text("SELECT * FROM raw.cdc_us_cancer_statistics"), conn)

# Fill missing Sex values based on source_file name patterns
print(df['Sex'].value_counts())

mask = (
    df['Sex'].isna()
    & df['source_file'].str.contains("male-and-female")
)

print(f"Number of rows to be updated to Male and Female: {mask.sum()}")

df.loc[mask, 'Sex'] = "Male and Female"

mask = (
    df['Sex'].isna()
    & df['source_file'].str.contains("female")
)
print(f"Number of rows to be updated to Female: {mask.sum()}")

df.loc[mask, 'Sex'] = "Female"

mask = (
    df['Sex'].isna()
    & df['source_file'].str.contains("male")
)
print(f"Number of rows to be updated to Male: {mask.sum()}")

df.loc[mask, 'Sex'] = "Male"

print(df['Sex'].value_counts())