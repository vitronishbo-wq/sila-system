"""Entities do Domínio de Contribuintes."""

from .taxpayer import Taxpayer
from .taxpayer_certificate import TaxpayerCertificate
from .taxpayer_debt import TaxpayerDebt

__all__ = ["Taxpayer", "TaxpayerCertificate", "TaxpayerDebt"]
