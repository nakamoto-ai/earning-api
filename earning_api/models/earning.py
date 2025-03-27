from typing import List

from pydantic import BaseModel, Field


class EarningBase(BaseModel):
    people_id: int = Field(..., description="ID of the person")
    tao_earned: float = Field(..., description="Tao earned")
    tao_price: float = Field(..., description="Price of tao")


class Earning(EarningBase):
    id: int = Field(..., description="Unique identifier")
    created_at: str = Field(..., description="Timestamp of creation")

    class Config:
        from_attributes = True  # Allow mapping from SQLite Row objects


class EarningList(BaseModel):
    earnings: List[EarningBase]
