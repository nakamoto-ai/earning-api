from typing import List

from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the person")


class Person(PersonBase):
    id: int = Field(..., description="Unique identifier")
    created_at: str = Field(..., description="Timestamp of creation")

    class Config:
        from_attributes = True  # Allow mapping from SQLite Row objects


class PeopleList(BaseModel):
    people: List[PersonBase]
