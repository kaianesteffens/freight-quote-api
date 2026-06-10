from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuoteRequest(BaseModel):
    origin: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    weight_kg: float = Field(gt=0)
    volume_m3: float = Field(gt=0)


class QuoteOptionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    carrier: str
    price: float
    delivery_days: int


class QuotePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    origin: str
    destination: str
    weight_kg: float
    volume_m3: float
    created_at: datetime
    options: list[QuoteOptionPublic]
