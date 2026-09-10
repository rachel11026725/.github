"""
Database connection utility.

Provides a simple interface to connect to a SQLite database (default)
or any database supported by SQLAlchemy (PostgreSQL, MySQL, etc.).
"""

import sqlite3
import os


def get_connection(db_url=None):
    """
    Return a database connection.

    If db_url is provided, it is used as the connection string for
    databases supported by SQLAlchemy (e.g. postgresql://user:pass@host/db).
    SQLAlchemy must be installed for non-SQLite databases:
        pip install sqlalchemy

    Otherwise, falls back to SQLite using the path in the DB_PATH
    environment variable (default: database.db).

    Args:
        db_url (str, optional): Database connection URL.

    Returns:
        connection: A database connection object.  For SQLAlchemy-backed
            connections the returned object is a
            ``sqlalchemy.engine.Connection`` whose underlying engine can be
            accessed via ``connection.engine`` and disposed with
            ``connection.engine.dispose()``.
    """
    if db_url:
        try:
            from sqlalchemy import create_engine
            import sqlalchemy.exc as sa_exc
        except ImportError:
            raise ImportError(
                "SQLAlchemy is required for non-SQLite databases. "
                "Install it with: pip install sqlalchemy"
            )
        try:
            engine = create_engine(db_url)
            return engine.connect()
        except sa_exc.ArgumentError as exc:
            raise ValueError(f"Invalid database URL '{db_url}': {exc}") from exc
        except sa_exc.OperationalError as exc:
            raise ConnectionError(
                f"Could not connect to database at '{db_url}': {exc}"
            ) from exc

    db_path = os.environ.get("DB_PATH", "database.db")
    try:
        return sqlite3.connect(db_path)
    except sqlite3.OperationalError as exc:
        raise ConnectionError(
            f"Could not connect to SQLite database at '{db_path}': {exc}"
        ) from exc


def close_connection(conn):
    """
    Close the given database connection.

    For SQLAlchemy connections the underlying engine is also disposed so
    that all pooled resources are released.
    """
    if conn is None:
        return
    conn.close()
    if hasattr(conn, "engine"):
        conn.engine.dispose()


if __name__ == "__main__":
    conn = get_connection()
    print("Connected to database successfully.")
    close_connection(conn)
    print("Connection closed.")
