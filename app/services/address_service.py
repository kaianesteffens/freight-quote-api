from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressUpdate


def list_addresses(db: Session, user: User) -> list[Address]:
    return list(
        db.scalars(
            select(Address).where(Address.user_id == user.id).order_by(Address.id)
        )
    )


def get_address(db: Session, user: User, address_id: int) -> Address:
    address = db.get(Address, address_id)
    if address is None or address.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    return address


def create_address(db: Session, user: User, payload: AddressCreate) -> Address:
    address = Address(user_id=user.id, **payload.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(
    db: Session, user: User, address_id: int, payload: AddressUpdate
) -> Address:
    address = get_address(db, user, address_id)
    for field, value in payload.model_dump().items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, user: User, address_id: int) -> None:
    address = get_address(db, user, address_id)
    db.delete(address)
    db.commit()
