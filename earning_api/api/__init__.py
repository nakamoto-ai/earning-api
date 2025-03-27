from fastapi import APIRouter
from earning_api.api.v1.earning import earnings_router as v1_earnings_router
from earning_api.api.v1.people import people_router as v1_people_router

# API Version 1
api_v1_router = APIRouter()
api_v1_router.include_router(
    v1_earnings_router,
    prefix="/api/v1",
    tags=["earnings"],
)
api_v1_router.include_router(
    v1_people_router,
    prefix="/api/v1",
    tags=["people"],
)
