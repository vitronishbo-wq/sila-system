from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.workflow.application.services.workflow_engine import WorkflowEngine
from app.modules.workflow.infrastructure.repositories.workflow_repository import WorkflowRepository


def get_workflow_engine(db: Session = Depends(get_db)) -> WorkflowEngine:
    """Dependency para obter engine de workflow"""
    return WorkflowEngine(db)


def get_workflow_repository(db: Session = Depends(get_db)) -> WorkflowRepository:
    """Dependency para obter repositório de workflow"""
    return WorkflowRepository(db)


def can_view_instance(instance_id: UUID, db: Session = Depends(get_db)):
    """Verifica se pode visualizar instância"""
    repo = WorkflowRepository(db)
    instance = repo.get_instance(instance_id)
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instância não encontrada"
        )
    
    return instance
