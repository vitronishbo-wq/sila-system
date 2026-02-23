from app.modules.workflow.api.deps import can_view_instance
from app.modules.workflow.api.schemas.workflow_schema import (    WorkflowStartRequest, WorkflowTransitionRequest,
    WorkflowInstanceResponse, WorkflowHistoryResponse
)
from app.modules.workflow.api.schemas.task_schema import (
    TaskResponse, TaskAssignRequest, TaskCompleteRequest,
    TaskListResponse
)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.modules.workflow.api.deps import get_workflow_engine
from app.modules.workflow.application.services.workflow_engine import WorkflowEngine

router = APIRouter(prefix="/workflow", tags=["Workflow"])

# middleware será adicionado na app principal


@router.post("/start", response_model=WorkflowInstanceResponse)
async def start_workflow(
    request: WorkflowStartRequest,
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Inicia um novo workflow
    """
    try:
        # Mock de identidade para teste
        citizen_id = UUID('00000000-0000-0000-0000-000000000001')
        user_id = UUID('00000000-0000-0000-0000-000000000002')
        
        instance = engine.start_workflow(
            workflow_code=request.workflow_code,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            citizen_id=citizen_id,
            created_by=user_id,
            variables=request.variables
        )
        return instance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/instances/{instance_id}", response_model=WorkflowInstanceResponse)
async def get_instance(
    instance = Depends(can_view_instance)
):
    """
    Obtém detalhes de uma instância
    """
    return instance


@router.post("/instances/{instance_id}/transitions", response_model=WorkflowInstanceResponse)
async def execute_transition(
    instance_id: UUID,
    request: WorkflowTransitionRequest,
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Executa uma transição no workflow
    """
    try:
        # Mock de identidade para teste
        user_id = UUID('00000000-0000-0000-0000-000000000002')
        
        instance = engine.execute_transition(
            instance_id=instance_id,
            transition_code=request.transition_code,
            actor_id=user_id,
            form_data=request.form_data
        )
        return instance
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/instances/{instance_id}/timeline", response_model=List[WorkflowHistoryResponse])
async def get_instance_timeline(
    instance = Depends(can_view_instance),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Obtém linha do tempo da instância
    """
    return engine.get_instance_timeline(instance.id)


@router.get("/tasks/my", response_model=TaskListResponse)
async def get_my_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Lista tarefas atribuídas ao usuário atual
    """
    # Mock de identidade para teste
    user_id = UUID('00000000-0000-0000-0000-000000000002')
    
    tasks = engine.get_tasks_for_user(user_id, skip, limit)
    
    return {
        "total": len(tasks),
        "items": tasks
    }


@router.get("/tasks/pending", response_model=TaskListResponse)
async def get_pending_tasks(
    role: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Lista tarefas pendentes (para gestores)
    """
    if role:
        tasks = engine.get_tasks_for_role(role, skip, limit)
    else:
        tasks = engine.get_tasks_for_role("OPERATOR", skip, limit)
    
    return {
        "total": len(tasks),
        "items": tasks
    }


@router.post("/tasks/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: UUID,
    request: TaskAssignRequest,
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Atribui uma tarefa a um usuário
    """
    try:
        # Mock de identidade para teste
        actor_id = UUID('00000000-0000-0000-0000-000000000002')
        
        task = engine.assign_task(
            task_id=task_id,
            user_id=request.user_id,
            actor_id=actor_id
        )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    request: TaskCompleteRequest,
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    """
    Completa uma tarefa
    """
    try:
        # Mock de identidade para teste
        user_id = UUID('00000000-0000-0000-0000-000000000002')
        
        task = engine.complete_task(
            task_id=task_id,
            result=request.result,
            actor_id=user_id
        )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
