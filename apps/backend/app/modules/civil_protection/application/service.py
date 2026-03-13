"""Compatibilidade temporaria com estrutura antiga do modulo."""
from apps.backend.app.modules.civil_protection.application.services.atendimento_service import AtendimentoService
from apps.backend.app.modules.civil_protection.application.services import BombeiroService, CorporacaoService, DespachoService, OcorrenciaEmergencialService
__all__ = ['CorporacaoService', 'BombeiroService', 'OcorrenciaEmergencialService', 'DespachoService', 'AtendimentoService']