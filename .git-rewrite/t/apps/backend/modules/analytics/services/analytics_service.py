"""
Serviço principal para gestão de Analytics.

Este módulo implementa a lógica de negócio completa para:
- Coleta e processamento de métricas em tempo real
- Geração de dashboards executivos e operacionais
- Criação e execução de relatórios personalizados
- Sistema de alertas baseados em thresholds
- Cache inteligente para performance otimizada
- Análise de tendências e forecasting básico
- Integração com módulos existentes (Documents, Notifications)
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from modules.citizenship.models.citizen import Citizen

from ..models.analytics_models import (
    Alert,
    AlertRule,
    Dashboard,
    DashboardAccessLog,
    DashboardMetric,
    Metric,
    MetricValue,
)
from ..schemas.analytics_schemas import (
    AlertRead,
    AnalyticsFilters,
    AnalyticsSummary,
    DashboardData,
    ExecutiveKPIs,
    MetricTrendData,
    MetricValueRead,
    ModuleUsageStats,
    ReportData,
    ReportGenerationRequest,
    SystemPerformanceMetrics,
)

logger = logging.getLogger(__name__)

# Configurações de serviço
CACHE_TTL_SECONDS = 300  # 5 minutos
MAX_CACHE_SIZE = 1000
BATCH_SIZE_METRICS = 100


class AnalyticsService:
    """Classe principal para operações de analytics."""

    @staticmethod
    async def record_metric_value(
        db: AsyncSession,
        metric_id: UUID,
        value: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Registra novo valor para uma métrica.

        Args:
            db: Sessão do banco de dados
            metric_id: ID da métrica
            value: Valor a ser registrado
            metadata: Metadados opcionais

        Returns:
            True se registrado com sucesso
        """
        try:
            # Verificar se métrica existe e está ativa
            metric = (
                db.query(Metric)
                .filter(Metric.id == metric_id, Metric.is_active == True)
                .first()
            )

            if not metric:
                logger.warning(f"Métrica não encontrada ou inativa: {metric_id}")
                return False

            # Criar registro de valor
            metric_value = MetricValue(
                metric_id=metric_id, value=value, metadata=metadata or {}
            )

            db.add(metric_value)

            # Atualizar valor atual da métrica
            metric.current_value = value
            metric.last_calculated_at = datetime.utcnow()

            db.commit()

            logger.debug(f"Valor registrado para métrica {metric.name}: {value}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao registrar valor de métrica: {e}")
            raise

    @staticmethod
    async def get_metric_values(
        db: AsyncSession, metric_id: UUID, filters: Optional[AnalyticsFilters] = None
    ) -> List[MetricValueRead]:
        """
        Busca valores históricos de uma métrica.

        Args:
            db: Sessão do banco de dados
            metric_id: ID da métrica
            filters: Filtros opcionais

        Returns:
            Lista de valores da métrica
        """
        try:
            query = db.query(MetricValue).filter(MetricValue.metric_id == metric_id)

            # Aplicar filtros de tempo
            if filters:
                if filters.start_date:
                    query = query.filter(MetricValue.timestamp >= filters.start_date)
                if filters.end_date:
                    query = query.filter(MetricValue.timestamp <= filters.end_date)

                # Aplicar agrupamento se especificado
                if filters.group_by:
                    # Implementar agrupamento por período
                    pass

            values = query.order_by(MetricValue.timestamp).all()

            # Converter para schema de leitura
            result = []
            for value in values:
                value_dict = {
                    "id": value.id,
                    "metric_id": value.metric_id,
                    "value": value.value,
                    "timestamp": value.timestamp,
                    "metadata": value.metadata or {},
                    "created_at": value.created_at,
                }
                result.append(MetricValueRead(**value_dict))

            return result

        except Exception as e:
            logger.error(f"Erro ao buscar valores de métrica: {e}")
            raise

    @staticmethod
    async def get_executive_kpis(db: AsyncSession) -> ExecutiveKPIs:
        """
        Obtém KPIs executivos principais do sistema.

        Args:
            db: Sessão do banco de dados

        Returns:
            KPIs executivos atualizados
        """
        try:
            # Dados de usuários
            total_users = (
                db.query(func.count(Citizen.id))
                .filter(Citizen.status == "active")
                .scalar()
            )

            active_users_today = (
                db.query(func.count(Citizen.id))
                .filter(Citizen.last_login >= datetime.utcnow() - timedelta(days=1))
                .scalar()
            )

            # Dados de documentos
            total_documents = (
                db.query(func.count(Document.id))
                .filter(Document.status == "active")
                .scalar()
            )

            documents_uploaded_today = (
                db.query(func.count(Document.id))
                .filter(Document.created_at >= datetime.utcnow() - timedelta(days=1))
                .scalar()
            )

            # Dados de notificações
            total_notifications = (
                db.query(func.count(Notification.id))
                .filter(Notification.status.in_(["sent", "delivered"]))
                .scalar()
            )

            notifications_sent_today = (
                db.query(func.count(Notification.id))
                .filter(Notification.sent_at >= datetime.utcnow() - timedelta(days=1))
                .scalar()
            )

            # Performance do sistema (valores mock - implementar coleta real)
            system_uptime = 99.9  # Implementar cálculo real
            avg_response_time = 150.0  # ms - implementar medição real

            # Alertas críticos
            critical_alerts = (
                db.query(func.count(Alert.id))
                .filter(Alert.severity == "critical", Alert.resolved_at.is_(None))
                .scalar()
            )

            return ExecutiveKPIs(
                total_users=total_users,
                active_users_today=active_users_today,
                total_documents=total_documents,
                documents_uploaded_today=documents_uploaded_today,
                total_notifications=total_notifications,
                notifications_sent_today=notifications_sent_today,
                system_uptime_percentage=system_uptime,
                average_response_time_ms=avg_response_time,
                critical_alerts_count=critical_alerts,
            )

        except Exception as e:
            logger.error(f"Erro ao obter KPIs executivos: {e}")
            raise

    @staticmethod
    async def generate_dashboard_data(
        db: AsyncSession, dashboard_id: UUID, user_id: UUID
    ) -> DashboardData:
        """
        Gera dados completos para um dashboard específico.

        Args:
            db: Sessão do banco de dados
            dashboard_id: ID do dashboard
            user_id: ID do usuário solicitante

        Returns:
            Dados do dashboard formatados
        """
        try:
            # Buscar dashboard
            dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()

            if not dashboard:
                raise ValueError("Dashboard não encontrado")

            # Verificar permissões (público ou criador)
            if not dashboard.is_public and dashboard.created_by != user_id:
                raise ValueError("Sem permissão para acessar este dashboard")

            # Buscar métricas do dashboard
            dashboard_metrics = (
                db.query(DashboardMetric)
                .filter(DashboardMetric.dashboard_id == dashboard_id)
                .order_by(DashboardMetric.display_order)
                .all()
            )

            metrics_data = []
            for dm in dashboard_metrics:
                # Buscar valores recentes da métrica
                recent_values = (
                    db.query(MetricValue)
                    .filter(MetricValue.metric_id == dm.metric_id)
                    .order_by(desc(MetricValue.timestamp))
                    .limit(10)
                    .all()
                )

                metric_data = {
                    "metric_id": str(dm.metric_id),
                    "metric_name": dm.metric.name,
                    "current_value": dm.metric.current_value,
                    "unit": dm.metric.unit,
                    "chart_type": dm.chart_type or "line",
                    "values": [
                        {"timestamp": v.timestamp.isoformat(), "value": v.value}
                        for v in recent_values
                    ],
                }
                metrics_data.append(metric_data)

            # Registrar acesso
            access_log = DashboardAccessLog(dashboard_id=dashboard_id, user_id=user_id)
            db.add(access_log)

            # Atualizar último acesso
            dashboard.last_accessed_at = datetime.utcnow()

            db.commit()

            # Gerar dados de resumo
            summary_stats = {
                "total_metrics": len(metrics_data),
                "last_updated": datetime.utcnow(),
                "time_range": "last_24_hours",
            }

            return DashboardData(
                dashboard_id=dashboard_id,
                dashboard_name=dashboard.name,
                last_updated=datetime.utcnow(),
                metrics=metrics_data,
                summary_stats=summary_stats,
            )

        except Exception as e:
            logger.error(f"Erro ao gerar dados do dashboard: {e}")
            raise

    @staticmethod
    async def generate_report(
        db: AsyncSession, report_request: ReportGenerationRequest, user_id: UUID
    ) -> ReportData:
        """
        Gera relatório personalizado baseado nos parâmetros.

        Args:
            db: Sessão do banco de dados
            report_request: Parâmetros de geração
            user_id: ID do usuário solicitante

        Returns:
            Dados do relatório gerado
        """
        try:
            start_time = time.time()

            # Calcular período de análise
            time_range = await AnalyticsService._calculate_time_range(report_request)

            # Coletar dados baseado no tipo de relatório
            if report_request.report_id:
                # Relatório específico
                report_data = await AnalyticsService._generate_specific_report(
                    db, report_request, time_range
                )
            else:
                # Relatório geral
                report_data = await AnalyticsService._generate_general_report(
                    db, report_request, time_range
                )

            # Gerar gráficos se solicitado
            charts = []
            if report_request.include_charts:
                charts = await AnalyticsService._generate_charts(
                    report_data, report_request
                )

            # Exportar arquivo se necessário
            file_url = None
            if report_request.format != "json":
                file_url = await AnalyticsService._export_report_file(
                    report_data, report_request, user_id
                )

            # Calcular tempo de execução
            execution_time = time.time() - start_time

            return ReportData(
                report_id=report_request.report_id or uuid4(),
                report_name="Relatório Personalizado",
                generated_at=datetime.utcnow(),
                time_range=time_range,
                summary=report_data.get("summary", {}),
                metrics=report_data.get("metrics", []),
                charts=charts,
                raw_data=(
                    report_data.get("raw_data")
                    if report_request.include_raw_data
                    else None
                ),
                file_url=file_url,
            )

        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            raise

    @staticmethod
    async def check_alerts(db: AsyncSession) -> List[AlertRead]:
        """
        Verifica e dispara alertas baseados em regras ativas.

        Args:
            db: Sessão do banco de dados

        Returns:
            Lista de alertas disparados
        """
        try:
            triggered_alerts = []

            # Buscar regras de alerta ativas
            alert_rules = db.query(AlertRule).filter(AlertRule.is_active == True).all()

            for rule in alert_rules:
                try:
                    # Buscar valor atual da métrica
                    current_value = rule.metric.current_value

                    if current_value is None:
                        continue

                    # Verificar condição
                    should_trigger = False

                    if (
                        rule.condition == "greater_than"
                        and current_value > rule.threshold_value
                    ):
                        should_trigger = True
                    elif (
                        rule.condition == "less_than"
                        and current_value < rule.threshold_value
                    ):
                        should_trigger = True
                    elif (
                        rule.condition == "equals"
                        and current_value == rule.threshold_value
                    ):
                        should_trigger = True
                    elif (
                        rule.condition == "not_equals"
                        and current_value != rule.threshold_value
                    ):
                        should_trigger = True

                    if should_trigger:
                        # Verificar cooldown
                        if rule.last_triggered_at:
                            cooldown_end = rule.last_triggered_at + timedelta(
                                minutes=rule.cooldown_minutes
                            )
                            if datetime.utcnow() < cooldown_end:
                                continue

                        # Criar alerta
                        alert = Alert(
                            alert_rule_id=rule.id,
                            metric_value=current_value,
                            message=f"Métrica '{rule.metric.name}' atingiu threshold: {current_value}",
                            severity=rule.severity,
                            metadata={
                                "rule_name": rule.name,
                                "threshold": rule.threshold_value,
                            },
                        )

                        db.add(alert)
                        triggered_alerts.append(alert)

                        # Atualizar regra
                        rule.last_triggered_at = datetime.utcnow()
                        rule.trigger_count += 1

                except Exception as e:
                    logger.error(f"Erro ao processar regra de alerta {rule.id}: {e}")

            if triggered_alerts:
                db.commit()
                logger.info(f"{len(triggered_alerts)} alertas disparados")

            # Converter para schema de leitura
            result = []
            for alert in triggered_alerts:
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

        except Exception as e:
            logger.error(f"Erro na verificação de alertas: {e}")
            raise

    @staticmethod
    async def get_analytics_summary(
        db: AsyncSession, user_id: UUID
    ) -> AnalyticsSummary:
        """
        Obtém resumo completo de analytics para usuário admin.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário (deve ser admin)

        Returns:
            Resumo completo de analytics
        """
        try:
            # Verificar se usuário é admin
            user = db.query(Citizen).filter(Citizen.id == user_id).first()
            if not user or not hasattr(user, "role") or user.role != "admin":
                raise ValueError("Apenas administradores podem acessar resumo completo")

            # Obter KPIs executivos
            executive_kpis = await AnalyticsService.get_executive_kpis(db)

            # Obter estatísticas de uso por módulo
            module_stats = await AnalyticsService._get_module_usage_stats(db)

            # Obter métricas de performance do sistema
            system_metrics = await AnalyticsService._get_system_performance_metrics(db)

            # Obter tendências principais
            top_trends = await AnalyticsService._get_top_trends(db)

            # Obter alertas ativos
            active_alerts = await AnalyticsService.check_alerts(db)

            return AnalyticsSummary(
                executive_kpis=executive_kpis,
                module_usage=module_stats,
                system_performance=system_metrics,
                top_trends=top_trends,
                active_alerts=active_alerts,
                generated_at=datetime.utcnow(),
            )

        except Exception as e:
            logger.error(f"Erro ao obter resumo de analytics: {e}")
            raise

    # Métodos auxiliares privados

    @staticmethod
    async def _calculate_time_range(request: ReportGenerationRequest) -> Dict[str, Any]:
        """Calcula período de análise baseado na solicitação."""
        now = datetime.utcnow()

        if request.custom_start_date and request.custom_end_date:
            return {
                "start": request.custom_start_date,
                "end": request.custom_end_date,
                "range_type": "custom",
            }

        # Calcular baseado no time_range
        time_ranges = {
            "last_hour": timedelta(hours=1),
            "last_24_hours": timedelta(days=1),
            "last_7_days": timedelta(days=7),
            "last_30_days": timedelta(days=30),
            "last_90_days": timedelta(days=90),
            "last_year": timedelta(days=365),
        }

        delta = time_ranges.get(request.time_range.value, timedelta(days=30))
        start_date = now - delta

        return {"start": start_date, "end": now, "range_type": request.time_range.value}

    @staticmethod
    async def _generate_specific_report(
        db: AsyncSession, request: ReportGenerationRequest, time_range: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera relatório específico baseado no tipo."""
        # Implementar geração baseada no report_type
        # Por ora, retornar estrutura básica
        return {
            "summary": {"total_records": 0, "period": time_range["range_type"]},
            "metrics": [],
            "raw_data": [],
        }

    @staticmethod
    async def _generate_general_report(
        db: AsyncSession, request: ReportGenerationRequest, time_range: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera relatório geral com métricas do sistema."""
        try:
            # Buscar métricas ativas
            metrics = db.query(Metric).filter(Metric.is_active == True).all()

            metrics_data = []
            for metric in metrics:
                # Buscar valores no período
                values = (
                    db.query(MetricValue)
                    .filter(
                        MetricValue.metric_id == metric.id,
                        MetricValue.timestamp >= time_range["start"],
                        MetricValue.timestamp <= time_range["end"],
                    )
                    .all()
                )

                if values:
                    values_list = [v.value for v in values]
                    metrics_data.append(
                        {
                            "metric_id": str(metric.id),
                            "name": metric.name,
                            "current_value": metric.current_value,
                            "average": sum(values_list) / len(values_list),
                            "min": min(values_list),
                            "max": max(values_list),
                            "count": len(values_list),
                        }
                    )

            return {
                "summary": {
                    "total_metrics": len(metrics_data),
                    "period": time_range["range_type"],
                    "data_points": sum(m["count"] for m in metrics_data),
                },
                "metrics": metrics_data,
                "raw_data": [],  # Implementar se necessário
            }

        except Exception as e:
            logger.error(f"Erro ao gerar relatório geral: {e}")
            return {"summary": {}, "metrics": [], "raw_data": []}

    @staticmethod
    async def _generate_charts(
        report_data: Dict[str, Any], request: ReportGenerationRequest
    ) -> List[Dict[str, Any]]:
        """Gera gráficos para o relatório."""
        # Implementar geração de gráficos
        # Por ora, retornar estrutura vazia
        return []

    @staticmethod
    async def _export_report_file(
        report_data: ReportData, request: ReportGenerationRequest, user_id: UUID
    ) -> str:
        """Exporta relatório para arquivo."""
        try:
            # Implementar exportação baseada no formato
            if request.format == "pdf":
                return await AnalyticsService._export_pdf(report_data, user_id)
            elif request.format == "excel":
                return await AnalyticsService._export_excel(report_data, user_id)
            elif request.format == "csv":
                return await AnalyticsService._export_csv(report_data, user_id)
            else:
                return None

        except Exception as e:
            logger.error(f"Erro na exportação do relatório: {e}")
            return None

    @staticmethod
    async def _export_pdf(report_data: ReportData, user_id: UUID) -> str:
        """Exporta relatório para PDF."""
        try:
            filename = f"report_{report_data.report_id}_{int(time.time())}.pdf"
            filepath = f"/tmp/{filename}"

            # Criar PDF básico
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()

            story = []

            # Título
            story.append(
                Paragraph(f"Relatório: {report_data.report_name}", styles["Title"])
            )
            story.append(Spacer(1, 12))

            # Resumo
            summary_text = f"""
            Período: {report_data.time_range['range_type']}
            Gerado em: {report_data.generated_at.strftime('%Y-%m-%d %H:%M:%S')}
            Total de métricas: {len(report_data.metrics)}
            """
            story.append(Paragraph(summary_text, styles["Normal"]))
            story.append(Spacer(1, 12))

            # Métricas
            if report_data.metrics:
                data = [["Métrica", "Valor Atual", "Média", "Mín", "Máx"]]
                for metric in report_data.metrics:
                    data.append(
                        [
                            metric.get("name", "N/A"),
                            str(metric.get("current_value", 0)),
                            str(metric.get("average", 0)),
                            str(metric.get("min", 0)),
                            str(metric.get("max", 0)),
                        ]
                    )

                table = Table(data)
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 14),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )

                story.append(table)

            doc.build(story)

            return filepath

        except Exception as e:
            logger.error(f"Erro na exportação PDF: {e}")
            return None

    @staticmethod
    async def _export_excel(report_data: ReportData, user_id: UUID) -> str:
        """Exporta relatório para Excel."""
        try:
            filename = f"report_{report_data.report_id}_{int(time.time())}.xlsx"
            filepath = f"/tmp/{filename}"

            # Criar DataFrame com dados
            if report_data.metrics:
                df = pd.DataFrame(report_data.metrics)
                df.to_excel(filepath, index=False)

            return filepath

        except Exception as e:
            logger.error(f"Erro na exportação Excel: {e}")
            return None

    @staticmethod
    async def _export_csv(report_data: ReportData, user_id: UUID) -> str:
        """Exporta relatório para CSV."""
        try:
            filename = f"report_{report_data.report_id}_{int(time.time())}.csv"
            filepath = f"/tmp/{filename}"

            # Criar CSV com dados
            if report_data.metrics:
                df = pd.DataFrame(report_data.metrics)
                df.to_csv(filepath, index=False)

            return filepath

        except Exception as e:
            logger.error(f"Erro na exportação CSV: {e}")
            return None

    @staticmethod
    async def _get_module_usage_stats(db: AsyncSession) -> List[ModuleUsageStats]:
        """Obtém estatísticas de uso por módulo."""
        # Implementar coleta de estatísticas por módulo
        # Por ora, retornar dados mock
        return [
            ModuleUsageStats(
                module_name="Documents",
                total_requests=1500,
                unique_users=45,
                average_response_time=0.8,
                error_rate=0.02,
                top_endpoints=[
                    {"endpoint": "/documents/upload", "requests": 450},
                    {"endpoint": "/documents/user", "requests": 380},
                ],
            ),
            ModuleUsageStats(
                module_name="Notifications",
                total_requests=890,
                unique_users=32,
                average_response_time=0.6,
                error_rate=0.01,
                top_endpoints=[
                    {"endpoint": "/notifications/", "requests": 320},
                    {"endpoint": "/notifications/user", "requests": 280},
                ],
            ),
        ]

    @staticmethod
    async def _get_system_performance_metrics(
        db: AsyncSession,
    ) -> SystemPerformanceMetrics:
        """Obtém métricas de performance do sistema."""
        # Implementar coleta de métricas reais do sistema
        # Por ora, retornar dados mock baseados no sistema atual
        return SystemPerformanceMetrics(
            timestamp=datetime.utcnow(),
            cpu_usage_percent=45.2,
            memory_usage_percent=67.8,
            disk_usage_percent=23.1,
            database_connections=12,
            active_sessions=8,
            queue_size=0,
            response_time_p95=245.5,
        )

    @staticmethod
    async def _get_top_trends(db: AsyncSession) -> List[MetricTrendData]:
        """Obtém tendências principais das métricas."""
        # Implementar análise de tendências
        # Por ora, retornar dados mock
        return [
            MetricTrendData(
                metric_id=uuid4(),
                metric_name="Documentos Enviados",
                data_points=[
                    {"date": "2024-01-01", "value": 45},
                    {"date": "2024-01-02", "value": 52},
                    {"date": "2024-01-03", "value": 48},
                ],
                trend_direction="up",
                trend_percentage=15.2,
            )
        ]


# Função utilitária para coleta periódica de métricas
async def collect_system_metrics_periodically(
    db_session_factory, interval_seconds: int = 60
):
    """Coleta métricas do sistema periodicamente."""
    while True:
        try:
            async with db_session_factory() as db:
                # Coletar métricas básicas do sistema
                import psutil

                # Métricas de sistema
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent

                # Registrar métricas (se existirem métricas definidas)
                # Esta é uma implementação básica - pode ser expandida

            await asyncio.sleep(interval_seconds)

        except Exception as e:
            logger.error(f"Erro na coleta periódica de métricas: {e}")
            await asyncio.sleep(
                interval_seconds * 2
            )  # Aguardar mais tempo em caso de erro
