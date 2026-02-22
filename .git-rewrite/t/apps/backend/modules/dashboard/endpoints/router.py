from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_session
from modules.auth.auth_utils import get_current_active_user

from ..schemas.dashboard_stats import DashboardStatsSummary
from ..services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/ping")
async def ping():
    """Health check do módulo dashboard."""
    return {"status": "ok", "module": "dashboard"}


@router.get("/stats", response_model=DashboardStatsSummary)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """
    Retorna estatísticas gerais consolidadas do sistema
    para o painel administrativo principal.

    Requer autenticação JWT.
    """
    try:
        dashboard_service = DashboardService(db)

        # Buscar estatísticas usando o serviço
        stats = await dashboard_service.get_stats_summary()

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}",
        )


@router.get("/service-stats")
async def get_service_stats(
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """
    Retorna métricas detalhadas por serviço/módulo
    para análise de performance individual.

    Args:
        module: Nome do módulo específico (opcional)

    Requer autenticação JWT.
    """
    try:
        dashboard_service = DashboardService(db)

        # Buscar estatísticas por serviço usando o serviço
        stats = await dashboard_service.get_service_stats(module)

        return {"status": "success", "data": stats, "timestamp": "2024-01-15T10:00:00Z"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas de serviços: {str(e)}",
        )


@router.get("/health")
async def get_system_health(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """
    Retorna status de saúde completo de todos os serviços
    para monitoramento em tempo real.

    Requer autenticação JWT.
    """
    try:
        # Verificação básica de saúde dos serviços
        # TODO: Implementar verificações reais de saúde

        health_status = {
            "status": "healthy",
            "services": [
                {
                    "name": "database",
                    "status": "up",
                    "responseTime": 45,
                    "lastCheck": "2024-01-15T10:00:00Z",
                },
                {
                    "name": "api",
                    "status": "up",
                    "responseTime": 23,
                    "lastCheck": "2024-01-15T10:00:00Z",
                },
                {
                    "name": "cache",
                    "status": "up",
                    "responseTime": 12,
                    "lastCheck": "2024-01-15T10:00:00Z",
                },
                {
                    "name": "file_storage",
                    "status": "up",
                    "responseTime": 67,
                    "lastCheck": "2024-01-15T10:00:00Z",
                },
            ],
            "overallUptime": "99.8%",
            "lastIncident": None,
            "timestamp": "2024-01-15T10:00:00Z",
        }

        return {"status": "success", "data": health_status}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar saúde do sistema: {str(e)}",
        )


@router.get("/activities")
async def get_recent_activities(
    limit: int = 10,
    activity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """
    Retorna atividades recentes do sistema
    para feed de informações do dashboard.

    Args:
        limit: Número máximo de atividades (máx 100)
        activity_type: Tipo específico de atividade (opcional)

    Requer autenticação JWT.
    """
    try:
        if limit > 100:
            limit = 100

        # Dados mockados para desenvolvimento
        # TODO: Implementar consulta real de atividades

        activities = [
            {
                "id": "1",
                "type": "user_registration",
                "title": "Novo usuário registrado",
                "description": "Usuário admin@sila.gov.ao registrado no sistema",
                "severity": "info",
                "timestamp": "2024-01-15T10:30:00Z",
                "userId": "user-123",
                "module": "auth",
            },
            {
                "id": "2",
                "type": "system_backup",
                "title": "Backup automático concluído",
                "description": "Backup completo do sistema realizado com sucesso",
                "severity": "success",
                "timestamp": "2024-01-15T09:00:00Z",
                "userId": "system",
                "module": "system",
            },
            {
                "id": "3",
                "type": "service_request",
                "title": "Nova solicitação de serviço",
                "description": "Solicitação de emissão de RG registrada",
                "severity": "info",
                "timestamp": "2024-01-15T09:45:00Z",
                "userId": "user-456",
                "module": "citizenship",
            },
            {
                "id": "4",
                "type": "appointment_scheduled",
                "title": "Consulta médica agendada",
                "description": "Consulta de clínica geral agendada para 16/01/2024",
                "severity": "info",
                "timestamp": "2024-01-15T08:30:00Z",
                "userId": "user-789",
                "module": "health",
            },
            {
                "id": "5",
                "type": "license_approved",
                "title": "Licença comercial aprovada",
                "description": "Alvará de funcionamento aprovado para Empresa XYZ",
                "severity": "success",
                "timestamp": "2024-01-15T08:15:00Z",
                "userId": "user-101",
                "module": "commercial",
            },
        ]

        # Aplicar filtros
        filtered_activities = activities[:limit]

        if activity_type:
            filtered_activities = [
                activity
                for activity in filtered_activities
                if activity["type"] == activity_type
            ]

        return {
            "status": "success",
            "data": filtered_activities,
            "total": len(filtered_activities),
            "timestamp": "2024-01-15T10:00:00Z",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar atividades recentes: {str(e)}",
        )


@router.get("/chart")
async def get_dashboard_chart(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """Retorna dados de gráfico de documentos por mês."""
    return [
        {"mes": "Jan", "documentos": 120},
        {"mes": "Fev", "documentos": 210},
        {"mes": "Mar", "documentos": 340},
        {"mes": "Abr", "documentos": 510},
        {"mes": "Mai", "documentos": 780},
    ]


@router.get("/alerts")
async def get_dashboard_alerts(
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
):
    """Retorna alertas operacionais do dashboard."""
    return [
        {"msg": "17 documentos aguardam validação", "nivel": "warning"},
        {"msg": "Backup automático executado com sucesso", "nivel": "info"},
    ]
