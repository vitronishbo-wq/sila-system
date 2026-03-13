"""Compatibilidade temporaria com estrutura antiga do modulo."""
from apps.backend.app.modules.civil_protection.infrastructure.repositories import SQLAlchemyAtendimentoRepository
from apps.backend.app.modules.civil_protection.infrastructure.repositories import SQLAlchemyBombeiroRepository, SQLAlchemyCorporacaoRepository, SQLAlchemyDespachoRepository, SQLAlchemyOcorrenciaEmergencialRepository
__all__ = ['SQLAlchemyCorporacaoRepository', 'SQLAlchemyBombeiroRepository', 'SQLAlchemyOcorrenciaEmergencialRepository', 'SQLAlchemyDespachoRepository', 'SQLAlchemyAtendimentoRepository']