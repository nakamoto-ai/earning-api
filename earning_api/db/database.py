from contextlib import contextmanager
import logging
import sqlite3

from earning_api.core.config import settings

logger = logging.getLogger(__name__)


class Database:
    """Database class to manage SQLite connections and operations."""

    def __init__(self, db_path: str = settings.DATABASE_PATH):
        """Initialize with database path."""
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self):
        """Initialize the database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS earnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    people_id INTEGER NOT NULL,
                    tao_earned REAL NOT NULL,
                    tao_price REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (people_id) REFERENCES people (id) ON DELETE CASCADE
                )               
            """)
            conn.commit()
            logger.info("Database schema initialized")

    @contextmanager
    def get_connection(self):
        """Provide a database connection with proper cleanup and foreign key enforcement."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a non-returning query (e.g., INSERT, UPDATE)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict]:
        """Fetch all rows from a query."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query: str, params: tuple = ()) -> dict | None:
        """Fetch one row from a query."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None


db = Database()
