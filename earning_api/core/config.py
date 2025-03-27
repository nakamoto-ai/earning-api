import sys

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_PATH: str = "people_earnings.db"
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000
    TOKEN: str = ""

    @field_validator("TOKEN", mode="before")
    def validate_token(cls, v):
        if not v or v == "":
            print("ERROR: TOKEN is not set in the environment or .env file.")
            sys.exit(1)
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
