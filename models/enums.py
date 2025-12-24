"""
Enums for models
"""

from enum import Enum


# ====== Stock-related Enums ======

class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELISTED = "delisted"


class CountryEnum(Enum):
    COTE_D_IVOIRE = "Côte d'Ivoire"
    BENIN = "Bénin"
    BURKINA_FASO = "Burkina Faso"
    GUINEA_BISSAU = "Guinée-Bissau"
    MALI = "Mali"
    NIGER = "Niger"
    SENEGAL = "Sénégal"
    TOGO = "Togo"


class TradingStatusEnum(Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    DELISTED = "Delisted"
