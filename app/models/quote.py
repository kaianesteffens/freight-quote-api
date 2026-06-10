from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    weight_kg: Mapped[float] = mapped_column(Float)
    volume_m3: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="quotes")
    options: Mapped[list["QuoteOption"]] = relationship(
        back_populates="quote", cascade="all, delete-orphan"
    )


class QuoteOption(Base):
    __tablename__ = "quote_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    quote_id: Mapped[int] = mapped_column(ForeignKey("quotes.id"), index=True)
    carrier: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    delivery_days: Mapped[int] = mapped_column(Integer)

    quote: Mapped["Quote"] = relationship(back_populates="options")


from app.models.user import User  # noqa: E402
