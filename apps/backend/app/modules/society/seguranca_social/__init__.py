"""Seguranca social module - beneficiarios e prestacoes sociais."""
from app.modules.society.seguranca_social.api.router import router
from app.modules.society.seguranca_social.application.services import BeneficiarioService, PensaoService
from app.modules.society.seguranca_social.infrastructure.models import BeneficiarioModel, PensaoModel
__all__ = ['router', 'BeneficiarioService', 'PensaoService', 'BeneficiarioModel', 'PensaoModel']