import inspect
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.core.security import IAMClient
from app.modules.governance.workflow.application.ports.assistencia_social_adapter_port import AssistenciaSocialAdapterPort
from app.modules.governance.workflow.application.ports.educacao_adapter_port import EducacaoAdapterPort
from app.modules.governance.workflow.application.ports.emprego_adapter_port import EmpregoAdapterPort
from app.modules.governance.workflow.application.ports.identidade_adapter_port import IdentidadeAdapterPort
from app.modules.governance.workflow.application.ports.juventude_adapter_port import JuventudeAdapterPort
from app.modules.governance.workflow.application.ports.saude_adapter_port import SaudeAdapterPort
from app.modules.governance.workflow.application.ports.task_repository_port import TaskRepositoryPort
from app.modules.governance.workflow.application.ports.workflow_repository_port import WorkflowRepositoryPort
from app.modules.governance.workflow.domain.enums import TaskPriority, WorkflowStatus
from app.modules.governance.workflow.domain.models.workflow_history import WorkflowHistory
from app.modules.governance.workflow.domain.models.workflow_instance import WorkflowInstance
from app.modules.governance.workflow.domain.models.workflow_task import WorkflowTask
from app.modules.governance.workflow.integrations.notification_client import NotificationClient

class WorkflowEngine:
    """Motor principal de workflow (async)."""

    def __init__(self, workflow_repo: WorkflowRepositoryPort, task_repo: TaskRepositoryPort, iam: IAMClient | None=None, notifications: NotificationClient | None=None, educacao_adapter: EducacaoAdapterPort | None=None, identidade_adapter: IdentidadeAdapterPort | None=None, juventude_adapter: JuventudeAdapterPort | None=None, emprego_adapter: EmpregoAdapterPort | None=None, saude_adapter: SaudeAdapterPort | None=None, assistencia_social_adapter: AssistenciaSocialAdapterPort | None=None):
        self.workflow_repo = workflow_repo
        self.task_repo = task_repo
        self.iam = iam or IAMClient()
        self.notifications = notifications or NotificationClient()
        self.adapters = {'educacao': educacao_adapter, 'identidade': identidade_adapter, 'identity': identidade_adapter, 'juventude': juventude_adapter, 'emprego': emprego_adapter, 'saude': saude_adapter, 'assistencia': assistencia_social_adapter, 'assistencia_social': assistencia_social_adapter}

    async def start_workflow(self, workflow_code: str, entity_type: str, entity_id: UUID, citizen_id: UUID, created_by: UUID, variables: Dict[str, Any] | None=None) -> WorkflowInstance:
        definition = await self.workflow_repo.get_definition_by_code(workflow_code)
        if not definition:
            raise ValueError(f'Workflow não encontrado: {workflow_code}')
        if not definition.is_active:
            raise ValueError(f'Workflow inativo: {workflow_code}')
        initial_state = await self.workflow_repo.get_initial_state(definition.id)
        if not initial_state:
            raise ValueError(f'Workflow sem estado inicial: {workflow_code}')
        existing = await self.workflow_repo.get_instance_by_entity(entity_type, entity_id)
        if existing and existing.status == WorkflowStatus.ACTIVE:
            raise ValueError('Já existe workflow ativo para esta entidade')
        instance = WorkflowInstance(workflow_id=definition.id, current_state_id=initial_state.id, entity_type=entity_type, entity_id=entity_id, citizen_id=citizen_id, created_by=created_by, variables=variables or {}, deadline=datetime.now() + timedelta(hours=definition.timeout_hours) if definition.timeout_hours else None, timeout_hours=definition.timeout_hours)
        instance = await self.workflow_repo.save_instance(instance)
        history = WorkflowHistory.system(instance_id=instance.id, action='WORKFLOW_STARTED', data={'workflow_code': workflow_code, 'initial_state': initial_state.code})
        await self.workflow_repo.save_history(history)
        await self._create_auto_tasks(instance, initial_state)
        await self.workflow_repo.commit()
        self.notifications.notify_citizen(citizen_id, 'Processo Iniciado', 'Seu processo foi iniciado com sucesso')
        return instance

    async def execute_transition(self, instance_id: UUID, transition_code: str, actor_id: UUID, form_data: Dict[str, Any] | None=None) -> WorkflowInstance:
        instance = await self.workflow_repo.get_instance(instance_id)
        if not instance:
            raise ValueError('Instância não encontrada')
        if not instance.is_active:
            raise ValueError('Instância não está ativa')
        definition = await self.workflow_repo.get_definition(instance.workflow_id)
        transition = await self.workflow_repo.get_transition_by_code(definition.id, transition_code)
        if not transition:
            raise ValueError(f'Transição não encontrada: {transition_code}')
        if transition.from_state_id != instance.current_state_id:
            raise ValueError('Transição não permitida no estado atual')
        if not await self._evaluate_transition_condition(transition.condition_expression, instance, form_data):
            raise ValueError('Condição da transição não atendida')
        user_info = await self.iam.get_user(str(actor_id))
        permissions = list(getattr(user_info, 'permissions', []) or [])
        roles = list(getattr(user_info, 'roles', []) or [])
        if transition.required_permissions or transition.required_roles:
            if not transition.can_execute(permissions, roles):
                raise PermissionError('Usuário não tem permissão para executar esta transição')
        await self._execute_actions(transition.pre_actions, instance, form_data)
        from_state_id = instance.current_state_id
        instance.current_state_id = transition.to_state_id
        instance.updated_at = datetime.now()
        if form_data:
            for key, value in form_data.items():
                instance.set_variable(key, value)
        instance = await self.workflow_repo.save_instance(instance)
        await self._execute_actions(transition.post_actions, instance, form_data)
        to_state = await self.workflow_repo.get_state(transition.to_state_id)
        if to_state and to_state.is_final:
            instance.complete()
            instance = await self.workflow_repo.save_instance(instance)
        history = WorkflowHistory.transition(instance_id=instance.id, from_state=from_state_id, to_state=transition.to_state_id, transition_id=transition.id, performed_by=actor_id, comment=f'Transição executada: {transition.name}')
        await self.workflow_repo.save_history(history)
        await self._create_auto_tasks(instance, to_state)
        await self.workflow_repo.commit()
        self.notifications.notify_citizen(instance.citizen_id, 'Processo Atualizado', 'Seu processo mudou de status')
        return instance

    async def create_task(self, instance_id: UUID, state_id: UUID, transition_id: UUID, title: str, description: str=None, assigned_to: UUID=None, assigned_role: str=None, priority: str='MEDIUM', due_in_hours: int=None) -> WorkflowTask:
        instance = await self.workflow_repo.get_instance(instance_id)
        if not instance:
            raise ValueError('Instância não encontrada')
        task = WorkflowTask(instance_id=instance_id, state_id=state_id, transition_id=transition_id, title=title, description=description, assigned_to=assigned_to, assigned_role=assigned_role, priority=TaskPriority(priority.lower()), due_at=datetime.now() + timedelta(hours=due_in_hours) if due_in_hours else None, timeout_hours=due_in_hours)
        task = await self.task_repo.save_task(task)
        history = WorkflowHistory(instance_id=instance_id, task_id=task.id, action='TASK_CREATED', action_type='SYSTEM', data={'task_title': title})
        await self.workflow_repo.save_history(history)
        await self.workflow_repo.commit()
        return task

    async def assign_task(self, task_id: UUID, user_id: UUID, actor_id: UUID) -> Optional[WorkflowTask]:
        task = await self.task_repo.assign_task(task_id, user_id)
        if task:
            history = WorkflowHistory.assignment(instance_id=task.instance_id, task_id=task_id, assigned_to=user_id, performed_by=actor_id)
            await self.workflow_repo.save_history(history)
            await self.workflow_repo.commit()
            self.notifications.notify_operator(user_id, 'Nova Tarefa', f'Tarefa atribuída: {task.title}')
        return task

    async def complete_task(self, task_id: UUID, result: Dict[str, Any] | None=None, actor_id: UUID=None) -> Optional[WorkflowTask]:
        task = await self.task_repo.complete_task(task_id, result)
        if task:
            history = WorkflowHistory(instance_id=task.instance_id, task_id=task_id, action='TASK_COMPLETED', action_type='SYSTEM', performed_by=actor_id, data={'result': result or {}})
            await self.workflow_repo.save_history(history)
            if task.transition_id:
                transition = await self.workflow_repo.get_transition(task.transition_id)
                if transition and transition.transition_type.value == 'automatic':
                    await self.execute_transition(task.instance_id, transition.code, actor_id or task.assigned_to, result)
                else:
                    await self.workflow_repo.commit()
            else:
                await self.workflow_repo.commit()
        return task

    async def get_tasks_for_user(self, user_id: UUID, skip: int=0, limit: int=100) -> List[WorkflowTask]:
        tasks, _ = await self.task_repo.get_pending_tasks(user_id=user_id, skip=skip, limit=limit)
        return tasks

    async def get_tasks_for_role(self, role: str, skip: int=0, limit: int=100) -> List[WorkflowTask]:
        tasks, _ = await self.task_repo.get_pending_tasks(role=role, skip=skip, limit=limit)
        return tasks

    async def get_instance_timeline(self, instance_id: UUID) -> List[Dict[str, Any]]:
        history = await self.workflow_repo.get_instance_history(instance_id)
        return [h.to_dict() for h in history]

    async def check_sla_breaches(self) -> List[WorkflowInstance]:
        overdue_instances: List[WorkflowInstance] = []
        instances, _ = await self.workflow_repo.list_instances(status=WorkflowStatus.ACTIVE)
        for instance in instances:
            if instance.is_overdue:
                overdue_instances.append(instance)
                history = WorkflowHistory.system(instance_id=instance.id, action='SLA_BREACHED', data={'deadline': instance.deadline.isoformat() if instance.deadline else None})
                await self.workflow_repo.save_history(history)
        if overdue_instances:
            await self.workflow_repo.commit()
            self.notifications.notify_managers('SLA Estourado', f'{len(overdue_instances)} processo(s) ultrapassaram o prazo')
        return overdue_instances

    async def _create_auto_tasks(self, instance: WorkflowInstance, state):
        if not state or not state.is_auto_forward:
            return
        transitions = await self.workflow_repo.get_transitions(state.id)
        for transition in transitions:
            if transition.transition_type.value == 'automatic':
                await self.create_task(instance_id=instance.id, state_id=state.id, transition_id=transition.id, title=transition.name, description=transition.description, assigned_role=transition.assignment_value if transition.assignment_type.value == 'role' else None, due_in_hours=state.timeout_hours)

    async def _evaluate_transition_condition(self, condition_expression: str | None, instance: WorkflowInstance, form_data: Dict[str, Any] | None=None) -> bool:
        if not condition_expression:
            return True
        expression = condition_expression.strip()
        if not expression:
            return True
        if ' and ' in expression:
            parts = [part.strip() for part in expression.split(' and ')]
            return all((await self._evaluate_transition_condition(part, instance, form_data) for part in parts))
        if ' or ' in expression:
            parts = [part.strip() for part in expression.split(' or ')]
            return any((await self._evaluate_transition_condition(part, instance, form_data) for part in parts))
        if expression.lower().startswith('not '):
            return not await self._evaluate_transition_condition(expression[4:].strip(), instance, form_data)
        payload = self._build_runtime_payload(instance, form_data)
        lower = expression.lower()
        if lower == 'true':
            return True
        if lower == 'false':
            return False
        if '.' in expression:
            adapter_name, method_name = expression.split('.', 1)
            method_name = method_name.split('(', 1)[0].strip()
            if method_name:
                result = await self._invoke_adapter_call(adapter_name=adapter_name.strip(), method_name=method_name, payload=payload)
                return bool(result)
        return bool(payload.get(expression))

    async def _execute_actions(self, actions: Dict[str, Any], instance: WorkflowInstance, form_data: Dict[str, Any] | None=None) -> None:
        if not actions:
            return
        payload = self._build_runtime_payload(instance, form_data)
        for action_type, action_config in actions.items():
            if action_type == 'update_variables':
                for key, value in action_config.items():
                    instance.set_variable(key, self._resolve_value(value, payload))
            elif action_type == 'send_notification':
                title = action_config.get('title', 'Workflow')
                message = action_config.get('message', '')
                data = action_config.get('data')
                self.notifications.notify_citizen(instance.citizen_id, title, message, self._resolve_value(data, payload) if data else None)
            elif action_type in {'call_adapter', 'invoke_adapter', 'integration'}:
                await self._run_adapter_actions(action_config, instance, form_data)

    async def _run_adapter_actions(self, action_config: Any, instance: WorkflowInstance, form_data: Dict[str, Any] | None) -> None:
        calls: List[Dict[str, Any]] = []
        if isinstance(action_config, list):
            calls = [item for item in action_config if isinstance(item, dict)]
        elif isinstance(action_config, dict):
            if 'adapter' in action_config and 'method' in action_config:
                calls = [action_config]
            else:
                for adapter_name, config in action_config.items():
                    if isinstance(config, str):
                        calls.append({'adapter': adapter_name, 'method': config})
                    elif isinstance(config, dict):
                        call = {'adapter': adapter_name, **config}
                        calls.append(call)
        if not calls:
            return
        payload = self._build_runtime_payload(instance, form_data)
        for call in calls:
            adapter_name = str(call.get('adapter', '')).strip()
            method_name = str(call.get('method', '')).strip()
            if not adapter_name or not method_name:
                continue
            raw_args = call.get('args')
            args = self._resolve_value(raw_args, payload) if isinstance(raw_args, dict) else payload
            result = await self._invoke_adapter_call(adapter_name, method_name, args)
            store_key = call.get('save_as') or call.get('result_key')
            if store_key:
                instance.set_variable(str(store_key), result)

    async def _invoke_adapter_call(self, adapter_name: str, method_name: str, payload: Dict[str, Any]) -> Any:
        adapter = self.adapters.get(adapter_name.lower())
        if adapter is None:
            raise ValueError(f'Adapter não configurado: {adapter_name}')
        method = getattr(adapter, method_name, None)
        if method is None:
            raise ValueError(f'Método {method_name} não encontrado no adapter {adapter_name}')
        kwargs = self._filter_kwargs(method, payload or {})
        result = method(**kwargs)
        if inspect.isawaitable(result):
            return await result
        return result

    @staticmethod
    def _filter_kwargs(method: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
        signature = inspect.signature(method)
        params = signature.parameters.values()
        if any((param.kind == inspect.Parameter.VAR_KEYWORD for param in params)):
            return payload
        accepted = {param.name for param in signature.parameters.values() if param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)}
        if not accepted:
            return {}
        return {key: value for key, value in payload.items() if key in accepted}

    @staticmethod
    def _build_runtime_payload(instance: WorkflowInstance, form_data: Dict[str, Any] | None=None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {'instance_id': instance.id, 'workflow_id': instance.workflow_id, 'entity_type': instance.entity_type, 'entity_id': instance.entity_id, 'citizen_id': instance.citizen_id, 'created_by': instance.created_by, 'current_state_id': instance.current_state_id}
        payload.update(instance.context or {})
        payload.update(instance.variables or {})
        if form_data:
            payload.update(form_data)
        return payload

    def _resolve_value(self, value: Any, payload: Dict[str, Any]) -> Any:
        if isinstance(value, str) and value.startswith('$'):
            return payload.get(value[1:])
        if isinstance(value, dict):
            return {key: self._resolve_value(item, payload) for key, item in value.items()}
        if isinstance(value, list):
            return [self._resolve_value(item, payload) for item in value]
        return value