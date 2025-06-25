from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import Task
from app.services.task_services import TaskServices

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[Task], summary="List all tasks")
def list_tasks(db: Session = Depends(get_db)):
    """List all tasks in the database."""
    task_service = TaskServices(db)
    tasks = task_service.list_tasks()
    return tasks or []
