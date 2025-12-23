"""Test stocks models."""


from models.stocks import Company
from models.enums import CountryEnum, StatusEnum


def test_create_company(db):
    company = Company.create(
        db,
        company_name="Test Company",
        country=CountryEnum.COTE_D_IVOIRE,
    )

    assert company.company_id is not None
    assert company.company_name == "Test Company"
    assert company.country == CountryEnum.COTE_D_IVOIRE
    assert company.status == StatusEnum.ACTIVE
