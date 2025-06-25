from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import __description__, __title__, __version__
from app.api import task
from app.database import get_db

from app.core import settings

app = FastAPI(
    title=__title__,
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(task.router)


@app.get("/", tags=["Home"], summary="Initial Route")
def home():
    return {"detail": "Task Manager API running..."}


@app.get("/health", tags=["Home"], summary="Health Check")
def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy", "db_connected": db.is_active}


@app.get("/version", tags=["Home"], summary="API Version")
def version():
    return {"version": __version__, "description": __description__, "title": __title__}

@app.get("/environment", tags=["Home"], summary="Environment Variables")
def environment():
    return {
        "app_name": settings.app_name,
        "redis_url": settings.redis_url,
        "environment": settings.environment,
        "debug": settings.debug
    }
    
