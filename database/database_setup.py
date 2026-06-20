from connection import get_db_connection
from sqlalchemy import text


def create_schemas(conn) -> None:
    """
    Create database schemas if they do not already exist.
    """
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))

def create_tables(conn, table_name: str) -> None:
    """
    Create database tables if they do not already exist.
    """
    conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS staging.{table_name} (
            raw_id BIGSERIAL PRIMARY KEY,
            source_file TEXT,
            ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            payload JSONB NOT NULL
        )
    """))
    
    conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS core.{table_name} (
            ingestion_id BIGSERIAL PRIMARY KEY,
            source_name TEXT NOT NULL,
            started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMPTZ,
            status TEXT NOT NULL
        )
    """))


if __name__ == "__main__":

    table_name = "" #"cdc_us_cancer_statistics"

    try:
        engine = get_db_connection()

        with engine.begin() as conn:
            create_schemas(conn)

            if table_name:
                create_tables(conn, table_name)

    except Exception as e:
        raise RuntimeError(f"Error during database setup: {e}")