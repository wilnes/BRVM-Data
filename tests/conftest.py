"""
Configuration for all tests
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.stocks import Company
from models.enums import CountryEnum, StatusEnum
from db.base import Base

# Use an in-memory SQLite database for fast tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()  # only rollback if still active
        connection.close()


@pytest.fixture
def company(db):
    company = Company.create(
        db=db,
        company_name="Test company",
        country=CountryEnum.COTE_D_IVOIRE,
        status=StatusEnum.ACTIVE,
    )
    return company
