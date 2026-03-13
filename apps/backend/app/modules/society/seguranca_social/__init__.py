"""Seguranca social module - beneficiarios e prestacoes sociais."""
from apps.backend.app.modules.society.seguranca_social.api.router import router
from apps.backend.app.modules.society.seguranca_social.application.services import BeneficiarioService, PensaoService
from apps.backend.app.modules.society.seguranca_social.infrastructure.models import BeneficiarioModel, PensaoModel
__all__ = ['router', 'BeneficiarioService', 'PensaoService', 'BeneficiarioModel', 'PensaoModel']