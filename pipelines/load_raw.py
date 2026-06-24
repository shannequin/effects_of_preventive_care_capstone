import json
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

    print(f"Table 'raw.{table_name}' created with {len(df)} records.")

    # Append the table name to the list of allowed raw tables
    config_path = "config/tables.json"

    # Read the existing configuration
    with open(config_path, "r") as f:
        tables_config = json.load(f)

    allowed_tables = tables_config["ALLOWED_RAW_TABLES"]

    # Validate if the table name is already in the allowed list
    if table_name in allowed_tables:
        print(f"Table '{table_name}' already exists in the allowed list.")
    
    else:
        # Append the new table name to the allowed list and sort it
        allowed_tables.append(table_name)
        allowed_tables.sort()

        # Update the configuration file with the new allowed list
        with open(config_path, "w") as f:
            json.dump(tables_config, f, indent=4)

        print(f"Table '{table_name}' added to the allowed list.")