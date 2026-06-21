import pandas as pd
from database.connection import get_db_connection


def create_raw_table_from_df(df: pd.DataFrame, table_name: str) -> None:
    """
    Create a new table in the database raw schema.
    If the table already exists, it will be overwritten.
    """
    engine = get_db_connection()

    with engine.begin() as conn:
        df.to_sql(
            name=table_name,
            con=conn,
            schema="raw",
            if_exists="replace",
            index=False
        )