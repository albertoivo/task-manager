from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.enums import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()

    @field_validator("status")
    def validate_status(cls, value: TaskStatus) -> TaskStatus:
        if value not in TaskStatus:
            raise ValueError(f"Invalid status: {value}")
        return value

    @field_validator("priority")
    def validate_priority(cls, value: TaskPriority) -> TaskPriority:
        if value not in TaskPriority:
            raise ValueError(f"Invalid priority: {value}")
        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        str_min_length=1,
        str_max_length=500,
    )
