from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, desc, func, select, and_
from ...domain.models.service_request import ServiceRequest
from ...domain.enums import ServiceRequestStatus, ServiceType
from ..models.service_request_model import ServiceRequestModel
from ...application.ports.request_repository_port import RequestRepositoryPort

class RequestRepository(RequestRepositoryPort):
    """Implementação do repositório de pedidos (ASYNC)"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, request: ServiceRequest) -> ServiceRequest:
        """Salva um pedido"""
        model_data = {'id': request.id, 'request_number': request.request_number, 'citizen_id': request.citizen_id, 'created_by_user_id': request.created_by_user_id, 'assigned_to_user_id': request.assigned_to_user_id, 'service_type': request.service_type.value, 'title': request.title, 'description': request.description, 'status': request.status.value, 'priority': request.priority.value, 'channel': request.channel.value, 'workflow_instance_id': request.workflow_instance_id, 'workflow_data': request.workflow_data, 'metadata_': request.metadata, 'tags': request.tags, 'created_at': request.created_at, 'updated_at': request.updated_at, 'submitted_at': request.submitted_at, 'completed_at': request.completed_at, 'deadline': request.deadline, 'sla_due_at': request.sla_due_at, 'sla_breached': request.sla_breached}
        stmt = select(ServiceRequestModel).where(ServiceRequestModel.id == request.id)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            for key, value in model_data.items():
                if value is not None:
                    setattr(existing, key, value)
            await self.db.flush()
            return self._to_domain(existing)
        else:
            model = ServiceRequestModel(**model_data)
            self.db.add(model)
            await self.db.flush()
            return self._to_domain(model)

    async def get_by_id(self, request_id: UUID) -> Optional[ServiceRequest]:
        """Busca pedido por ID"""
        stmt = select(ServiceRequestModel).where(ServiceRequestModel.id == request_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_number(self, request_number: str) -> Optional[ServiceRequest]:
        """Busca pedido por número"""
        stmt = select(ServiceRequestModel).where(ServiceRequestModel.request_number == request_number)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Busca pedidos por cidadão"""
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(ServiceRequestModel.citizen_id == citizen_id)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(ServiceRequestModel.citizen_id == citizen_id).order_by(desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def get_by_assignee(self, user_id: UUID, status: Optional[ServiceRequestStatus]=None, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Busca pedidos atribuídos a um usuário"""
        where_clause = ServiceRequestModel.assigned_to_user_id == user_id
        if status:
            where_clause = and_(where_clause, ServiceRequestModel.status == status.value)
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(where_clause)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(where_clause).order_by(desc(ServiceRequestModel.priority), desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def get_by_status(self, status: ServiceRequestStatus, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Busca pedidos por status"""
        where_clause = ServiceRequestModel.status == status.value
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(where_clause)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(where_clause).order_by(desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def get_by_service_type(self, service_type: ServiceType, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Busca pedidos por tipo de serviço"""
        where_clause = ServiceRequestModel.service_type == service_type.value
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(where_clause)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(where_clause).order_by(desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def get_by_date_range(self, start_date: datetime, end_date: datetime, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Busca pedidos por intervalo de datas"""
        where_clause = ServiceRequestModel.created_at.between(start_date, end_date)
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(where_clause)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(where_clause).order_by(desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def search(self, query: str, filters: dict=None, skip: int=0, limit: int=100) -> Tuple[List[ServiceRequest], int]:
        """Pesquisa avançada de pedidos"""
        where_clauses = []
        if query:
            where_clauses.append(or_(ServiceRequestModel.request_number.ilike(f'%{query}%'), ServiceRequestModel.title.ilike(f'%{query}%'), ServiceRequestModel.description.ilike(f'%{query}%')))
        if filters:
            if filters.get('status'):
                where_clauses.append(ServiceRequestModel.status == filters['status'])
            if filters.get('priority'):
                where_clauses.append(ServiceRequestModel.priority == filters['priority'])
            if filters.get('service_type'):
                where_clauses.append(ServiceRequestModel.service_type == filters['service_type'])
            if filters.get('citizen_id'):
                where_clauses.append(ServiceRequestModel.citizen_id == filters['citizen_id'])
            if filters.get('assigned_to'):
                where_clauses.append(ServiceRequestModel.assigned_to_user_id == filters['assigned_to'])
        combined_where = where_clauses[0] if len(where_clauses) == 1 else and_(*where_clauses) if where_clauses else True
        count_stmt = select(func.count()).select_from(ServiceRequestModel).where(combined_where)
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        stmt = select(ServiceRequestModel).where(combined_where).order_by(desc(ServiceRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._to_domain(m) for m in models], total)

    async def count_by_status(self) -> dict:
        """Contagem de pedidos por status"""
        stmt = select(ServiceRequestModel.status, func.count().label('count')).group_by(ServiceRequestModel.status)
        result = await self.db.execute(stmt)
        rows = result.all()
        return {r.status: r.count for r in rows}

    async def get_next_sequence(self, year: int) -> int:
        """Próximo número sequencial do ano"""
        pattern = f'SR/{year}/%'
        stmt = select(func.count()).select_from(ServiceRequestModel).where(ServiceRequestModel.request_number.like(pattern))
        result = await self.db.execute(stmt)
        count = result.scalar() or 0
        return count + 1

    def _to_domain(self, model: ServiceRequestModel) -> Optional[ServiceRequest]:
        """Converte model para domain object"""
        if not model:
            return None
        from ...domain.enums import ServiceRequestStatus, ServiceType, RequestChannel, RequestPriority
        status_value = model.status
        legacy_status_map = {'RASCUNHO': ServiceRequestStatus.DRAFT.value, 'RECEBIDO': ServiceRequestStatus.SUBMITTED.value, 'SUBMETIDO': ServiceRequestStatus.SUBMITTED.value, 'EM_ANALISE': ServiceRequestStatus.UNDER_REVIEW.value, 'EM_ANDAMENTO': ServiceRequestStatus.IN_PROGRESS.value, 'AGUARDANDO_INFO': ServiceRequestStatus.WAITING_INFO.value, 'APROVADO': ServiceRequestStatus.APPROVED.value, 'REJEITADO': ServiceRequestStatus.REJECTED.value, 'CONCLUIDO': ServiceRequestStatus.COMPLETED.value, 'CANCELADO': ServiceRequestStatus.CANCELLED.value, 'EXPIRADO': ServiceRequestStatus.EXPIRED.value}
        status_value = legacy_status_map.get(status_value, status_value)
        channel_value = model.channel
        legacy_channel_map = {'WEB': 'web', 'MOBILE': 'mobile', 'COUNTER': 'counter', 'EMAIL': 'email', 'API': 'api', 'WHATSAPP': 'whatsapp'}
        channel_value = legacy_channel_map.get(channel_value, channel_value)
        priority_value = model.priority
        legacy_priority_map = {'MEDIUM': 'medium', 'LOW': 'low', 'HIGH': 'high', 'URGENT': 'urgent', 'CRITICAL': 'critical', 'MEDIA': 'medium', 'BAIXA': 'low', 'ALTA': 'high', 'URGENTE': 'urgent', 'CRITICA': 'critical'}
        if priority_value in legacy_priority_map:
            priority_value = legacy_priority_map[priority_value]
        service_type_value = model.service_type
        legacy_service_type_map = {'DOCUMENT_REQUEST': ServiceType.IDENTITY_BI.value, 'DOCUMENT': ServiceType.IDENTITY_BI.value, 'GENERAL': ServiceType.GENERAL_SUPPORT.value}
        service_type_value = legacy_service_type_map.get(service_type_value, service_type_value)
        request = ServiceRequest(id=model.id, request_number=model.request_number, citizen_id=model.citizen_id, created_by_user_id=model.created_by_user_id, assigned_to_user_id=model.assigned_to_user_id, service_type=ServiceType(service_type_value), title=model.title, description=model.description, status=ServiceRequestStatus(status_value), priority=RequestPriority(priority_value), channel=RequestChannel(channel_value), workflow_instance_id=model.workflow_instance_id, workflow_data=model.workflow_data or {}, metadata=model.metadata_ or {}, tags=model.tags or [], created_at=model.created_at, updated_at=model.updated_at, submitted_at=model.submitted_at, completed_at=model.completed_at, deadline=model.deadline, sla_due_at=model.sla_due_at, sla_breached=model.sla_breached)
        return request