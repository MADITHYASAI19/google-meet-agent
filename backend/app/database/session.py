from typing import Generator
from AI_Lecture_Assistant.backend.app.database.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency function to provide a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
