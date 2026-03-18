from apps.backend.app.core.observability import trace
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.core.services.base_request_service import BaseRequestService
from ...domain.models.service_request import ServiceRequest
from ...domain.enums import ServiceType, RequestChannel, RequestPriority, ServiceRequestStatus
from ..ports.domain_client_port import DomainClientPort
from ..ports.request_repository_port import RequestRepositoryPort
from ..ports.request_service_port import RequestServicePort
from .request_factory import RequestFactory

class RequestService(BaseRequestService[ServiceRequest, RequestRepositoryPort], RequestServicePort):
    """Serviço de pedidos de serviço (ASYNC) - com herança de BaseRequestService para ciclo de vida unificado"""

    def __init__(self, db: AsyncSession, repository: RequestRepositoryPort, workflow_engine=None, notification_service=None, educacao_client: Optional[DomainClientPort]=None, juventude_client: Optional[DomainClientPort]=None, emprego_client: Optional[DomainClientPort]=None, saude_client: Optional[DomainClientPort]=None, assistencia_client: Optional[DomainClientPort]=None, identidade_client: Optional[DomainClientPort]=None):
        super().__init__(db=db, repository=repository, notification_service=notification_service, audit_enabled=True, workflow_engine=workflow_engine)
        self.workflow_engine = workflow_engine
        self.educacao_client = educacao_client
        self.juventude_client = juventude_client
        self.emprego_client = emprego_client
        self.saude_client = saude_client
        self.assistencia_client = assistencia_client
        self.identidade_client = identidade_client
        self._domain_clients: dict[ServiceType, DomainClientPort] = {}
        if self.educacao_client:
            self._domain_clients[ServiceType.EDUCATION_ENROLLMENT] = self.educacao_client
            self._domain_clients[ServiceType.EDUCATION_CERTIFICATE] = self.educacao_client
        if self.juventude_client:
            self._domain_clients[ServiceType.YOUTH_PROGRAM] = self.juventude_client
        if self.emprego_client:
            self._domain_clients[ServiceType.EMPLOYMENT_APPLICATION] = self.emprego_client
        if self.saude_client:
            self._domain_clients[ServiceType.HEALTH_APPOINTMENT] = self.saude_client
            self._domain_clients[ServiceType.HEALTH_EXAM] = self.saude_client
            self._domain_clients[ServiceType.HEALTH_PRESCRIPTION] = self.saude_client
        if self.assistencia_client:
            self._domain_clients[ServiceType.SOCIAL_BENEFIT] = self.assistencia_client

    def get_repository(self) -> RequestRepositoryPort:
        """Return repository instance"""
        return self.repo

    def default_status(self) -> str:
        """Initial status for service requests (DRAFT)"""
        return ServiceRequestStatus.DRAFT.value

    @trace()
    async def create_request_model(self, citizen_id: UUID, request_data: Dict[str, Any], **kwargs) -> ServiceRequest:
        """Create ServiceRequest domain model with request_number"""
        year = datetime.now().year
        sequence = await self.repo.get_next_sequence(year)
        request_number = f'SR/{year}/{sequence:06d}'
        draft = RequestFactory.create_draft(citizen_id=citizen_id, created_by=kwargs.get('created_by', citizen_id), service_type=request_data.get('service_type'), title=request_data.get('title'), description=request_data.get('description'), channel=request_data.get('channel', RequestChannel.WEB), priority=request_data.get('priority', RequestPriority.MEDIUM), metadata=request_data.get('metadata'), tags=request_data.get('tags'))
        draft.request_number = request_number
        return draft

    @trace()
    async def get_user_from_citizen_id(self, citizen_id: UUID) -> Optional[UUID]:
        """For service requests, citizen_id IS the user"""
        return citizen_id

    @trace()
    async def _post_save_create(self, saved_request: ServiceRequest, created_by: UUID) -> None:
        """After save: Notify citizen and start workflow"""
        await super()._post_save_create(saved_request, created_by)
        if self.workflow_engine:
            await self._start_workflow(saved_request)

    @trace()
    async def create_request(self, citizen_id: UUID, created_by: UUID, service_type: ServiceType, title: str, description: Optional[str]=None, channel: RequestChannel=RequestChannel.WEB, priority: RequestPriority=RequestPriority.MEDIUM, metadata: Dict[str, Any]=None, tags: List[str]=None) -> ServiceRequest:
        """Cria um novo pedido - delegates to BaseRequestService template method"""
        return await super().create_request(citizen_id=citizen_id, created_by=created_by, request_data={'service_type': service_type, 'title': title, 'description': description, 'channel': channel, 'priority': priority, 'metadata': metadata, 'tags': tags})

    @trace()
    async def _validate_create_request(self, citizen_id: UUID, request_data: Dict[str, Any], **kwargs) -> None:
        """
        Validação de criação com integração runtime:
        1) identidade civil (sempre)
        2) domínio específico por service_type (quando configurado)
        """
        _ = kwargs
        service_type = request_data.get('service_type')
        payload = dict(request_data.get('metadata') or {})
        service_value = service_type.value if isinstance(service_type, ServiceType) else str(service_type)
        if self.identidade_client is not None:
            ok, reason = await self.identidade_client.validate_payload(service_type=service_value, citizen_id=citizen_id, payload=payload)
            if not ok:
                raise ValueError(reason or 'Validação de identidade civil falhou')
        if not isinstance(service_type, ServiceType):
            service_type = ServiceType(service_type)
        domain_client = self._domain_clients.get(service_type)
        if domain_client is None:
            return
        ok, reason = await domain_client.validate_payload(service_type=service_type.value, citizen_id=citizen_id, payload=payload)
        if not ok:
            raise ValueError(reason or 'Payload inválido para o domínio solicitado')

    @trace()
    async def get_request(self, request_id: UUID, user_id: UUID, is_citizen: bool=False) -> Optional[ServiceRequest]:
        """Busca um pedido por ID com verificação de permissão"""
        return await super().get_request(request_id, user_id, is_citizen)

    @trace()
    async def list_citizen_requests(self, citizen_id: UUID, skip: int=0, limit: int=100) -> List[ServiceRequest]:
        """Lista pedidos de um cidadão"""
        requests, _ = await super().list_requests(skip=skip, limit=limit, citizen_id=citizen_id)
        return requests

    @trace()
    async def list_operator_requests(self, user_id: UUID, status: Optional[str]=None, skip: int=0, limit: int=100) -> List[ServiceRequest]:
        """
        Lista pedidos atribuídos a um operador
        """
        status_enum = ServiceRequestStatus(status) if status else None
        requests, _ = await self.repo.get_by_assignee(user_id, status_enum, skip, limit)
        return requests

    @trace()
    async def list_pending_requests(self, skip: int=0, limit: int=100) -> List[ServiceRequest]:
        """
        Lista pedidos pendentes (não atribuídos)
        """
        requests, _ = await self.repo.get_by_status(ServiceRequestStatus.SUBMITTED, skip, limit)
        return requests

    @trace()
    async def submit_request(self, request_id: UUID, submitted_by: UUID) -> ServiceRequest:
        """
        Submete um pedido (rascunho -> submetido)
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise ValueError('Pedido não encontrado')
        if request.created_by_user_id != submitted_by:
            raise PermissionError('Apenas o criador pode submeter o pedido')
        request.submit()
        saved = await self.repo.save(request)
        dispatch_data = await self._dispatch_submission(saved)
        if dispatch_data is not None:
            workflow_data = dict(saved.workflow_data or {})
            workflow_data['domain_dispatch'] = dispatch_data
            saved.workflow_data = workflow_data
            saved = await self.repo.save(saved)
        if self.workflow_engine:
            await self._start_workflow(saved)
        return saved

    @trace()
    async def assign_request(self, request_id: UUID, assigned_to: UUID, assigned_by: UUID) -> ServiceRequest:
        """
        Atribui um pedido a um operador
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise ValueError('Pedido não encontrado')
        request.assign(assigned_to, assigned_by)
        saved = await self.repo.save(request)
        if self.notification_svc:
            await self.notification_svc.notify_operator(user_id=assigned_to, title='Novo Pedido Atribuído', message=f'O pedido {saved.request_number} foi atribuído a você.', data={'request_id': str(saved.id)})
        return saved

    @trace()
    async def change_status(self, request_id: UUID, new_status: str, changed_by: UUID, reason: Optional[str]=None) -> ServiceRequest:
        """
        Altera o status de um pedido delegando �\xa0 base para notificações
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise ValueError('Pedido não encontrado')
        status_enum = ServiceRequestStatus(new_status)
        if not self._validate_status_transition(request.status, status_enum):
            raise ValueError(f'Transição de {request.status} para {status_enum} não permitida')
        return await self.update_status(request_id=request_id, new_status=new_status, updated_by=changed_by, reason=reason)

    @trace()
    async def link_workflow(self, request_id: UUID, workflow_instance_id: UUID) -> ServiceRequest:
        """
        Vincula workflow ao pedido
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise ValueError('Pedido não encontrado')
        request.link_workflow(workflow_instance_id)
        return await self.repo.save(request)

    @trace()
    async def search_requests(self, query: str, filters: dict=None, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """
        Pesquisa avançada de pedidos
        """
        return await self.repo.search(query, filters, skip, limit)

    @trace()
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Estatísticas gerais
        """
        return {'by_status': await self.repo.count_by_status(), 'total': sum((await self.repo.count_by_status()).values())}

    def _validate_status_transition(self, current: ServiceRequestStatus, new: ServiceRequestStatus) -> bool:
        """
        Valida transição de status
        """
        transitions = {ServiceRequestStatus.DRAFT: [ServiceRequestStatus.SUBMITTED, ServiceRequestStatus.CANCELLED], ServiceRequestStatus.SUBMITTED: [ServiceRequestStatus.UNDER_REVIEW, ServiceRequestStatus.REJECTED, ServiceRequestStatus.CANCELLED], ServiceRequestStatus.UNDER_REVIEW: [ServiceRequestStatus.IN_PROGRESS, ServiceRequestStatus.REJECTED, ServiceRequestStatus.WAITING_INFO], ServiceRequestStatus.IN_PROGRESS: [ServiceRequestStatus.COMPLETED, ServiceRequestStatus.WAITING_INFO], ServiceRequestStatus.WAITING_INFO: [ServiceRequestStatus.IN_PROGRESS, ServiceRequestStatus.CANCELLED], ServiceRequestStatus.APPROVED: [ServiceRequestStatus.COMPLETED], ServiceRequestStatus.REJECTED: [], ServiceRequestStatus.COMPLETED: [], ServiceRequestStatus.CANCELLED: [], ServiceRequestStatus.EXPIRED: []}
        return new in transitions.get(current, [])

    @trace()
    async def _start_workflow(self, request: ServiceRequest):
        """Inicia workflow para o pedido"""
        try:
            try:
                wf_instance = await self.workflow_engine.start_workflow(definition_key=request.service_type.value, business_key=str(request.id), variables={'citizen_id': str(request.citizen_id), 'request_id': str(request.id), 'request_number': request.request_number, 'title': request.title}, actor_id=request.created_by_user_id)
            except TypeError:
                wf_instance = await self.workflow_engine.start_workflow(definition_name=request.service_type.value, context={'citizen_id': str(request.citizen_id), 'request_id': str(request.id), 'request_number': request.request_number, 'title': request.title})
            wf_id = getattr(wf_instance, 'id', None)
            if wf_id is None and isinstance(wf_instance, dict):
                wf_id = wf_instance.get('instance_id') or wf_instance.get('id')
            if wf_id:
                request.link_workflow(UUID(str(wf_id)))
                await self.repo.save(request)
        except Exception as e:
            print(f'Erro ao iniciar workflow: {e}')

    async def _dispatch_submission(self, request: ServiceRequest) -> Dict[str, Any] | None:
        """Executa integração de submissão no client do domínio correspondente."""
        payload = dict(request.metadata or {})
        domain_client = self._domain_clients.get(request.service_type)
        if domain_client is None:
            return None
        return await domain_client.submit(service_type=request.service_type.value, request_id=request.id, citizen_id=request.citizen_id, payload=payload)