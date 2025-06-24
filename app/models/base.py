from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now():
    """Função para gerar timestamp UTC atual a cada chamada"""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Base model class for all SQLAlchemy models."""

    __abstract__ = True  # This class is not a table, but a base for other models
    __tablename__ = None  # No table name for the base class

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
