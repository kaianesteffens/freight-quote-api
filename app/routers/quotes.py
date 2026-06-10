from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.quote import QuotePublic, QuoteRequest
from app.services import quote_service

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("", response_model=QuotePublic, status_code=status.HTTP_201_CREATED)
def create_quote(
    payload: QuoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuotePublic:
    return quote_service.create_quote(db, current_user, payload)


@router.get("", response_model=list[QuotePublic])
def list_quotes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[QuotePublic]:
    return quote_service.list_quotes(db, current_user)
