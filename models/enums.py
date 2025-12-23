"""
Enums for models
"""

from enum import Enum


class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELISTED = "delisted"


class CountryEnum(Enum):
    COTE_D_IVOIRE = "Cote d'Ivoire"
