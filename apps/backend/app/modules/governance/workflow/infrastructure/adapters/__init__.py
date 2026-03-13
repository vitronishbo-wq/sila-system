"""Cross-module adapters used by Workflow runtime."""
from app.modules.governance.workflow.infrastructure.adapters.assistencia_social_adapter import AssistenciaSocialAdapter
from app.modules.governance.workflow.infrastructure.adapters.educacao_adapter import EducacaoAdapter
from app.modules.governance.workflow.infrastructure.adapters.emprego_adapter import EmpregoAdapter
from app.modules.governance.workflow.infrastructure.adapters.identidade_adapter import IdentidadeAdapter
from app.modules.governance.workflow.infrastructure.adapters.juventude_adapter import JuventudeAdapter
from app.modules.governance.workflow.infrastructure.adapters.saude_adapter import SaudeAdapter
__all__ = ['AssistenciaSocialAdapter', 'EducacaoAdapter', 'EmpregoAdapter', 'IdentidadeAdapter', 'JuventudeAdapter', 'SaudeAdapter']