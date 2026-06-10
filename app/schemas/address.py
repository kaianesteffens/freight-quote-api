from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=255)
    number: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=1, max_length=120)
    zip_code: str = Field(min_length=1, max_length=20)
    country: str = Field(min_length=1, max_length=120)


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressPublic(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
