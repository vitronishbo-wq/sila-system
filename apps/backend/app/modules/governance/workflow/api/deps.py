from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.api.deps import get_db
from app.domain.bridges import CitizenRepository
from app.domain.bridges.society_repository_bridges import make_assistencia_beneficiario_repository, make_assistencia_visita_repository, make_educacao_matricula_repository, make_educacao_turma_repository, make_emprego_candidato_repository, make_juventude_jovem_repository, make_saude_appointment_repository
from apps.backend.app.modules.governance.workflow.application.services.workflow_engine import WorkflowEngine
from apps.backend.app.modules.governance.workflow.infrastructure.adapters import AssistenciaSocialAdapter, EducacaoAdapter, EmpregoAdapter, IdentidadeAdapter, JuventudeAdapter, SaudeAdapter
from apps.backend.app.modules.governance.workflow.infrastructure.repositories.task_repository import TaskRepository
from apps.backend.app.modules.governance.workflow.infrastructure.repositories.workflow_repository import WorkflowRepository

async def can_view_instance(instance_id: UUID, db: AsyncSession=Depends(get_db)):
    """Verifica se pode visualizar instância"""
    repo = WorkflowRepository(db)
    instance = await repo.get_instance(instance_id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Instância não encontrada')
    return instance

async def get_workflow_engine(db: AsyncSession=Depends(get_db)) -> WorkflowEngine:
    """Compõe engine com dependências concretas na borda (API)."""
    workflow_repo = WorkflowRepository(db)
    task_repo = TaskRepository(db)
    educacao_adapter = EducacaoAdapter(matricula_repo=make_educacao_matricula_repository(db), turma_repo=make_educacao_turma_repository(db))
    identidade_adapter = IdentidadeAdapter(CitizenRepository(db))
    juventude_adapter = JuventudeAdapter(make_juventude_jovem_repository(db))
    emprego_adapter = EmpregoAdapter(make_emprego_candidato_repository(db))
    saude_adapter = SaudeAdapter(make_saude_appointment_repository(db))
    assistencia_social_adapter = AssistenciaSocialAdapter(beneficiario_repo=make_assistencia_beneficiario_repository(db), visita_repo=make_assistencia_visita_repository(db))
    return WorkflowEngine(workflow_repo=workflow_repo, task_repo=task_repo, educacao_adapter=educacao_adapter, identidade_adapter=identidade_adapter, juventude_adapter=juventude_adapter, emprego_adapter=emprego_adapter, saude_adapter=saude_adapter, assistencia_social_adapter=assistencia_social_adapter)