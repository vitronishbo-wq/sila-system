from __future__ import annotations
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.intelligence.bi.api.deps import get_dashboard_service, get_kpi_service, require_permission
from apps.backend.app.modules.intelligence.bi.api.schemas.dashboard_schema import DashboardDomainDataResponse, DashboardExecutiveResponse
from apps.backend.app.modules.intelligence.bi.api.schemas.kpi_schema import KPIConsolidatedResponse, KPIDomainResponse
from apps.backend.app.modules.intelligence.bi.application.services.dashboard_service import DashboardService
from apps.backend.app.modules.intelligence.bi.application.services.kpi_service import KPIService
router = APIRouter(prefix='/bi', tags=['bi'])

def _parse_domains(domains: str | None) -> list[str] | None:
    if not domains:
        return None
    parsed = [item.strip() for item in domains.split(',') if item.strip()]
    return parsed or None

def _ensure_domain_source(is_available: bool, domain: str) -> None:
    if not is_available:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Fonte de dados indisponivel para o dominio '{domain}'. Verifique integracao/adapters do modulo no BI.")

async def _domain_dashboard(domain: str, service: DashboardService, data_ref: date | None) -> dict:
    _ensure_domain_source(service.has_domain_source(domain), domain)
    try:
        return await service.get_dashboard_domain(domain=domain, data_ref=data_ref)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Falha ao montar dashboard do dominio '{domain}': {exc}")

async def _domain_kpis(domain: str, service: KPIService, data_ref: date | None) -> dict:
    _ensure_domain_source(service.has_domain_source(domain), domain)
    try:
        return await service.get_domain_kpis(domain=domain, data_ref=data_ref)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Falha ao coletar KPIs do dominio '{domain}': {exc}")

@router.get('/domains', dependencies=[Depends(require_permission('bi:view'))])
async def get_available_domains(dashboard_service: DashboardService=Depends(get_dashboard_service)):
    return {'domains': dashboard_service.available_domains()}

@router.get('/kpis', response_model=KPIConsolidatedResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_consolidated_kpis(data_ref: date | None=Query(None), domains: str | None=Query(None, description='Lista de dominios separados por virgula (ex: educacao,saude,financas).'), service: KPIService=Depends(get_kpi_service)):
    return await service.get_consolidated_kpis(data_ref=data_ref, domains=_parse_domains(domains))

@router.get('/kpis/domain/{domain}', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_by_domain(domain: str, data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain=domain, service=service, data_ref=data_ref)

@router.get('/kpis/educacao', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_educacao(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='educacao', service=service, data_ref=data_ref)

@router.get('/kpis/juventude', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_juventude(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='juventude', service=service, data_ref=data_ref)

@router.get('/kpis/emprego', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_emprego(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='emprego', service=service, data_ref=data_ref)

@router.get('/kpis/saude', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_saude(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='saude', service=service, data_ref=data_ref)

@router.get('/kpis/assistencia', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_assistencia(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='assistencia', service=service, data_ref=data_ref)

@router.get('/kpis/identidade', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_identidade(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='identidade', service=service, data_ref=data_ref)

@router.get('/kpis/workflow', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_workflow(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='workflow', service=service, data_ref=data_ref)

@router.get('/kpis/service-requests', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_service_requests(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='service_requests', service=service, data_ref=data_ref)

@router.get('/kpis/financas', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_financas(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='financas', service=service, data_ref=data_ref)

@router.get('/kpis/financas-publicas', response_model=KPIDomainResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_kpis_financas_publicas(data_ref: date | None=Query(None), service: KPIService=Depends(get_kpi_service)):
    return await _domain_kpis(domain='financas_publicas', service=service, data_ref=data_ref)

@router.get('/dashboards/executivo', response_model=DashboardExecutiveResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_executivo(data_ref: date | None=Query(None), domains: str | None=Query(None, description='Lista de dominios separados por virgula para filtrar o painel executivo.'), service: DashboardService=Depends(get_dashboard_service)):
    return await service.get_dashboard_executivo(data_ref=data_ref, domains=_parse_domains(domains))

@router.get('/dashboards/domain/{domain}', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_by_domain(domain: str, data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain=domain, service=service, data_ref=data_ref)

@router.get('/dashboards/educacao', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_educacao(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='educacao', service=service, data_ref=data_ref)

@router.get('/dashboards/juventude', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_juventude(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='juventude', service=service, data_ref=data_ref)

@router.get('/dashboards/emprego', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_emprego(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='emprego', service=service, data_ref=data_ref)

@router.get('/dashboards/saude', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_saude(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='saude', service=service, data_ref=data_ref)

@router.get('/dashboards/assistencia', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_assistencia(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='assistencia', service=service, data_ref=data_ref)

@router.get('/dashboards/identidade', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_identidade(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='identidade', service=service, data_ref=data_ref)

@router.get('/dashboards/workflow', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_workflow(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='workflow', service=service, data_ref=data_ref)

@router.get('/dashboards/service-requests', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_service_requests(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='service_requests', service=service, data_ref=data_ref)

@router.get('/dashboards/financas', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_financas(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='financas', service=service, data_ref=data_ref)

@router.get('/dashboards/financas-publicas', response_model=DashboardDomainDataResponse, dependencies=[Depends(require_permission('bi:view'))])
async def get_dashboard_financas_publicas(data_ref: date | None=Query(None), service: DashboardService=Depends(get_dashboard_service)):
    return await _domain_dashboard(domain='financas_publicas', service=service, data_ref=data_ref)