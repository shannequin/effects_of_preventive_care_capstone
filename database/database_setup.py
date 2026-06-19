from connection import get_db_connection
from sqlalchemy import text


def create_schemas(conn) -> None:
    """
    Create database schemas if they do not already exist.
    """
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))

def create_tables(conn) -> None:
    """
    Create database tables if they do not already exist.
    """
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS raw.customers (
            raw_id BIGSERIAL PRIMARY KEY,
            source_file TEXT,
            ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            payload JSONB NOT NULL
        )
    """))
    
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit.ingestion_log (
            ingestion_id BIGSERIAL PRIMARY KEY,
            source_name TEXT NOT NULL,
            started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMPTZ,
            status TEXT NOT NULL
        )
    """))

def setup_database() -> None:
    """
    Create all required schemas and tables.
    """
    engine = get_db_connection()

    with engine.begin() as conn:
        create_schemas(conn)
        # create_tables(conn)

    print("Database setup completed")


if __name__ == "__main__":
    setup_database()