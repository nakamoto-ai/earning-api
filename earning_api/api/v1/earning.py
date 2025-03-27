import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from earning_api.core.auth import verify_token
from earning_api.core.dependencies import get_db
from earning_api.db.database import Database
from earning_api.models.earning import Earning, EarningList
from earning_api.services.earning_service import EarningService

earnings_router = APIRouter()
logger = logging.getLogger(__name__)


@earnings_router.post("/earnings",
                      status_code=201,
                      dependencies=[Depends(verify_token)])
async def add_earnings(earning_list: EarningList,
                       db: Database = Depends(get_db)):
    """Add a list of earnings."""
    try:
        service = EarningService(db)
        added_count = service.add_earning(earning_list)
        logger.info(f"Added {added_count} earnings to the database")
        return {"message": f"Successfully added {added_count} earnings"}
    except Exception as e:
        logger.error(f"Error adding earnings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


SINCE_DATE_QUERY: Optional[str] = Query(
    None,
    description=
    "Optional timestamp to filter entities after this data. Format: YYYY-MM-DD"
)


@earnings_router.get("/earnings", response_model=list[Earning])
async def get_earnings(
        since: Optional[str] = SINCE_DATE_QUERY,
        db: Database = Depends(get_db),
):
    """Retrieve all earnings."""
    try:
        service = EarningService(db)
        earnings = service.get_earning(since)
        logger.info(f"Retrieved {len(earnings)} earnings")
        return earnings
    except Exception as e:
        logger.error(f"Error retrieving earnings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
