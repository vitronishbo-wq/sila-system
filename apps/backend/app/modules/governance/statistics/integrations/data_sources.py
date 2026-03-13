from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.statistics.integrations.assistencia_data_source import AssistenciaDataSource
from app.modules.governance.statistics.integrations.educacao_data_source import EducacaoDataSource
from app.modules.governance.statistics.integrations.emprego_data_source import EmpregoDataSource
from app.modules.governance.statistics.integrations.identidade_data_source import IdentidadeDataSource
from app.modules.governance.statistics.integrations.juventude_data_source import JuventudeDataSource
from app.modules.governance.statistics.integrations.saude_data_source import SaudeDataSource
from app.modules.governance.statistics.integrations.service_requests_data_source import ServiceRequestsDataSource
from app.modules.governance.statistics.integrations.workflow_data_source import WorkflowDataSource

class DataSources:
    """Registry de fontes de dados do modulo statistics."""

    def __init__(self, educacao: EducacaoDataSource | None=None, juventude: JuventudeDataSource | None=None, emprego: EmpregoDataSource | None=None, saude: SaudeDataSource | None=None, assistencia: AssistenciaDataSource | None=None, identidade: IdentidadeDataSource | None=None, workflow: WorkflowDataSource | None=None, service_requests: ServiceRequestsDataSource | None=None):
        self.educacao = educacao
        self.juventude = juventude
        self.emprego = emprego
        self.saude = saude
        self.assistencia = assistencia
        self.identidade = identidade
        self.workflow = workflow
        self.service_requests = service_requests

    @classmethod
    def from_session(cls, db: AsyncSession) -> 'DataSources':
        return cls(educacao=EducacaoDataSource(db), juventude=JuventudeDataSource(db), emprego=EmpregoDataSource(db), saude=SaudeDataSource(db), assistencia=AssistenciaDataSource(db), identidade=IdentidadeDataSource(db), workflow=WorkflowDataSource(db), service_requests=ServiceRequestsDataSource(db))

    def as_dict(self) -> dict[str, object]:
        return {'educacao': self.educacao, 'juventude': self.juventude, 'emprego': self.emprego, 'saude': self.saude, 'assistencia': self.assistencia, 'identidade': self.identidade, 'workflow': self.workflow, 'service_requests': self.service_requests}

    async def workflow_metrics(self, data_ref):
        if not self.workflow:
            return {}
        return await self.workflow.collect_metrics(data_ref)

    async def service_requests_metrics(self, data_ref):
        if not self.service_requests:
            return {}
        return await self.service_requests.collect_metrics(data_ref)

    async def health_metrics(self, data_ref):
        if not self.saude:
            return {}
        return await self.saude.collect_metrics(data_ref)