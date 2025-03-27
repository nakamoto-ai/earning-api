import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from earning_api.core.auth import verify_token
from earning_api.core.dependencies import get_db
from earning_api.db.database import Database
from earning_api.models.earning import Earning, EarningList
from earning_api.models.people import PeopleList, Person
from earning_api.services.earning_service import EarningService
from earning_api.services.people_service import PeopleService

people_router = APIRouter()
logger = logging.getLogger(__name__)


@people_router.post("/people",
                    status_code=201,
                    dependencies=[Depends(verify_token)])
async def add_people(people_list: PeopleList, db: Database = Depends(get_db)):
    """Add a list of people."""
    try:
        service = PeopleService(db)
        added_count = service.add_people(people_list)
        logger.info(f"Added {added_count} people to the database")
        return {"message": f"Successfully added {added_count} people"}
    except Exception as e:
        logger.error(f"Error adding people: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@people_router.get("/people", response_model=list[Person])
async def get_people(db: Database = Depends(get_db)):
    """Retrieve all people."""
    try:
        service = PeopleService(db)
        people = service.get_people()
        logger.info(f"Retrieved {len(people)} people")
        return people
    except Exception as e:
        logger.error(f"Error retrieving people: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
