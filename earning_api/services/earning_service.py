from datetime import datetime
import logging
import sqlite3
from typing import Optional

from fastapi import HTTPException

from earning_api.db.database import Database
from earning_api.models.earning import Earning, EarningList

logger = logging.getLogger(__name__)


class EarningService:

    def __init__(self, db: Database):
        self.db = db

    def add_earning(self, earning_list: EarningList) -> int:
        """Add a list of earnings to the database."""
        added_count = 0
        for earning in earning_list.earnings:
            try:
                self.db.execute(
                    "INSERT INTO earnings (people_id, tao_earned, tao_price) VALUES (?, ?, ?)",
                    (earning.people_id, earning.tao_earned, earning.tao_price))
                added_count += 1
            except sqlite3.IntegrityError:
                logger.warning(
                    "Unexpected IntegrityError: Error in Database Logic")
                continue
        return added_count

    def get_earning(self, since: Optional[str] = None) -> list[Earning]:
        """Retrieve all earnings from the database."""
        if since:
            try:
                datetime.strptime(since, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400,
                                    detail="Invalid timestamp format")

            query = """
                SELECT id, people_id, tao_earned, tao_price, created_at
                FROM earnings
                WHERE created_at >= ?
            """
            params = (since, )
        else:
            query = """
                SELECT id, people_id, tao_earned, tao_price, created_at
                FROM earnings
            """
            params = ()

        rows = self.db.fetch_all(query, params)
        return [Earning(**row) for row in rows]
