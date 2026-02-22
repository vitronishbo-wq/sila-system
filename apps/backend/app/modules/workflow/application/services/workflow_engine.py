from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import json
from datetime import datetime, timedelta

from app.modules.workflow.domain.models.workflow_definition import WorkflowDefinition
from app.modules.workflow.domain.models.workflow_instance import WorkflowInstance
from app.modules.workflow.domain.models.workflow_task import WorkflowTask
from app.modules.workflow.domain.models.workflow_history import WorkflowHistory
from app.modules.workflow.domain.enums import WorkflowStatus, TaskStatus, TaskPriority, EntityType
from app.modules.workflow.infrastructure.repositories.workflow_repository import WorkflowRepository
from app.modules.workflow.infrastructure.repositories.task_repository import TaskRepository
from app.modules.workflow.integrations.iam_client import IAMClient
from app.modules.workflow.integrations.notification_client import NotificationClient


class WorkflowEngine:
    """Motor principal de workflow"""
    
    def __init__(self, db: Session):
        self.db = db
        self.workflow_repo = WorkflowRepository(db)
        self.task_repo = TaskRepository(db)
        self.iam = IAMClient()
        self.notifications = NotificationClient()
    
    def start_workflow(self, workflow_code: str, entity_type: str, entity_id: UUID,
                       citizen_id: UUID, created_by: UUID,
                       variables: Dict[str, Any] = None) -> WorkflowInstance:
        """
        Inicia uma nova instância de workflow
        """
        # Buscar definição do workflow
        definition = self.workflow_repo.get_definition_by_code(workflow_code)
        if not definition:
            raise ValueError(f"Workflow não encontrado: {workflow_code}")
        
        if not definition.is_active:
            raise ValueError(f"Workflow inativo: {workflow_code}")
        
        # Buscar estado inicial
        initial_state = self.workflow_repo.get_initial_state(definition.id)
        if not initial_state:
            raise ValueError(f"Workflow sem estado inicial: {workflow_code}")
        
        # Verificar se já existe instância para esta entidade
        existing = self.workflow_repo.get_instance_by_entity(entity_type, entity_id)
        if existing and existing.status == WorkflowStatus.ACTIVE:
            raise ValueError(f"Já existe workflow ativo para esta entidade")
        
        # Criar instância
        instance = WorkflowInstance(
            workflow_id=definition.id,
            current_state_id=initial_state.id,
            entity_type=entity_type,
            entity_id=entity_id,
            citizen_id=citizen_id,
            created_by=created_by,
            variables=variables or {},
            deadline=datetime.now() + timedelta(hours=definition.timeout_hours) if definition.timeout_hours else None,
            timeout_hours=definition.timeout_hours
        )
        
        instance = self.workflow_repo.save_instance(instance)
        
        # Registrar histórico
        history = WorkflowHistory.system(
            instance_id=instance.id,
            action="WORKFLOW_STARTED",
            data={
                "workflow_code": workflow_code,
                "initial_state": initial_state.code
            }
        )
        self.workflow_repo.save_history(history)
        
        # Criar tarefas iniciais automaticamente
        self._create_auto_tasks(instance, initial_state)
        
        # Notificar
        self.notifications.notify_citizen(
            citizen_id,
            "Processo Iniciado",
            f"Seu processo foi iniciado com sucesso"
        )
        
        return instance
    
    def execute_transition(self, instance_id: UUID, transition_code: str,
                           actor_id: UUID, form_data: Dict[str, Any] = None) -> WorkflowInstance:
        """
        Executa uma transição em uma instância
        """
        instance = self.workflow_repo.get_instance(instance_id)
        if not instance:
            raise ValueError(f"Instância não encontrada")
        
        if not instance.is_active:
            raise ValueError(f"Instância não está ativa")
        
        # Buscar transição
        definition = self.workflow_repo.get_definition(instance.workflow_id)
        transition = self.workflow_repo.get_transition_by_code(definition.id, transition_code)
        if not transition:
            raise ValueError(f"Transição não encontrada: {transition_code}")
        
        # Verificar se é do estado atual
        if transition.from_state_id != instance.current_state_id:
            raise ValueError(f"Transição não permitida no estado atual")
        
        # Verificar permissões do ator
        user_info = self.iam.get_user(actor_id)
        if not transition.can_execute(user_info.get('permissions', []), user_info.get('roles', [])):
            raise PermissionError(f"Usuário não tem permissão para executar esta transição")
        
        # Executar pré-ações
        self._execute_actions(transition.pre_actions, instance, form_data)
        
        # Registrar estado anterior
        from_state_id = instance.current_state_id
        
        # Atualizar estado
        instance.current_state_id = transition.to_state_id
        instance.updated_at = datetime.now()
        
        # Atualizar variáveis com dados do formulário
        if form_data:
            for key, value in form_data.items():
                instance.set_variable(key, value)
        
        instance = self.workflow_repo.save_instance(instance)
        
        # Executar pós-ações
        self._execute_actions(transition.post_actions, instance, form_data)
        
        # Verificar se é estado final
        to_state = self._get_state(transition.to_state_id)
        if to_state and to_state.is_final:
            instance.complete()
            instance = self.workflow_repo.save_instance(instance)
        
        # Registrar histórico
        history = WorkflowHistory.transition(
            instance_id=instance.id,
            from_state=from_state_id,
            to_state=transition.to_state_id,
            transition_id=transition.id,
            performed_by=actor_id,
            comment=f"Transição executada: {transition.name}"
        )
        self.workflow_repo.save_history(history)
        
        # Criar novas tarefas se necessário
        self._create_auto_tasks(instance, to_state)
        
        # Notificar cidadão
        self.notifications.notify_citizen(
            instance.citizen_id,
            "Processo Atualizado",
            f"Seu processo mudou de status"
        )
        
        return instance
    
    def create_task(self, instance_id: UUID, state_id: UUID, transition_id: UUID,
                    title: str, description: str = None,
                    assigned_to: UUID = None, assigned_role: str = None,
                    priority: str = "MEDIUM", due_in_hours: int = None) -> WorkflowTask:
        """
        Cria uma tarefa manual
        """
        instance = self.workflow_repo.get_instance(instance_id)
        if not instance:
            raise ValueError(f"Instância não encontrada")
        
        task = WorkflowTask(
            instance_id=instance_id,
            state_id=state_id,
            transition_id=transition_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_role=assigned_role,
            priority=TaskPriority(priority),
            due_at=datetime.now() + timedelta(hours=due_in_hours) if due_in_hours else None,
            timeout_hours=due_in_hours
        )
        
        task = self.task_repo.save_task(task)
        
        # Registrar histórico
        history = WorkflowHistory(
            instance_id=instance_id,
            task_id=task.id,
            action="TASK_CREATED",
            action_type="SYSTEM",
            data={"task_title": title}
        )
        self.workflow_repo.save_history(history)
        
        return task
    
    def assign_task(self, task_id: UUID, user_id: UUID, actor_id: UUID) -> WorkflowTask:
        """
        Atribui uma tarefa a um usuário
        """
        task = self.task_repo.assign_task(task_id, user_id)
        
        if task:
            history = WorkflowHistory.assignment(
                instance_id=task.instance_id,
                task_id=task_id,
                assigned_to=user_id,
                performed_by=actor_id
            )
            self.workflow_repo.save_history(history)
            
            # Notificar
            self.notifications.notify_operator(
                user_id,
                "Nova Tarefa",
                f"Tarefa atribuída: {task.title}"
            )
        
        return task
    
    def complete_task(self, task_id: UUID, result: Dict[str, Any] = None,
                      actor_id: UUID = None) -> WorkflowTask:
        """
        Completa uma tarefa
        """
        task = self.task_repo.complete_task(task_id, result)
        
        if task:
            history = WorkflowHistory(
                instance_id=task.instance_id,
                task_id=task_id,
                action="TASK_COMPLETED",
                action_type="SYSTEM",
                performed_by=actor_id,
                data={"result": result}
            )
            self.workflow_repo.save_history(history)
            
            # Se a tarefa está vinculada a uma transição, executar automaticamente
            if task.transition_id:
                try:
                    transition = self.workflow_repo.get_transition(task.transition_id)
                    if transition and transition.transition_type.value == "AUTOMATIC":
                        self.execute_transition(
                            task.instance_id,
                            transition.code,
                            actor_id or task.assigned_to,
                            result
                        )
                except:
                    pass
        
        return task
    
    def get_tasks_for_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[WorkflowTask]:
        """
        Obtém tarefas pendentes para um usuário
        """
        tasks, _ = self.task_repo.get_pending_tasks(user_id=user_id, skip=skip, limit=limit)
        return tasks
    
    def get_tasks_for_role(self, role: str, skip: int = 0, limit: int = 100) -> List[WorkflowTask]:
        """
        Obtém tarefas pendentes para uma role
        """
        tasks, _ = self.task_repo.get_pending_tasks(role=role, skip=skip, limit=limit)
        return tasks
    
    def get_instance_timeline(self, instance_id: UUID) -> List[Dict[str, Any]]:
        """
        Obtém linha do tempo da instância
        """
        history = self.workflow_repo.get_instance_history(instance_id)
        return [h.to_dict() for h in history]
    
    def check_sla_breaches(self) -> List[WorkflowInstance]:
        """
        Verifica instâncias com SLA estourado
        """
        overdue_instances = []
        
        # Verificar instâncias com deadline passado
        instances = self.workflow_repo.list_instances(status=WorkflowStatus.ACTIVE)[0]
        for instance in instances:
            if instance.is_overdue:
                overdue_instances.append(instance)
                
                # Registrar no histórico
                history = WorkflowHistory.system(
                    instance_id=instance.id,
                    action="SLA_BREACHED",
                    data={"deadline": instance.deadline.isoformat()}
                )
                self.workflow_repo.save_history(history)
                
                # Notificar
                self.notifications.notify_managers(
                    "SLA Estourado",
                    f"Processo {instance.id} ultrapassou o prazo"
                )
        
        return overdue_instances
    
    def _create_auto_tasks(self, instance: WorkflowInstance, state):
        """Cria tarefas automáticas baseadas no estado"""
        if not state or not state.is_auto_forward:
            return
        
        # Buscar transições automáticas deste estado
        transitions = self.workflow_repo.get_transitions(state.id)
        for transition in transitions:
            if transition.transition_type.value == "AUTOMATIC":
                self.create_task(
                    instance_id=instance.id,
                    state_id=state.id,
                    transition_id=transition.id,
                    title=transition.name,
                    description=transition.description,
                    assigned_role=transition.assignment_value if transition.assignment_type.value == "ROLE" else None,
                    due_in_hours=state.timeout_hours
                )
    
    def _execute_actions(self, actions: Dict[str, Any], instance: WorkflowInstance, form_data: Dict[str, Any] = None):
        """Executa ações configuradas na transição"""
        if not actions:
            return
        
        for action_type, action_config in actions.items():
            if action_type == "update_variables":
                for key, value in action_config.items():
                    instance.set_variable(key, value)
            
            elif action_type == "send_notification":
                template = action_config.get("template")
                recipient = action_config.get("recipient")
                # Implementar envio de notificação
    
    def _get_state(self, state_id: UUID):
        """Obtém estado por ID"""
        from app.modules.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
        model = self.db.query(WorkflowStateModel).filter(
            WorkflowStateModel.id == state_id
        ).first()
        if model:
            from app.modules.workflow.domain.models.workflow_state import WorkflowState
            return WorkflowState(
                id=model.id,
                workflow_id=model.workflow_id,
                code=model.code,
                name=model.name,
                is_final=model.is_final,
                is_auto_forward=model.is_auto_forward
            )
        return None
