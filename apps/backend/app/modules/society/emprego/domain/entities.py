"""Compatibility export for legacy imports."""
from app.modules.society.emprego.domain.models import Candidato
DomainEntity = Candidato
__all__ = ['DomainEntity', 'Candidato']