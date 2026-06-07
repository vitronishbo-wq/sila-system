"""Compatibility layer for seguranca_social services."""

from apps.backend.app.modules.society.seguranca_social.application.services import (
    BeneficiarioService,
    PensaoService,
)

SegurancaSocialService = BeneficiarioService
__all__ = ["BeneficiarioService", "PensaoService", "SegurancaSocialService"]
