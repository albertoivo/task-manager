from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskServices:
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self) -> List[Task]:
        """List all tasks from database."""
        return self.db.query(Task).all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(**task_data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        task = self.get_task(task_id)
        if task:
            update_data = task_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_task(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False
