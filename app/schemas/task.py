from pydantic import BaseModel, ConfigDict, field_validator

from app.models.enums import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: str | None = None
    assigned_to: str | None = None
    tags: list[str] | None = None

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
        use_enum_values = True
        anystr_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 500
