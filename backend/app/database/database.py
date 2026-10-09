from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from AI_Lecture_Assistant.backend.app.config.settings import settings

# Create the SQLAlchemy engine
engine = create_engine(
    settings.database.url,
    echo=settings.app.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database.url else {}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
Base = declarative_base()
