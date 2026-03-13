"""Compatibility export for legacy imports."""
from app.modules.society.seguranca_social.domain.models import Beneficiario
DomainEntity = Beneficiario
__all__ = ['DomainEntity', 'Beneficiario']