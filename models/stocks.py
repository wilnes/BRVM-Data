"""
Data model for stocks
"""

from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship, mapped_column
from db.base_class import Base
from models.enums import CountryEnum, StatusEnum


class Company(Base):
    __tablename__ = "company"

    # attributes
    company_id: int = mapped_column(Integer, primary_key=True)
    company_name: str = mapped_column(String(255), nullable=False)
    country: CountryEnum = mapped_column(SQLEnum(CountryEnum), nullable=False)
    status: StatusEnum = mapped_column(SQLEnum(StatusEnum), nullable=False)
    created_at: datetime = mapped_column()
    updated_at: datetime = mapped_column()

    # relationships
    equities = relationship("Equity", back_populates="company")


class Equity(Base):
    __tablename__ = "equity"

    equity_id: int = mapped_column(Integer, primary_key=True)
    company_id: int = mapped_column(
        ForeignKey("company.company_id"), nullable=False)
    ticker: str = mapped_column(String(50), nullable=False, unique=True)
    isin: str = mapped_column(String(50))
    listing_date: Date = mapped_column(Date)
    trading_status: str = mapped_column(String(50))
    # created_at = mapped_column(TIMESTAMP)

    company = relationship("Company", back_populates="equities")
