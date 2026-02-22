"""
Endpoints RESTful para o módulo de Analytics.

Este módulo implementa os endpoints completos para:
- Dashboards executivos e métricas estratégicas
- Relatórios personalizáveis e análises de dados
- Métricas em tempo real e indicadores de performance
- Sistema de alertas baseados em thresholds
- Cache inteligente para performance otimizada
- Exportação de dados em múltiplos formatos
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_db
from modules.analytics.models.analytics_models import (
    Metric,
    Report,
)
from modules.analytics.schemas.analytics_schemas import (
    AlertRead,
    AnalyticsFilters,
    AnalyticsSummary,
    DashboardData,
    ExecutiveKPIs,
    MetricRead,
    ReportData,
    ReportGenerationRequest,
)
from modules.analytics.services.analytics_service import AnalyticsService
from core.security import get_current_active_user
from modules.citizenship.models.citizen import Citizen

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Health check do módulo Analytics.

    Verifica se o módulo está operacional e retorna informações básicas.
    """
    return {
        "status": "healthy",
        "module": "analytics",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "features": [
            "executive_dashboards",
            "custom_reports",
            "realtime_metrics",
            "trend_analysis",
            "alert_system",
            "data_export",
            "caching_system",
        ],
    }


@router.get("/dashboard/executive", response_model=ExecutiveKPIs)
async def get_executive_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém dashboard executivo com KPIs principais.

    Disponível apenas para usuários administradores.
    """
    try:
        # Verificar se usuário é admin
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem acessar dashboard executivo",
            )

        kpis = await AnalyticsService.get_executive_kpis(db)
        return kpis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard executivo: {str(e)}",
        )


@router.get("/dashboard/{dashboard_id}", response_model=DashboardData)
async def get_dashboard_data(
    dashboard_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém dados completos de um dashboard específico.

    Retorna métricas e configurações do dashboard solicitado.
    """
    try:
        dashboard_id_uuid = UUID(dashboard_id)

        dashboard_data = await AnalyticsService.generate_dashboard_data(
            db=db, dashboard_id=dashboard_id_uuid, user_id=current_user.id
        )

        return dashboard_data

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dados do dashboard: {str(e)}",
        )


@router.post("/reports/generate", response_model=ReportData)
async def generate_report(
    report_request: ReportGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Gera relatório personalizado baseado nos parâmetros.

    Permite criação de relatórios sob demanda com filtros específicos.
    """
    try:
        report_data = await AnalyticsService.generate_report(
            db=db, report_request=report_request, user_id=current_user.id
        )

        return report_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}",
        )


@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Faz download do arquivo de relatório gerado.

    Retorna o arquivo físico do relatório em formato solicitado.
    """
    try:
        report_id_uuid = UUID(report_id)

        # Buscar relatório
        report = db.query(Report).filter(Report.id == report_id_uuid).first()

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Relatório não encontrado"
            )

        # Verificar se usuário tem acesso (criador ou admin)
        if report.created_by != current_user.id:
            if not hasattr(current_user, "role") or current_user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para baixar este relatório",
                )

        # Verificar se arquivo existe
        if not report.file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo do relatório não encontrado",
            )

        # Retornar arquivo
        filename = f"report_{report.name}.{report.format.value}"
        return FileResponse(
            path=report.file_path,
            filename=filename,
            media_type="application/octet-stream",
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de relatório inválido"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no download do relatório: {str(e)}",
        )


@router.get("/metrics/realtime", response_model=List[MetricRead])
async def get_realtime_metrics(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém métricas em tempo real do sistema.

    Retorna métricas ativas mais recentes.
    """
    try:
        query = db.query(Metric).filter(Metric.is_active == True)

        # Filtrar por categoria se especificado
        if category:
            query = query.filter(Metric.category == category)

        metrics = query.order_by(desc(Metric.last_calculated_at)).limit(limit).all()

        # Converter para schema de leitura
        result = []
        for metric in metrics:
            metric_dict = {
                "id": metric.id,
                "name": metric.name,
                "description": metric.description,
                "category": metric.category,
                "metric_type": metric.metric_type,
                "unit": metric.unit,
                "is_active": metric.is_active,
                "created_by": metric.created_by,
                "created_at": metric.created_at,
                "updated_at": metric.updated_at,
                "last_calculated_at": metric.last_calculated_at,
                "current_value": metric.current_value,
            }
            result.append(MetricRead(**metric_dict))

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métricas em tempo real: {str(e)}",
        )


@router.post("/metrics/{metric_id}/record")
async def record_metric_value(
    metric_id: str,
    value: float,
    metadata: Optional[Dict] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Registra novo valor para uma métrica específica.

    Permite alimentação manual de métricas do sistema.
    """
    try:
        metric_id_uuid = UUID(metric_id)

        success = await AnalyticsService.record_metric_value(
            db=db, metric_id=metric_id_uuid, value=value, metadata=metadata
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Métrica não encontrada ou inativa",
            )

        return {"detail": "Valor de métrica registrado com sucesso"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de métrica inválidos"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar valor de métrica: {str(e)}",
        )


@router.get("/metrics/{metric_id}/history")
async def get_metric_history(
    metric_id: str,
    filters: Optional[AnalyticsFilters] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém histórico de valores de uma métrica específica.

    Retorna série temporal para análise de tendências.
    """
    try:
        metric_id_uuid = UUID(metric_id)

        values = await AnalyticsService.get_metric_values(
            db=db, metric_id=metric_id_uuid, filters=filters
        )

        return values

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de métrica inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter histórico de métrica: {str(e)}",
        )


@router.get("/alerts", response_model=List[AlertRead])
async def get_active_alerts(
    severity: Optional[str] = Query(None, description="Filtrar por severidade"),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Lista alertas ativos do sistema.

    Disponível apenas para usuários administradores.
    """
    try:
        # Verificar se usuário é admin
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem visualizar alertas",
            )

        # Verificar e disparar novos alertas
        new_alerts = await AnalyticsService.check_alerts(db)

        # Buscar alertas ativos
        query = db.query(Alert).filter(Alert.resolved_at.is_(None))

        if severity:
            query = query.filter(Alert.severity == severity)

        alerts = query.order_by(desc(Alert.created_at)).limit(limit).all()

        # Converter para schema de leitura
        result = []
        for alert in alerts:
            alert_dict = {
                "id": alert.id,
                "alert_rule_id": alert.alert_rule_id,
                "metric_value": alert.metric_value,
                "message": alert.message,
                "severity": alert.severity,
                "created_at": alert.created_at,
                "acknowledged_at": alert.acknowledged_at,
                "acknowledged_by": alert.acknowledged_by,
                "resolved_at": alert.resolved_at,
            }
            result.append(AlertRead(**alert_dict))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter alertas: {str(e)}",
        )


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Reconhece alerta específico.

    Marca alerta como reconhecido pelo usuário.
    """
    try:
        alert_id_uuid = UUID(alert_id)

        # Buscar alerta
        alert = db.query(Alert).filter(Alert.id == alert_id_uuid).first()

        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Alerta não encontrado"
            )

        if not alert.acknowledged_at:
            alert.acknowledged_at = datetime.utcnow()
            alert.acknowledged_by = current_user.id
            db.commit()

        return {"detail": "Alerta reconhecido com sucesso"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de alerta inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao reconhecer alerta: {str(e)}",
        )


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém resumo completo de analytics do sistema.

    Disponível apenas para usuários administradores.
    """
    try:
        summary = await AnalyticsService.get_analytics_summary(
            db=db, user_id=current_user.id
        )

        return summary

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter resumo de analytics: {str(e)}",
        )


@router.post("/process-alerts", status_code=status.HTTP_200_OK)
async def process_alerts(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Dispara processamento manual de verificação de alertas.

    Útil para testes e manutenção do sistema de alertas.
    """
    try:
        # Verificar se usuário é admin
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem processar alertas manualmente",
            )

        # Executar verificação em background
        background_tasks.add_task(AnalyticsService.check_alerts, db)

        return {
            "detail": "Verificação de alertas iniciada em background",
            "status": "processing",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar alertas: {str(e)}",
        )


@router.get("/trends/{metric_id}")
async def get_metric_trends(
    metric_id: str,
    days: int = Query(30, ge=1, le=365, description="Número de dias para análise"),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Obtém análise de tendências para uma métrica específica.

    Retorna dados históricos e análise de padrões.
    """
    try:
        metric_id_uuid = UUID(metric_id)

        # Buscar valores históricos da métrica
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        values = (
            db.query(MetricValue)
            .filter(
                MetricValue.metric_id == metric_id_uuid,
                MetricValue.timestamp >= cutoff_date,
            )
            .order_by(MetricValue.timestamp)
            .all()
        )

        if not values:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dados insuficientes para análise de tendências",
            )

        # Calcular tendência básica
        values_list = [v.value for v in values]
        first_value = values_list[0]
        last_value = values_list[-1]

        if first_value != 0:
            trend_percentage = ((last_value - first_value) / first_value) * 100
        else:
            trend_percentage = 0

        trend_direction = (
            "up"
            if trend_percentage > 5
            else "down" if trend_percentage < -5 else "stable"
        )

        # Converter para formato de resposta
        data_points = [
            {
                "timestamp": v.timestamp.isoformat(),
                "value": v.value,
                "metadata": v.metadata,
            }
            for v in values
        ]

        return {
            "metric_id": str(metric_id_uuid),
            "metric_name": values[0].metric.name if values else "Métrica",
            "data_points": data_points,
            "trend_direction": trend_direction,
            "trend_percentage": trend_percentage,
            "analysis_period_days": days,
            "data_points_count": len(data_points),
        }

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de métrica inválido"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter tendências: {str(e)}",
        )


@router.get("/export/data")
async def export_analytics_data(
    format: str = Query("json", description="Formato de exportação"),
    time_range: str = Query("last_30_days", description="Período de dados"),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Exporta dados de analytics em formato solicitado.

    Permite download de dados brutos para análise externa.
    """
    try:
        # Verificar se usuário é admin
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem exportar dados",
            )

        # Calcular período
        time_ranges = {
            "last_hour": timedelta(hours=1),
            "last_24_hours": timedelta(days=1),
            "last_7_days": timedelta(days=7),
            "last_30_days": timedelta(days=30),
            "last_90_days": timedelta(days=90),
            "last_year": timedelta(days=365),
        }

        delta = time_ranges.get(time_range, timedelta(days=30))
        start_date = datetime.utcnow() - delta

        # Buscar métricas no período
        values = db.query(MetricValue).filter(MetricValue.timestamp >= start_date).all()

        # Preparar dados para exportação
        export_data = {
            "export_info": {
                "generated_at": datetime.utcnow().isoformat(),
                "time_range": time_range,
                "total_records": len(values),
                "generated_by": current_user.full_name,
            },
            "metrics": [],
        }

        for value in values:
            export_data["metrics"].append(
                {
                    "metric_id": str(value.metric_id),
                    "metric_name": value.metric.name,
                    "value": value.value,
                    "timestamp": value.timestamp.isoformat(),
                    "metadata": value.metadata,
                }
            )

        # Exportar baseado no formato
        if format == "csv":
            # Implementar exportação CSV
            import csv
            import io

            output = io.StringIO()
            fieldnames = ["metric_id", "metric_name", "value", "timestamp", "metadata"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for record in export_data["metrics"]:
                writer.writerow(record)

            return {"data": output.getvalue(), "format": "csv"}

        elif format == "excel":
            # Implementar exportação Excel
            return {
                "data": export_data,
                "format": "json",
                "message": "Excel export not implemented yet",
            }

        else:
            # Retornar JSON por padrão
            return export_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na exportação de dados: {str(e)}",
        )


@router.post("/test-metrics")
async def generate_test_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Gera métricas de teste para validação do sistema.

    Útil para desenvolvimento e testes do módulo Analytics.
    """
    try:
        # Verificar se usuário é admin
        if not hasattr(current_user, "role") or current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem gerar métricas de teste",
            )

        # Gerar métricas de teste básicas
        test_metrics = [
            {"name": "Test Metric 1", "value": 100, "category": "user_activity"},
            {"name": "Test Metric 2", "value": 250, "category": "system_performance"},
            {"name": "Test Metric 3", "value": 75, "category": "business_metrics"},
        ]

        results = []
        for metric_data in test_metrics:
            # Buscar ou criar métrica de teste
            metric = db.query(Metric).filter(Metric.name == metric_data["name"]).first()

            if not metric:
                # Criar métrica de teste
                metric = Metric(
                    name=metric_data["name"],
                    description=f"Métrica de teste: {metric_data['name']}",
                    category=metric_data["category"],
                    metric_type="gauge",
                    unit="count",
                    aggregation_function="sum",
                    is_active=True,
                    created_by=current_user.id,
                )
                db.add(metric)
                db.commit()
                db.refresh(metric)

            # Registrar valor
            success = await AnalyticsService.record_metric_value(
                db=db, metric_id=metric.id, value=metric_data["value"]
            )

            results.append(
                {
                    "metric_name": metric_data["name"],
                    "value": metric_data["value"],
                    "success": success,
                }
            )

        return {
            "detail": "Métricas de teste geradas",
            "results": results,
            "total_generated": len([r for r in results if r["success"]]),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar métricas de teste: {str(e)}",
        )
