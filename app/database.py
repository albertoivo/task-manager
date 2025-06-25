import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker

from app.models.base import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Configure connect_args based on database type
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create all tables in the database
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[session.Session, None, None]:
    """Dependency to get a database session."""
    db: session.Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
