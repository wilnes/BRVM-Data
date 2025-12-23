"""
Data model for stocks
"""

from datetime import datetime
from sqlalchemy import (Integer, String, ForeignKey,
                        Date, Enum as SQLEnum, func, DateTime)
from sqlalchemy.orm import relationship, mapped_column, Mapped, Session
from db.base_class import Base
from models.enums import CountryEnum, StatusEnum


class Company(Base):
    __tablename__ = "companies"

    # attributes
    company_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[CountryEnum] = mapped_column(
        SQLEnum(CountryEnum), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        SQLEnum(StatusEnum), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(),
        nullable=False
    )

    @classmethod
    def create(cls, db: Session,  **kwargs):
        # check if company with same name exists
        company_name = kwargs.get("company_name")
        existing = db.query(cls).filter_by(company_name=company_name).first()
        if existing:
            raise ValueError(
                f"Company with name '{company_name}' already exists")

        # add status to kwargs if not provided
        if "status" not in kwargs:
            kwargs["status"] = StatusEnum.ACTIVE

        # create new company
        company = cls(**kwargs)
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    # relationships
    equities = relationship("Equity", back_populates="company")


class Equity(Base):
    __tablename__ = "equities"

    equity_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.company_id"), nullable=False)
    ticker: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    isin: Mapped[str] = mapped_column(String(50))
    listing_date: Mapped[Date] = mapped_column(Date)
    trading_status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(),
        nullable=False
    )

    company = relationship("Company", back_populates="equities")
