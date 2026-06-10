from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.address import AddressCreate, AddressPublic, AddressUpdate
from app.services import address_service

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("", response_model=list[AddressPublic])
def list_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AddressPublic]:
    return address_service.list_addresses(db, current_user)


@router.post("", response_model=AddressPublic, status_code=status.HTTP_201_CREATED)
def create_address(
    payload: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressPublic:
    return address_service.create_address(db, current_user, payload)


@router.get("/{address_id}", response_model=AddressPublic)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressPublic:
    return address_service.get_address(db, current_user, address_id)


@router.put("/{address_id}", response_model=AddressPublic)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressPublic:
    return address_service.update_address(db, current_user, address_id, payload)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    address_service.delete_address(db, current_user, address_id)
