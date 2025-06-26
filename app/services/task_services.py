from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.enums import TaskPriority, TaskStatus
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

    def filter_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Filter tasks by status."""
        return self.db.query(Task).filter(Task.status == status.value).all()

    def filter_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Filter tasks by priority."""
        return self.db.query(Task).filter(Task.priority == priority.value).all()

    def filter_tasks_by_assigned_to(self, assigned_to: str) -> List[Task]:
        """Filter tasks by assigned person."""
        return self.db.query(Task).filter(Task.assigned_to == assigned_to).all()

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks (due_date < today and status != completed)."""
        # Usar apenas a data (sem horário) para comparação
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())  # 00:00:00 de hoje

        return (
            self.db.query(Task)
            .filter(
                and_(
                    Task.due_date < today_start,  # Antes de hoje (00:00:00)
                    Task.status != TaskStatus.COMPLETED.value,
                )
            )
            .all()
        )

    def get_tasks_due_soon(self, days: int = 7) -> List[Task]:
        """Get tasks due within the next N days."""
        now = datetime.now()
        future_date = now + timedelta(days=days)
        return (
            self.db.query(Task)
            .filter(
                and_(
                    Task.due_date.between(now, future_date),
                    Task.status != TaskStatus.COMPLETED.value,
                )
            )
            .all()
        )

    def get_tasks_due_today(self) -> List[Task]:
        """Get tasks due today."""
        today = datetime.now().date()
        return (
            self.db.query(Task)
            .filter(
                and_(
                    Task.due_date >= datetime.combine(today, datetime.min.time()),
                    Task.due_date
                    < datetime.combine(today + timedelta(days=1), datetime.min.time()),
                    Task.status != TaskStatus.COMPLETED.value,
                )
            )
            .all()
        )

    def filter_tasks_by_date_range(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Task]:
        """Filter tasks by date range."""
        query = self.db.query(Task)

        if start_date:
            query = query.filter(Task.due_date >= start_date)
        if end_date:
            query = query.filter(Task.due_date <= end_date)

        return query.all()

    def search_tasks(self, search_term: str) -> List[Task]:
        """Search tasks by title or description."""
        search_pattern = f"%{search_term}%"
        return (
            self.db.query(Task)
            .filter(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern),
                )
            )
            .all()
        )

    def filter_tasks_advanced(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assigned_to: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search_term: Optional[str] = None,
    ) -> List[Task]:
        """Advanced filtering with multiple criteria."""
        query = self.db.query(Task)

        if status:
            query = query.filter(Task.status == status.value)
        if priority:
            query = query.filter(Task.priority == priority.value)
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        if start_date:
            query = query.filter(Task.due_date >= start_date)
        if end_date:
            query = query.filter(Task.due_date <= end_date)
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern),
                )
            )

        return query.all()
