"""Ports (interfaces) for workflow module."""

from apps.backend.app.modules.governance.workflow.application.ports.assistencia_social_adapter_port import (
    AssistenciaSocialAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.educacao_adapter_port import (
    EducacaoAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.emprego_adapter_port import (
    EmpregoAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.identidade_adapter_port import (
    IdentidadeAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.juventude_adapter_port import (
    JuventudeAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.saude_adapter_port import (
    SaudeAdapterPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.task_repository_port import (
    TaskRepositoryPort,
)
from apps.backend.app.modules.governance.workflow.application.ports.workflow_repository_port import (
    WorkflowRepositoryPort,
)

__all__ = [
    "AssistenciaSocialAdapterPort",
    "EducacaoAdapterPort",
    "EmpregoAdapterPort",
    "IdentidadeAdapterPort",
    "JuventudeAdapterPort",
    "SaudeAdapterPort",
    "TaskRepositoryPort",
    "WorkflowRepositoryPort",
]
