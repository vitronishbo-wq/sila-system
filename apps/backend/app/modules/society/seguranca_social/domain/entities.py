"""Compatibility export for legacy imports."""

from apps.backend.app.modules.society.seguranca_social.domain.models import Beneficiario

DomainEntity = Beneficiario
__all__ = ["DomainEntity", "Beneficiario"]
