from fastapi import FastAPI

from earning_api.api import api_v1_router
from earning_api.core.logging import setup_logging
from earning_api.core.config import settings

app = FastAPI(
    title="People Earnings API",
    description="API to manage people and their earnings",
    version="1.0.0",
)

setup_logging()

app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Earnings API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("earning_api.main:app",
                host="0.0.0.0",
                port=settings.PORT,
                reload=True)
