from fastapi import APIRouter

router = APIRouter()

@router.get("/tasks")
def list_tasks():
    return {"tasks": []}
