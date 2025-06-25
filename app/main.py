from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import __description__, __title__, __version__
from app.api import task
from app.database import get_db

from app.core import settings

from app.core.logging import setup_logging

logger = setup_logging()

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
    logger.info("Home route accessed")
    return {"detail": "Task Manager API running..."}


@app.get("/health", tags=["Home"], summary="Health Check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return {"status": "healthy", "db_connected": True}
    except Exception:
        logger.error("Database connection failed", exc_info=True)
        return {"status": "unhealthy", "db_connected": False}


@app.get("/version", tags=["Home"], summary="API Version")
def version():
    return {"version": __version__, "description": __description__, "title": __title__}

@app.get("/environment", tags=["Home"], summary="Environment Variables")
def environment():
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug
    }
    
