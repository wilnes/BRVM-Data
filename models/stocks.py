"""
Data model for stocks
"""

from datetime import datetime, date
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Date,
    Enum as SQLEnum,
    func,
    DateTime,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped, Session
from sqlalchemy.exc import IntegrityError
from db.base_class import Base
from models.enums import CountryEnum, StatusEnum, TradingStatusEnum


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
    # relationships
    equities: Mapped[list["Equity"]] = relationship("Equity", back_populates="company")

    @classmethod
    def create(cls, db: Session, **kwargs):
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


class Equity(Base):
    __tablename__ = "equities"

    equity_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.company_id"), nullable=False
    )
    ticker: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    isin: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    listing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    trading_status: Mapped[TradingStatusEnum] = mapped_column(
        SQLEnum(TradingStatusEnum), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    company: Mapped["Company"] = relationship("Company", back_populates="equities")
    eod_prices: Mapped[list["EquityEODPrice"]] = relationship(  # type:ignore
        "EquityEODPrice", back_populates="equity"
    )

    @classmethod
    def create(cls, db: Session, **kwargs):
        # Ensure required fileds are present
        required_fields = {"company_id", "ticker", "isin"}
        missing = required_fields - kwargs.keys()
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        # Default trading status
        kwargs.setdefault("trading_status", TradingStatusEnum.ACTIVE)

        # validate company exists
        company_id = kwargs.get("company_id")
        company = db.query(Company).filter_by(company_id=company_id).first()
        if not company:
            raise ValueError(f"Company with ID '{company_id}' does not exist")

        # Optional: proactive uniqueness checks
        if db.query(cls).filter_by(ticker=kwargs["ticker"]).first():
            raise ValueError("Ticker already exists")

        if db.query(cls).filter_by(isin=kwargs["isin"]).first():
            raise ValueError("ISIN already exists")

        equity = cls(**kwargs)
        db.add(equity)

        # create new equity
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Equity violates a database constraint")

        db.refresh(equity)
        return equity
