"""Compatibility exports for seguranca_social repositories."""

from apps.backend.app.modules.society.seguranca_social.infrastructure.repositories import (
    SQLAlchemyBeneficiarioRepository,
    SQLAlchemyPensaoRepository,
)

Repository = SQLAlchemyBeneficiarioRepository
__all__ = ["SQLAlchemyBeneficiarioRepository", "SQLAlchemyPensaoRepository", "Repository"]
