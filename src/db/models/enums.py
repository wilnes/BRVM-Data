"""
Enums for models
"""

from enum import Enum


class StatusEnum(Enum, str):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELISTED = "delisted"


class CountryEnum(Enum, str):
    COTE_D_IVOIRE = "Cote d'Ivoire"
