from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import TaskPriority, TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        CheckConstraint(
            f"status IN ({', '.join([f"'{status.value}'" for status in TaskStatus])})",
            name="check_status_values",
        ),
        CheckConstraint(
            f"priority IN ({', '.join([f"'{priority.value}'" for priority in TaskPriority])})",
            name="check_priority_values",
        ),
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default=TaskStatus.PENDING.value
    )
    priority: Mapped[str] = mapped_column(
        String(50), nullable=False, default=TaskPriority.MEDIUM.value
    )
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    assigned_to: Mapped[str] = mapped_column(String(100), nullable=True)
    tags: Mapped[str] = mapped_column(String(500), nullable=True, default="[]")
