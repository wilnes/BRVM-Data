"""
Configuration for all tests
"""

import os
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from db.base import Base


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """
    Ensure test environment variables are set BEFORE settings are loaded
    """
    os.environ["ENV"] = "test"
    os.environ["SQLITE_DB"] = "test.db"
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(scope="session")
def engine():
    """
    Create a SQLite engine for the test session
    """
    engine = create_engine("sqlite:///test.db")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(engine):
    """
    Apply Alembic migrations once for the test database
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    Base.metadata.create_all(bind=engine)  # Create tables
    yield
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture(scope="function")
def db(engine) -> Generator:
    """
    Create a transactional DB session per test
    """
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
