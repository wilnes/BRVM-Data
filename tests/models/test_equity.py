"""Test equity model"""

import pytest
from datetime import date
from models.stocks import Equity
from models.enums import TradingStatusEnum


def test_create_equity_success(db, company):
    equity = Equity.create(
        db,
        company_id=company.company_id,
        ticker="SGBI",
        isin="CI0000000600",
        listing_date=date(2020, 1, 15),
    )

    assert equity.equity_id is not None
    assert equity.company_id == company.company_id
    assert equity.ticker == "SGBI"
    assert equity.isin == "CI0000000600"
    assert equity.trading_status == TradingStatusEnum.ACTIVE
    assert equity.created_at is not None
    assert equity.updated_at is not None


def test_create_equity_missing_fields(db, company):
    with pytest.raises(ValueError, match="Missing required fields"):
        Equity.create(
            db,
            company_id=company.company_id,
            ticker="SGBI",
        )


def test_create_equity_duplicate_ticker(db, company):
    Equity.create(
        db,
        company_id=company.company_id,
        ticker="SGBI",
        isin="CI0000000600",
    )

    with pytest.raises(ValueError, match="Ticker already exists"):
        Equity.create(
            db,
            company_id=company.company_id,
            ticker="SGBI",
            isin="CI0000000601",
        )


def test_create_equity_duplicate_isin(db, company):
    Equity.create(
        db,
        company_id=company.company_id,
        ticker="SGBI",
        isin="CI0000000600",
    )

    with pytest.raises(ValueError, match="ISIN already exists"):
        Equity.create(
            db,
            company_id=company.company_id,
            ticker="SGBI2",
            isin="CI0000000600",
        )
