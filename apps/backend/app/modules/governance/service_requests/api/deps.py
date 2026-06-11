from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_identity_context, get_notification_service, get_scope_from_user
from apps.backend.app.core.bridges import CitizenRepository
from apps.backend.app.core.bridges.society_repository_bridges import (
    make_assistencia_beneficiario_repository,
    make_educacao_turma_repository,
    make_emprego_candidato_repository,
    make_juventude_jovem_repository,
    make_juventude_programa_repository,
    make_saude_health_unit_repository,
)
from apps.backend.app.core.db import get_session
from apps.backend.app.core.notifications.services.notification_service import NotificationService

from ..application.services.request_service import RequestService
from ..infrastructure.clients import (
    AssistenciaClient,
    EducacaoClient,
    EmpregoClient,
    IdentidadeClient,
    JuventudeClient,
    SaudeClient,
)
from ..infrastructure.repositories.request_repository import RequestRepository

session_dep = Depends(get_session)
notification_service_dep = Depends(get_notification_service)
identity_dep = Depends(get_identity_context)


class RequestPermissions:
    """Verificações de permissão para pedidos"""

    @staticmethod
    def can_view_request(request_citizen_id: UUID, identity) -> bool:
        """Verifica se pode visualizar pedido"""
        if identity.is_superuser:
            return True
        if identity.is_citizen and identity.citizen_id == str(request_citizen_id):
            return True
        if identity.has_permission("service_request", "view"):
            return True
        return False

    @staticmethod
    def can_update_request(request, identity) -> bool:
        """Verifica se pode atualizar pedido"""
        if identity.is_superuser:
            return True
        if request.assigned_to_user_id and str(request.assigned_to_user_id) == identity.user_id:
            return True
        if identity.has_permission("service_request", "update"):
            return True
        return False

    @staticmethod
    def can_assign_request(identity) -> bool:
        """Verifica se pode atribuir pedidos"""
        return identity.is_superuser or identity.has_permission("service_request", "assign")


async def get_request_service(
    db: AsyncSession = session_dep,
    notification_service: NotificationService = notification_service_dep,
    scope: dict = Depends(get_scope_from_user),
) -> RequestService:
    """Dependency para obter serviço de pedidos (ASYNC)"""
    repository = RequestRepository(db)
    # Apply territorial scope (set by outer dependency)
    # Attach allowed territories resolved via DI (None == unrestricted)
    try:
        repository.allowed_territories = scope.get("allowed_territories") if isinstance(scope, dict) else None
    except Exception:
        repository.allowed_territories = None
    identidade_client = IdentidadeClient(citizen_repo=CitizenRepository(db))
    educacao_client = EducacaoClient(turma_repo=make_educacao_turma_repository(db))
    juventude_client = JuventudeClient(
        jovem_repo=make_juventude_jovem_repository(db),
        programa_repo=make_juventude_programa_repository(db),
    )
    emprego_client = EmpregoClient(candidato_repo=make_emprego_candidato_repository(db))
    saude_client = SaudeClient(health_unit_repo=make_saude_health_unit_repository(db))
    assistencia_client = AssistenciaClient(
        beneficiario_repo=make_assistencia_beneficiario_repository(db)
    )
    return RequestService(
        db=db,
        repository=repository,
        notification_service=notification_service,
        identidade_client=identidade_client,
        educacao_client=educacao_client,
        juventude_client=juventude_client,
        emprego_client=emprego_client,
        saude_client=saude_client,
        assistencia_client=assistencia_client,
    )

request_service_dep = Depends(get_request_service)


async def get_request_or_404(
    request_id: UUID,
    service: RequestService = request_service_dep,
    identity=identity_dep,
):
    """Dependency para buscar pedido com verificação de acesso"""
    request = await service.get_request(
        request_id,
        UUID(identity.user_id) if identity else request_id,
        identity.is_citizen if identity else False,
    )
    if not request:
        from apps.backend.app.core.exceptions import RequestNotFoundError

        raise RequestNotFoundError(request_id).to_http_exception()
    return request


def require_request_permission(permission: str):
    """Dependency para verificar permissão em pedido"""

    request_dep = Depends(get_request_or_404)

    async def decorator(request=request_dep, identity=identity_dep):
        from apps.backend.app.core.exceptions import AccessDeniedError

        if permission == "view":
            if identity and (not RequestPermissions.can_view_request(request.citizen_id, identity)):
                raise AccessDeniedError("acessar este pedido").to_http_exception()
        elif permission == "update":
            if identity and (not RequestPermissions.can_update_request(request, identity)):
                raise AccessDeniedError("modificar este pedido").to_http_exception()
        elif permission == "assign":
            if identity and (not RequestPermissions.can_assign_request(identity)):
                raise AccessDeniedError("atribuir pedidos").to_http_exception()
        return request

    return decorator
