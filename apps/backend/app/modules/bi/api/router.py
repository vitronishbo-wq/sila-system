from fastapi import APIRouter, Depends

from .deps import require_permission
from .schemas.dashboard_schema import DashboardCreateSchema, DashboardSchema
from .schemas.kpi_schema import KPIResponse
from .schemas.report_schema import RunReportSchema, ReportSchema

router = APIRouter(prefix="/bi", tags=["bi"])

# middleware será adicionado na app principal


@router.get("/kpis", response_model=list[KPIResponse], dependencies=[Depends(require_permission("bi:view"))])
def list_kpis():
    return []


@router.get("/kpis/{code}", response_model=KPIResponse, dependencies=[Depends(require_permission("bi:view"))])
def get_kpi(code: str):
    return {"code": code, "value": 0.0}


@router.get("/dashboards", response_model=list[DashboardSchema], dependencies=[Depends(require_permission("bi:view"))])
def list_dashboards():
    return []


@router.post("/dashboards", response_model=DashboardSchema, dependencies=[Depends(require_permission("bi:admin"))])
def create_dashboard(payload: DashboardCreateSchema):
    return {"id": 1, **payload.dict(), "created_at": None}


@router.get("/dashboards/{id}", response_model=DashboardSchema, dependencies=[Depends(require_permission("bi:view"))])
def get_dashboard(id: int):
    return {"id": id, "name": "Demo", "description": "", "owner_id": None, "layout": {}, "created_at": None}


@router.put("/dashboards/{id}", response_model=DashboardSchema, dependencies=[Depends(require_permission("bi:admin"))])
def update_dashboard(id: int, payload: DashboardCreateSchema):
    return {"id": id, **payload.dict(), "created_at": None}


@router.post("/reports/run", dependencies=[Depends(require_permission("bi:view"))])
def run_report(payload: RunReportSchema):
    return {"status": "running", "report_id": payload.report_id}


@router.get("/reports/{id}", response_model=ReportSchema, dependencies=[Depends(require_permission("bi:view"))])
def get_report(id: int):
    return {"id": id, "name": "Demo", "query": "", "parameters": {}, "created_by": None, "created_at": None}
