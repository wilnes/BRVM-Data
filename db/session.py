"""
DB session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings

# Settings
settings = get_settings()

engine = create_engine(
    url=settings.POSTGRESQL_DATABASE_URI,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
