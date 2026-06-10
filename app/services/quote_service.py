from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.quote import Quote, QuoteOption
from app.models.user import User
from app.schemas.quote import QuoteRequest

settings = get_settings()

CARRIERS = [
    {"name": "Express", "base_days": 2, "weight_factor": 1.6, "volume_factor": 1.4},
    {"name": "Standard", "base_days": 5, "weight_factor": 1.0, "volume_factor": 1.0},
    {"name": "Economy", "base_days": 9, "weight_factor": 0.7, "volume_factor": 0.8},
]


def _distance_units(origin: str, destination: str) -> int:
    key = f"{origin.strip().lower()}->{destination.strip().lower()}"
    return sum(ord(char) for char in key) % 50 + 1


def calculate_options(request: QuoteRequest) -> list[dict]:
    distance = _distance_units(request.origin, request.destination)
    distance_multiplier = 1 + distance * settings.freight_distance_factor / 100

    options = []
    for carrier in CARRIERS:
        price = (
            settings.freight_base_price
            + settings.freight_price_per_kg * request.weight_kg * carrier["weight_factor"]
            + settings.freight_price_per_m3 * request.volume_m3 * carrier["volume_factor"]
        ) * distance_multiplier
        delivery_days = carrier["base_days"] + distance // 10
        options.append(
            {
                "carrier": carrier["name"],
                "price": round(price, 2),
                "delivery_days": int(delivery_days),
            }
        )
    return options


def create_quote(db: Session, user: User, request: QuoteRequest) -> Quote:
    quote = Quote(
        user_id=user.id,
        origin=request.origin,
        destination=request.destination,
        weight_kg=request.weight_kg,
        volume_m3=request.volume_m3,
        options=[QuoteOption(**option) for option in calculate_options(request)],
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def list_quotes(db: Session, user: User) -> list[Quote]:
    return list(
        db.scalars(
            select(Quote)
            .where(Quote.user_id == user.id)
            .order_by(Quote.created_at.desc(), Quote.id.desc())
        )
    )
