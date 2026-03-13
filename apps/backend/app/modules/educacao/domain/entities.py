"""Compatibility export for legacy imports."""
from app.modules.educacao.domain.models import Matricula
DomainEntity = Matricula
__all__ = ['DomainEntity', 'Matricula']