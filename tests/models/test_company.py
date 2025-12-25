"""Test company model"""

import pytest
from models.stocks import Company
from models.enums import CountryEnum, StatusEnum


def test_create_company(db):
    """Make sure we can create a company."""
    company = Company.create(
        db=db,
        company_name="Test company",
        country=CountryEnum.COTE_D_IVOIRE,
        status=StatusEnum.ACTIVE,
    )

    assert company.company_id is not None
    assert company.company_name == "Test company"
    assert company.country == CountryEnum.COTE_D_IVOIRE
    assert company.status == StatusEnum.ACTIVE


def test_company_persisted(db):
    """Make sure company is persisted in the database."""
    Company.create(
        db=db,
        company_name="BRVM",
        country=CountryEnum.COTE_D_IVOIRE,
        status=StatusEnum.ACTIVE,
    )

    company = db.query(Company).first()
    assert company is not None
    assert company.company_name == "BRVM"


def test_create_company_without_name_fails(db):
    with pytest.raises(Exception):
        Company.create(
            db=db,
            company_name=None,
            country=CountryEnum.COTE_D_IVOIRE,
            status=StatusEnum.ACTIVE,
        )
