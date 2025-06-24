from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    __abstract__ = True  # This class is not a table, but a base for other models
    __tablename__ = None  # No table name for the base class

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[str] = mapped_column(
        String(50), nullable=False, default="CURRENT_TIMESTAMP"
    )
    updated_at: Mapped[str] = mapped_column(
        String(50), nullable=False, on_update="CURRENT_TIMESTAMP"
    )
