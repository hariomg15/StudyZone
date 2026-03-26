from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL=settings.database_url

# Handle SQLite's threading restrictions
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine=create_engine(DATABASE_URL, echo=settings.debug, **engine_kwargs)

Sessionlocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
