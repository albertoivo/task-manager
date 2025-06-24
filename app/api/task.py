from typing import List

from fastapi import APIRouter

from app.schemas.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
def list_tasks():
    return {"tasks": []}
