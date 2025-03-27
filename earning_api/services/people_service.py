import logging
import sqlite3

from earning_api.db.database import Database
from earning_api.models.people import PeopleList, Person

logger = logging.getLogger(__name__)


class PeopleService:

    def __init__(self, db: Database):
        self.db = db

    def add_people(self, people_list: PeopleList) -> int:
        """Add a list of people to the database."""
        added_count = 0
        for person in people_list.people:
            try:
                self.db.execute("INSERT INTO people (name) VALUES (?)",
                                (person.name, ))
                added_count += 1
            except sqlite3.IntegrityError:
                logger.warning(f"Duplicate name skipped: {person.name}")
                continue  # Skip duplicates
        return added_count

    def get_people(self) -> list[Person]:
        """Retrieve all people from the database."""
        rows = self.db.fetch_all("SELECT id, name, created_at FROM people")
        return [Person(**row) for row in rows]
