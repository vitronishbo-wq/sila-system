"""Compatibility export for legacy imports."""
from apps.backend.app.modules.educacao.domain.models import Matricula
DomainEntity = Matricula
__all__ = ['DomainEntity', 'Matricula']