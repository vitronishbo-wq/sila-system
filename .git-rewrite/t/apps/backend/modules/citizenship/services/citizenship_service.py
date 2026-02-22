"""
Serviço principal para gestão de cidadania.

Este módulo implementa a lógica de negócio para:
- Gestão do catálogo de serviços
- Controle de solicitações de serviços
- Acompanhamento de status e histórico
- Integração com sistema de notificações
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import CitizenshipService, ServiceRequest
from ..models.citizen import Citizen
from ..schemas.citizenship import (
    CitizenshipServiceRead,
    ServiceCategory,
    ServiceRequestCreate,
    ServiceRequestRead,
    ServiceRequestStatus,
    ServiceStatus,
)

logger = logging.getLogger(__name__)


class CitizenshipService:
    """Classe principal para operações de cidadania."""

    @staticmethod
    async def get_available_services(
        db: AsyncSession, category: Optional[str] = None
    ) -> List[CitizenshipServiceRead]:
        """
        Busca serviços disponíveis no catálogo.

        Args:
            db: Sessão do banco de dados
            category: Categoria opcional para filtrar

        Returns:
            Lista de serviços disponíveis
        """
        try:
            query = db.query(CitizenshipService).filter(
                CitizenshipService.is_active == True
            )

            if category:
                query = query.filter(CitizenshipService.category == category)

            services = query.order_by(CitizenshipService.name).all()

            # Converter para schema de leitura
            result = []
            for service in services:
                service_dict = {
                    "id": service.id,
                    "code": service.code,
                    "name": service.name,
                    "description": service.description,
                    "category": service.category,
                    "estimated_days": service.estimated_days,
                    "requirements": service.requirements or [],
                    "is_active": service.is_active,
                    "created_at": service.created_at,
                    "updated_at": service.updated_at,
                }
                result.append(CitizenshipServiceRead(**service_dict))

            return result

        except Exception as e:
            logger.error(f"Erro ao buscar serviços: {e}")
            raise

    @staticmethod
    async def create_request(
        db: AsyncSession, citizen_id: UUID, request_data: ServiceRequestCreate
    ) -> ServiceRequestRead:
        """
        Cria uma nova solicitação de serviço.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão solicitante
            request_data: Dados da solicitação

        Returns:
            Dados da solicitação criada
        """
        try:
            # Buscar serviço solicitado
            service = (
                db.query(CitizenshipService)
                .filter(
                    CitizenshipService.code == request_data.service_code,
                    CitizenshipService.is_active == True,
                )
                .first()
            )

            if not service:
                raise ValueError(
                    f"Serviço {request_data.service_code} não encontrado ou inativo"
                )

            # Buscar dados do cidadão
            citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()
            if not citizen:
                raise ValueError("Cidadão não encontrado")

            # Gerar número de protocolo único
            protocol_number = f"CIT{datetime.now().strftime('%Y%m%d%H%M%S')}{citizen_id.hex[:8].upper()}"

            # Calcular data estimada de conclusão
            estimated_completion = datetime.utcnow() + timedelta(
                days=service.estimated_days
            )

            # Criar solicitação
            new_request = ServiceRequest(
                id=uuid4(),
                citizen_id=citizen_id,
                service_id=service.id,
                protocol_number=protocol_number,
                status=ServiceStatus.PENDING,
                priority=request_data.priority,
                observations=request_data.observations,
                contact_phone=request_data.contact_phone,
                contact_email=request_data.contact_email,
                estimated_completion=estimated_completion,
                created_at=datetime.utcnow(),
            )

            db.add(new_request)
            db.commit()
            db.refresh(new_request)

            # Converter para schema de leitura
            request_dict = {
                "id": new_request.id,
                "citizen_id": new_request.citizen_id,
                "service_code": request_data.service_code,
                "priority": new_request.priority,
                "observations": new_request.observations,
                "contact_phone": new_request.contact_phone,
                "contact_email": new_request.contact_email,
                "status": new_request.status,
                "protocol_number": new_request.protocol_number,
                "created_at": new_request.created_at,
                "updated_at": new_request.updated_at,
                "completed_at": new_request.completed_at,
                "service_name": service.name,
                "service_category": service.category,
                "estimated_completion": new_request.estimated_completion,
                "citizen_name": citizen.full_name,
                "citizen_document": citizen.document_id,
            }

            return ServiceRequestRead(**request_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar solicitação: {e}")
            raise

    @staticmethod
    async def get_user_requests(
        db: AsyncSession,
        citizen_id: UUID,
        status_filter: Optional[ServiceStatus] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ServiceRequestRead]:
        """
        Busca solicitações do usuário.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão
            status_filter: Filtro opcional por status
            skip: Offset para paginação
            limit: Limite de resultados

        Returns:
            Lista de solicitações do usuário
        """
        try:
            query = (
                db.query(ServiceRequest)
                .filter(ServiceRequest.citizen_id == citizen_id)
                .options(selectinload(ServiceRequest.service))
                .options(selectinload(ServiceRequest.citizen))
            )

            if status_filter:
                query = query.filter(ServiceRequest.status == status_filter)

            requests = (
                query.order_by(desc(ServiceRequest.created_at))
                .offset(skip)
                .limit(limit)
                .all()
            )

            result = []
            for request in requests:
                request_dict = {
                    "id": request.id,
                    "citizen_id": request.citizen_id,
                    "service_code": request.service.code,
                    "priority": request.priority,
                    "observations": request.observations,
                    "contact_phone": request.contact_phone,
                    "contact_email": request.contact_email,
                    "status": request.status,
                    "protocol_number": request.protocol_number,
                    "created_at": request.created_at,
                    "updated_at": request.updated_at,
                    "completed_at": request.completed_at,
                    "service_name": request.service.name,
                    "service_category": request.service.category,
                    "estimated_completion": request.estimated_completion,
                    "citizen_name": request.citizen.full_name,
                    "citizen_document": request.citizen.document_id,
                }
                result.append(ServiceRequestRead(**request_dict))

            return result

        except Exception as e:
            logger.error(f"Erro ao buscar solicitações do usuário: {e}")
            raise

    @staticmethod
    async def get_request_by_id(
        db: AsyncSession, request_id: UUID, citizen_id: UUID
    ) -> Optional[ServiceRequestRead]:
        """
        Busca solicitação específica por ID.

        Args:
            db: Sessão do banco de dados
            request_id: ID da solicitação
            citizen_id: ID do cidadão (para verificação de permissão)

        Returns:
            Dados da solicitação ou None se não encontrada
        """
        try:
            request = (
                db.query(ServiceRequest)
                .filter(
                    ServiceRequest.id == request_id,
                    ServiceRequest.citizen_id == citizen_id,
                )
                .options(selectinload(ServiceRequest.service))
                .options(selectinload(ServiceRequest.citizen))
                .first()
            )

            if not request:
                return None

            request_dict = {
                "id": request.id,
                "citizen_id": request.citizen_id,
                "service_code": request.service.code,
                "priority": request.priority,
                "observations": request.observations,
                "contact_phone": request.contact_phone,
                "contact_email": request.contact_email,
                "status": request.status,
                "protocol_number": request.protocol_number,
                "created_at": request.created_at,
                "updated_at": request.updated_at,
                "completed_at": request.completed_at,
                "service_name": request.service.name,
                "service_category": request.service.category,
                "estimated_completion": request.estimated_completion,
                "citizen_name": request.citizen.full_name,
                "citizen_document": request.citizen.document_id,
            }

            return ServiceRequestRead(**request_dict)

        except Exception as e:
            logger.error(f"Erro ao buscar solicitação por ID: {e}")
            raise

    @staticmethod
    async def cancel_request(
        db: AsyncSession, request_id: UUID, citizen_id: UUID
    ) -> Optional[ServiceRequestRead]:
        """
        Cancela uma solicitação de serviço.

        Args:
            db: Sessão do banco de dados
            request_id: ID da solicitação
            citizen_id: ID do cidadão

        Returns:
            Dados da solicitação cancelada ou None se não encontrada/pode ser cancelada
        """
        try:
            request = (
                db.query(ServiceRequest)
                .filter(
                    ServiceRequest.id == request_id,
                    ServiceRequest.citizen_id == citizen_id,
                )
                .first()
            )

            if not request:
                return None

            # Verificar se pode ser cancelada
            if request.status in [ServiceStatus.COMPLETED, ServiceStatus.CANCELLED]:
                return None

            # Atualizar status
            request.status = ServiceStatus.CANCELLED
            request.updated_at = datetime.utcnow()

            db.commit()

            # Recarregar para obter dados atualizados
            db.refresh(request)

            # Buscar dados relacionados para o retorno
            service = (
                db.query(CitizenshipService)
                .filter(CitizenshipService.id == request.service_id)
                .first()
            )
            citizen = db.query(Citizen).filter(Citizen.id == request.citizen_id).first()

            request_dict = {
                "id": request.id,
                "citizen_id": request.citizen_id,
                "service_code": service.code,
                "priority": request.priority,
                "observations": request.observations,
                "contact_phone": request.contact_phone,
                "contact_email": request.contact_email,
                "status": request.status,
                "protocol_number": request.protocol_number,
                "created_at": request.created_at,
                "updated_at": request.updated_at,
                "completed_at": request.completed_at,
                "service_name": service.name,
                "service_category": service.category,
                "estimated_completion": request.estimated_completion,
                "citizen_name": citizen.full_name,
                "citizen_document": citizen.document_id,
            }

            return ServiceRequestRead(**request_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao cancelar solicitação: {e}")
            raise

    @staticmethod
    async def get_request_status(
        db: AsyncSession, request_id: UUID, citizen_id: UUID
    ) -> Optional[ServiceRequestStatus]:
        """
        Busca informações de status de uma solicitação.

        Args:
            db: Sessão do banco de dados
            request_id: ID da solicitação
            citizen_id: ID do cidadão

        Returns:
            Informações de status ou None se não encontrada
        """
        try:
            request = (
                db.query(ServiceRequest)
                .filter(
                    ServiceRequest.id == request_id,
                    ServiceRequest.citizen_id == citizen_id,
                )
                .first()
            )

            if not request:
                return None

            # Calcular progresso baseado no status
            progress_map = {
                ServiceStatus.PENDING: 10,
                ServiceStatus.IN_REVIEW: 30,
                ServiceStatus.PROCESSING: 60,
                ServiceStatus.COMPLETED: 100,
                ServiceStatus.CANCELLED: 0,
                ServiceStatus.REJECTED: 0,
            }

            status_dict = {
                "id": request.id,
                "status": request.status,
                "protocol_number": request.protocol_number,
                "service_name": request.service.name,
                "created_at": request.created_at,
                "estimated_completion": request.estimated_completion,
                "current_step": _get_current_step(request.status),
                "progress_percentage": progress_map.get(request.status, 0),
            }

            return ServiceRequestStatus(**status_dict)

        except Exception as e:
            logger.error(f"Erro ao buscar status da solicitação: {e}")
            raise


def _get_current_step(status: ServiceStatus) -> str:
    """Retorna a etapa atual baseada no status."""
    step_map = {
        ServiceStatus.PENDING: "Aguardando análise inicial",
        ServiceStatus.IN_REVIEW: "Em análise pela equipe",
        ServiceStatus.PROCESSING: "Em processamento",
        ServiceStatus.COMPLETED: "Concluída",
        ServiceStatus.CANCELLED: "Cancelada pelo solicitante",
        ServiceStatus.REJECTED: "Rejeitada",
    }
    return step_map.get(status, "Status desconhecido")


# Dados iniciais de serviços (para desenvolvimento)
DEFAULT_SERVICES = [
    {
        "code": "CERT_NASC",
        "name": "Certidão de Nascimento",
        "description": "Emissão de certidão de nascimento",
        "category": ServiceCategory.CERTIDOES,
        "estimated_days": 5,
        "requirements": ["Certidão de nascimento original", "Documento de identidade"],
    },
    {
        "code": "CERT_CAS",
        "name": "Certidão de Casamento",
        "description": "Emissão de certidão de casamento",
        "category": ServiceCategory.CERTIDOES,
        "estimated_days": 7,
        "requirements": ["Certidão de casamento original", "Documento de identidade"],
    },
    {
        "code": "CERT_OBITO",
        "name": "Certidão de Óbito",
        "description": "Emissão de certidão de óbito",
        "category": ServiceCategory.CERTIDOES,
        "estimated_days": 3,
        "requirements": ["Declaração de óbito", "Documento de identidade do falecido"],
    },
    {
        "code": "ATUAL_END",
        "name": "Atualização de Endereço",
        "description": "Atualização de endereço residencial",
        "category": ServiceCategory.REGISTROS,
        "estimated_days": 10,
        "requirements": ["Comprovante de residência", "Documento de identidade"],
    },
]
