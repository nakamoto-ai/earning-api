from sqlite3 import Connection

from fastapi import Depends

from earning_api.db.database import Database, db


def get_db() -> Database:
    """Dependency to provide the database instance."""
    return db


def get_db_connection(db: Database = Depends(get_db)) -> Connection:
    """Dependency to provide a database connection (optional, for raw SQL usage)."""
    with db.get_connection() as conn:
        yield conn
