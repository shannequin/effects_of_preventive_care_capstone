from connection import get_db_connection
from sqlalchemy import text


def create_schemas(conn) -> None:
    """
    Create database schemas if they do not already exist.
    """
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS raw'))
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS staging'))
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS core'))

if __name__ == '__main__':
    try:
        engine = get_db_connection()

        with engine.begin() as conn:
            # Create schemas
            create_schemas(conn)

    except Exception as e:
        raise RuntimeError(f'Error during database setup: {e}')