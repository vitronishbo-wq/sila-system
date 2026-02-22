"""
Endpoints RESTful para o módulo de Notificações.

Este módulo implementa os endpoints completos para:
- Gestão completa de notificações multicanal
- Templates reutilizáveis de mensagens
- Controle de fila e agendamento
- Eventos automáticos e configurações
- Webhooks para integração externa
- Estatísticas e relatórios detalhados
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth_utils import get_current_active_user
from core.db.session import get_db
from modules.citizenship.models.citizen import Citizen
from modules.notifications.models.notification_models import (
    NotificationSettings,
    NotificationTemplate,
)
from modules.notifications.schemas.notifications import (
    NotificationCreate,
    NotificationFilters,
    NotificationRead,
    NotificationStatistics,
    NotificationTemplateCreate,
    NotificationTemplateRead,
)
from modules.notifications.services.notification_service import NotificationService

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Health check do módulo Notifications.

    Verifica se o módulo está operacional e retorna informações básicas.
    """
    return {
        "status": "healthy",
        "module": "notifications",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "features": [
            "multi_channel_notifications",
            "template_management",
            "queue_processing",
            "event_automation",
            "webhook_integration",
            "statistics_reporting",
        ],
    }


@router.get("/user", response_model=List[NotificationRead])
async def get_user_notifications(
    notification_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridade"),
    read_status: Optional[bool] = Query(
        None, description="Filtrar por status de leitura"
    ),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Lista notificações do usuário autenticado.

    Retorna notificações recebidas com filtros e paginação.
    """
    try:
        # Construir filtros
        filters = NotificationFilters(
            notification_type=notification_type,
            status=status,
            priority=priority,
            read_status=read_status,
        )

        notifications, _ = await NotificationService.get_user_notifications(
            db=db, user_id=current_user.id, filters=filters, page=page, size=size
        )

        return notifications

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar notificações: {str(e)}",
        )


@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Cria nova notificação individual.

    Permite envio personalizado de notificação para usuário específico.
    """
    try:
        notification = await NotificationService.create_notification(
            db=db, notification_data=notification_data, sender_id=current_user.id
        )

        return notification

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar notificação: {str(e)}",
        )


@router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Marca notificação como lida.

    Atualiza status da notificação para indicar que foi visualizada.
    """
    try:
        notification_id_uuid = UUID(notification_id)

        success = await NotificationService.mark_notification_read(
            db=db, notification_id=notification_id_uuid, user_id=current_user.id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificação não encontrada ou já marcada como lida",
            )

        return {"detail": "Notificação marcada como lida"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de notificação inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao marcar notificação como lida: {str(e)}",
        )


@router.get("/statistics/me", response_model=NotificationStatistics)
async def get_my_notification_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém estatísticas pessoais de notificações.

    Retorna métricas detalhadas sobre notificações recebidas.
    """
    try:
        stats = await NotificationService.get_notification_statistics(
            db=db, user_id=current_user.id
        )

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estatísticas: {str(e)}",
        )


@router.post("/process-queue", status_code=status.HTTP_200_OK)
async def process_notification_queue(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Dispara processamento manual da fila de notificações.

    Útil para testes e manutenção do sistema de notificações.
    """
    try:
        # Verificar se usuário tem permissão (apenas admin)
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem processar a fila manualmente",
            )

        # Executar processamento em background
        background_tasks.add_task(NotificationService.process_notification_queue, db)

        return {
            "detail": "Processamento da fila iniciado em background",
            "status": "processing",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar fila: {str(e)}",
        )


@router.get("/templates", response_model=List[NotificationTemplateRead])
async def get_notification_templates(
    notification_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    is_active: Optional[bool] = Query(True, description="Filtrar por status ativo"),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Lista templates de notificação disponíveis.

    Retorna templates criados pelo usuário ou públicos.
    """
    try:
        query = db.query(NotificationTemplate).filter(
            NotificationTemplate.is_active == is_active
        )

        # Filtrar por tipo se especificado
        if notification_type:
            query = query.filter(
                NotificationTemplate.notification_type == notification_type
            )

        # Incluir templates públicos ou do próprio usuário
        query = query.filter(
            or_(
                NotificationTemplate.is_public == True,
                NotificationTemplate.created_by == current_user.id,
            )
        )

        templates = query.order_by(NotificationTemplate.name).all()

        # Converter para schema de leitura
        result = []
        for template in templates:
            template_dict = {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "notification_type": template.notification_type,
                "subject": template.subject,
                "body": template.body,
                "variables": template.variables or {},
                "is_active": template.is_active,
                "created_by": template.created_by,
                "created_at": template.created_at,
                "updated_at": template.updated_at,
                "usage_count": template.usage_count,
            }
            result.append(NotificationTemplateRead(**template_dict))

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar templates: {str(e)}",
        )


@router.post(
    "/templates",
    response_model=NotificationTemplateRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_notification_template(
    template_data: NotificationTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Cria novo template de notificação.

    Permite criar templates reutilizáveis para notificações padronizadas.
    """
    try:
        # Criar template
        new_template = NotificationTemplate(
            name=template_data.name,
            description=template_data.description,
            notification_type=template_data.notification_type,
            subject=template_data.subject,
            body=template_data.body,
            variables=template_data.variables,
            is_active=template_data.is_active,
            created_by=current_user.id,
            is_public=False,  # Por padrão, apenas criador pode usar
        )

        db.add(new_template)
        db.commit()
        db.refresh(new_template)

        # Converter para schema de leitura
        template_dict = {
            "id": new_template.id,
            "name": new_template.name,
            "description": new_template.description,
            "notification_type": new_template.notification_type,
            "subject": new_template.subject,
            "body": new_template.body,
            "variables": new_template.variables or {},
            "is_active": new_template.is_active,
            "created_by": new_template.created_by,
            "created_at": new_template.created_at,
            "updated_at": new_template.updated_at,
            "usage_count": new_template.usage_count,
        }

        return NotificationTemplateRead(**template_dict)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar template: {str(e)}",
        )


@router.get("/settings/me")
async def get_my_notification_settings(
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém configurações de notificação do usuário.

    Retorna preferências pessoais de recebimento de notificações.
    """
    try:
        settings = (
            db.query(NotificationSettings)
            .filter(NotificationSettings.user_id == current_user.id)
            .first()
        )

        if not settings:
            # Criar configurações padrão se não existirem
            settings = NotificationSettings(
                user_id=current_user.id,
                email_notifications=True,
                sms_notifications=False,
                push_notifications=True,
                in_app_notifications=True,
                notification_frequency="immediate",
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)

        # Converter para schema de leitura
        settings_dict = {
            "id": settings.id,
            "user_id": settings.user_id,
            "email_notifications": settings.email_notifications,
            "sms_notifications": settings.sms_notifications,
            "push_notifications": settings.push_notifications,
            "in_app_notifications": settings.in_app_notifications,
            "notification_frequency": settings.notification_frequency,
            "quiet_hours_start": settings.quiet_hours_start,
            "quiet_hours_end": settings.quiet_hours_end,
            "created_at": settings.created_at,
            "updated_at": settings.updated_at,
        }

        return settings_dict

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter configurações: {str(e)}",
        )


@router.patch("/settings/me")
async def update_my_notification_settings(
    email_notifications: Optional[bool] = None,
    sms_notifications: Optional[bool] = None,
    push_notifications: Optional[bool] = None,
    in_app_notifications: Optional[bool] = None,
    notification_frequency: Optional[str] = None,
    quiet_hours_start: Optional[str] = None,
    quiet_hours_end: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Atualiza configurações de notificação do usuário.

    Permite personalizar preferências de recebimento.
    """
    try:
        settings = (
            db.query(NotificationSettings)
            .filter(NotificationSettings.user_id == current_user.id)
            .first()
        )

        if not settings:
            # Criar configurações padrão
            settings = NotificationSettings(user_id=current_user.id)
            db.add(settings)

        # Atualizar campos fornecidos
        if email_notifications is not None:
            settings.email_notifications = email_notifications
        if sms_notifications is not None:
            settings.sms_notifications = sms_notifications
        if push_notifications is not None:
            settings.push_notifications = push_notifications
        if in_app_notifications is not None:
            settings.in_app_notifications = in_app_notifications
        if notification_frequency is not None:
            settings.notification_frequency = notification_frequency
        if quiet_hours_start is not None:
            settings.quiet_hours_start = quiet_hours_start
        if quiet_hours_end is not None:
            settings.quiet_hours_end = quiet_hours_end

        settings.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(settings)

        return {"detail": "Configurações atualizadas com sucesso"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar configurações: {str(e)}",
        )


@router.post("/test-notification")
async def send_test_notification(
    notification_type: str = "email",
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Envia notificação de teste para o usuário atual.

    Útil para testar configurações e canais de entrega.
    """
    try:
        # Criar notificação de teste
        test_data = NotificationCreate(
            recipient_id=current_user.id,
            recipient_email=getattr(current_user, "email", None),
            notification_type=notification_type,
            priority="normal",
            channels=[notification_type],
            subject="Notificação de Teste - SILA System",
            body=f"Esta é uma notificação de teste enviada em {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}. Se você recebeu esta mensagem, o sistema de notificações está funcionando corretamente.",
            variables={"test_time": datetime.utcnow().isoformat()},
            metadata={"test_notification": True},
        )

        notification = await NotificationService.create_notification(
            db=db, notification_data=test_data, sender_id=current_user.id
        )

        return {
            "detail": "Notificação de teste enviada",
            "notification_id": str(notification.id),
            "channels": notification.channels,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao enviar notificação de teste: {str(e)}",
        )
