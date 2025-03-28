import sys
from typing import List

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_PATH: str = "people_earnings.db"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000
    TOKEN: str = ""
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="List of allowed CORS origins.")

    @field_validator("TOKEN", mode="before")
    def validate_token(cls, v):
        if not v or v == "":
            print("ERROR: TOKEN is not set in the environment or .env file.")
            sys.exit(1)
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(
            "CORS_ORIGIN must be a comma-seperated string or list")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
