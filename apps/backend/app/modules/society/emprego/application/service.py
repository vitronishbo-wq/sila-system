"""Compatibility layer for emprego services."""

from apps.backend.app.modules.society.emprego.application.services import CandidatoService

EmpregoService = CandidatoService
__all__ = ["CandidatoService", "EmpregoService"]
