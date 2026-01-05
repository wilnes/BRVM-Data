"""
Data model for trading days
"""

from datetime import datetime, date
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    ForeignKey,
    Date,
    Enum as SQLEnum,
    func,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped, Session

from db.base_class import Base
from models.enums import StatusEnum


class TradingDay(Base):
    __tablename__ = "trading_days"

    # attributes
    trading_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trading_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    is_open: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    note: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    eod_prices: Mapped[list["EquityEODPrice"]] = relationship(
        "EquityEODPrice", back_populates="trading_day"
    )

    @classmethod
    def create(cls, db: Session, **kwargs):
        """
        Create a trading day if it doesn't exist, return the instance.
        """
        trading_date = kwargs.get("trading_date")
        if trading_date is None:
            raise ValueError("trading_date is required")

        # Try to get existing first
        instance = db.query(cls).filter_by(trading_date=trading_date).first()
        if instance:
            return instance

        # Create new trading day
        trading_day = cls(**kwargs)
        db.add(trading_day)
        db.commit()
        db.refresh(trading_day)
        return trading_day


class EquityEODPrice(Base):
    __tablename__ = "equity_eod_prices"

    # primary key
    eod_price_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # foreign keys
    equity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("equities.equity_id"), nullable=False
    )
    trading_date: Mapped[date] = mapped_column(
        Date, ForeignKey("trading_days.trading_date"), nullable=False
    )

    # price attributes
    open_price: Mapped[float] = mapped_column(Float, nullable=True)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=True)
    low_price: Mapped[float] = mapped_column(Float, nullable=True)
    volume: Mapped[int] = mapped_column(Integer, nullable=True)
    traded_value: Mapped[float] = mapped_column(Float, nullable=True)
    full_data_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    data_source: Mapped[str] = mapped_column(String(255), nullable=True)

    # timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # relationships
    equity: Mapped["Equity"] = relationship(  # type:ignore
        "Equity", back_populates="eod_prices"
    )
    trading_day: Mapped["TradingDay"] = relationship(
        "TradingDay", back_populates="eod_prices"
    )

    @classmethod
    def create(cls, db: Session, **kwargs):
        """
        Create a new EOD price if it doesn't exist. Returns the instance.
        """
        equity_id = kwargs.get("equity_id")
        trading_date = kwargs.get("trading_date")

        if equity_id is None or trading_date is None:
            raise ValueError("Both 'equity_id' and 'trading_date' are required")

        existing = (
            db.query(cls)
            .filter_by(equity_id=equity_id, trading_date=trading_date)
            .first()
        )
        if existing:
            raise ValueError(
                f"EOD price for equity_id '{equity_id}' on date '{trading_date}' already exists"
            )

        # Create new record
        eod_price = cls(**kwargs)
        db.add(eod_price)
        db.commit()
        db.refresh(eod_price)
        return eod_price
