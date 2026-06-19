from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_db_connection() -> Engine:
    """Creates and returns a SQLAlchemy Engine for the configured database.

    Returns:
        Engine: A SQLAlchemy Engine connected to the PostgreSQL database.

    Raises:
        RuntimeError: If any required environment variable is missing.
    """
    missing = [name for name, val in (
        ("DB_USER", DB_USER),
        ("DB_PASSWORD", DB_PASSWORD),
        ("DB_HOST", DB_HOST),
        ("DB_PORT", DB_PORT),
        ("DB_NAME", DB_NAME),
    ) if not val]

    if missing:
        raise RuntimeError(f"Missing required DB environment variables: {', '.join(missing)}")

    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(connection_string)
