import json
import pandas as pd

from database.connection import get_db_connection


def create_and_load_table(df: pd.DataFrame, table_name: str, schema: str, if_exists: str) -> None:
    """
    Create or replace a table in the raw schema of the database.
    """
    engine = get_db_connection()

    with engine.begin() as conn:
        df.to_sql(
            name=table_name,
            con=conn,
            schema=schema,
            if_exists=if_exists,
            index=False
        )

    print(f"Table '{schema}.{table_name}' created with {len(df)} records.")

def update_config_tables(table_name: str, schema: str) -> None:
    """
    Update the configuration file to include the new table name in the list of allowed tables.
    """
    config_path = "config/allowed_tables.json"

    with open(config_path, "r") as f:
        tables_config = json.load(f)

    # Fetch the tables for the given schema
    allowed_tables = tables_config[f"ALLOWED_{schema.upper()}_TABLES"]

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
