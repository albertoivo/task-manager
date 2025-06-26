from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import TaskPriority, TaskStatus
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate
from app.services.task_services import TaskServices

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# === ENDPOINTS CRUD BÁSICOS ===

@router.get("/", response_model=List[TaskSchema], summary="List all tasks")
def list_tasks(db: Session = Depends(get_db)):
    """List all tasks in the database."""
    task_service = TaskServices(db)
    tasks = task_service.list_tasks()
    return tasks or []


# === ENDPOINTS DE FILTRO - REORDENADOS ===
# Rotas mais específicas primeiro!

@router.get("/overdue", response_model=List[TaskSchema])
def get_overdue_tasks(db: Session = Depends(get_db)):
    """Get all overdue tasks."""
    service = TaskServices(db)
    tasks = service.get_overdue_tasks()
    return tasks


@router.get("/due-soon", response_model=List[TaskSchema])
def get_tasks_due_soon(
    days: int = Query(7, description="Number of days to look ahead"),
    db: Session = Depends(get_db)
):
    """Get tasks due within the next N days."""
    service = TaskServices(db)
    tasks = service.get_tasks_due_soon(days)
    return tasks


@router.get("/due-today", response_model=List[TaskSchema])
def get_tasks_due_today(db: Session = Depends(get_db)):
    """Get tasks due today."""
    service = TaskServices(db)
    tasks = service.get_tasks_due_today()
    return tasks


@router.get("/search", response_model=List[TaskSchema])
def search_tasks(
    q: str = Query(..., description="Search term for title or description"),
    db: Session = Depends(get_db)
):
    """Search tasks by title or description."""
    service = TaskServices(db)
    tasks = service.search_tasks(q)
    return tasks


@router.get("/filter", response_model=List[TaskSchema])
def filter_tasks_advanced(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned person"),
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    db: Session = Depends(get_db)
):
    """Advanced task filtering."""
    service = TaskServices(db)
    tasks = service.filter_tasks_advanced(
        status=status,
        priority=priority,
        assigned_to=assigned_to,
        start_date=start_date,
        end_date=end_date,
        search_term=search
    )
    return tasks


@router.get("/filter/status/{status}", response_model=List[TaskSchema])
def get_tasks_by_status(
    status: TaskStatus,
    db: Session = Depends(get_db)
):
    """Get all tasks with specific status."""
    service = TaskServices(db)
    tasks = service.filter_tasks_by_status(status)
    return tasks


@router.get("/filter/priority/{priority}", response_model=List[TaskSchema])
def get_tasks_by_priority(
    priority: TaskPriority,
    db: Session = Depends(get_db)
):
    """Get all tasks with specific priority."""
    service = TaskServices(db)
    tasks = service.filter_tasks_by_priority(priority)
    return tasks


@router.get("/filter/assigned/{assigned_to}", response_model=List[TaskSchema])
def get_tasks_by_assigned_to(
    assigned_to: str,
    db: Session = Depends(get_db)
):
    """Get all tasks assigned to specific person."""
    service = TaskServices(db)
    tasks = service.filter_tasks_by_assigned_to(assigned_to)
    return tasks


# === ENDPOINTS CRUD BÁSICOS CONTINUAÇÃO ===

@router.get("/{task_id}", response_model=TaskSchema, summary="Get task by ID")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task_service = TaskServices(db)
    task = task_service.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED, summary="Create new task")
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    task_service = TaskServices(db)
    task = task_service.create_task(task_data)
    return task


@router.put("/{task_id}", response_model=TaskSchema, summary="Update task")
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task."""
    task_service = TaskServices(db)
    task = task_service.update_task(task_id, task_data)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task_service = TaskServices(db)
    success = task_service.delete_task(task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return None  # 204 No Content não retorna body
