from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from .deps import require_permission, get_statistics_service
from .schemas.statistics_schema import StatisticCreateSchema, StatisticSchema, StatisticDetailSchema
from .schemas.timeseries_schema import TimeSeriesPointSchema, TimeSeriesSchema
from ..application.services.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["statistics"])

# middleware será adicionado na app principal


# ==================== STATISTIC ENDPOINTS ====================

@router.post("/", response_model=StatisticSchema, dependencies=[Depends(require_permission("statistics:admin"))])
async def create_statistic(
    payload: StatisticCreateSchema,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Create a new statistic"""
    try:
        result = service.register_statistic(
            name=payload.name,
            code=payload.code,
            description=payload.description,
            unit=payload.unit,
            source_module=payload.source_module
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StatisticSchema], dependencies=[Depends(require_permission("statistics:view"))])
async def list_statistics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: StatisticsService = Depends(get_statistics_service)
):
    """List all statistics with pagination"""
    return service.list_all_statistics(skip=skip, limit=limit)


@router.get("/code/{code}", response_model=StatisticDetailSchema, dependencies=[Depends(require_permission("statistics:view"))])
async def get_statistic_by_code(
    code: str,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get statistic details by code"""
    stat = service.repo.get_statistic_by_code(code)
    if not stat:
        raise HTTPException(status_code=404, detail=f"Statistic with code '{code}' not found")
    
    return service.get_statistic_details(stat.id)


@router.get("/{statistic_id}", response_model=StatisticDetailSchema, dependencies=[Depends(require_permission("statistics:view"))])
async def get_statistic(
    statistic_id: int,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get statistic details by ID"""
    result = service.get_statistic_details(statistic_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Statistic with ID {statistic_id} not found")
    return result


@router.put("/{statistic_id}", response_model=StatisticSchema, dependencies=[Depends(require_permission("statistics:admin"))])
async def update_statistic(
    statistic_id: int,
    payload: StatisticCreateSchema,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Update a statistic"""
    result = service.update_statistic(
        statistic_id,
        name=payload.name,
        code=payload.code,
        description=payload.description,
        unit=payload.unit,
        source_module=payload.source_module
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Statistic with ID {statistic_id} not found")
    return result


@router.delete("/{statistic_id}", dependencies=[Depends(require_permission("statistics:admin"))])
async def delete_statistic(
    statistic_id: int,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Delete a statistic and all associated data"""
    if not service.delete_statistic(statistic_id):
        raise HTTPException(status_code=404, detail=f"Statistic with ID {statistic_id} not found")
    return {"message": "Statistic deleted successfully", "statistic_id": statistic_id}


# ==================== TIMESERIES ENDPOINTS ====================

@router.post("/{statistic_id}/record", response_model=TimeSeriesSchema, dependencies=[Depends(require_permission("statistics:admin"))])
async def record_value(
    statistic_id: int,
    payload: TimeSeriesPointSchema,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Record a new timeseries value"""
    try:
        result = service.record_value(
            statistic_id=statistic_id,
            value=payload.value,
            period_start=payload.period_start,
            period_end=payload.period_end,
            dimensions=payload.dimensions
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{statistic_id}/series", response_model=list[TimeSeriesSchema], dependencies=[Depends(require_permission("statistics:view"))])
async def get_series(
    statistic_id: int,
    limit: int = Query(100, ge=1, le=1000),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get timeseries values for a statistic"""
    return service.get_series(
        statistic_id=statistic_id,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/{statistic_id}/latest", response_model=TimeSeriesSchema | None, dependencies=[Depends(require_permission("statistics:view"))])
async def get_latest(
    statistic_id: int,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get the latest timeseries value for a statistic"""
    return service.get_latest(statistic_id)


@router.get("/{statistic_id}/period", response_model=list[TimeSeriesSchema], dependencies=[Depends(require_permission("statistics:view"))])
async def get_series_by_period(
    statistic_id: int,
    period_start: datetime = Query(...),
    period_end: datetime = Query(...),
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get timeseries values for a specific period"""
    return service.get_series_by_period(
        statistic_id=statistic_id,
        period_start=period_start,
        period_end=period_end
    )


@router.post("/{statistic_id}/bulk-record", response_model=list[TimeSeriesSchema], dependencies=[Depends(require_permission("statistics:admin"))])
async def bulk_record_values(
    statistic_id: int,
    records: list[TimeSeriesPointSchema],
    service: StatisticsService = Depends(get_statistics_service)
):
    """Record multiple timeseries values at once"""
    try:
        data = [
            {
                "statistic_id": statistic_id,
                "value": r.value,
                "period_start": r.period_start,
                "period_end": r.period_end,
                "dimensions": r.dimensions
            }
            for r in records
        ]
        return service.bulk_record_values(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{statistic_id}/series/{timeseries_id}", dependencies=[Depends(require_permission("statistics:admin"))])
async def delete_timeseries(
    statistic_id: int,
    timeseries_id: int,
    service: StatisticsService = Depends(get_statistics_service)
):
    """Delete a timeseries value"""
    if not service.delete_timeseries(timeseries_id):
        raise HTTPException(status_code=404, detail=f"Timeseries with ID {timeseries_id} not found")
    return {"message": "Timeseries value deleted successfully", "timeseries_id": timeseries_id}


# ==================== ANALYTICS ENDPOINTS ====================

@router.get("/{statistic_id}/analytics/average", dependencies=[Depends(require_permission("statistics:view"))])
async def get_average(
    statistic_id: int,
    period_start: datetime = Query(...),
    period_end: datetime = Query(...),
    service: StatisticsService = Depends(get_statistics_service)
):
    """Calculate average value for a period"""
    result = service.calculate_average(
        statistic_id=statistic_id,
        period_start=period_start,
        period_end=period_end
    )
    if result is None:
        raise HTTPException(status_code=404, detail="No data found for the specified period")
    return {"average": result, "period_start": period_start, "period_end": period_end}


@router.get("/{statistic_id}/analytics/sum", dependencies=[Depends(require_permission("statistics:view"))])
async def get_sum(
    statistic_id: int,
    period_start: datetime = Query(...),
    period_end: datetime = Query(...),
    service: StatisticsService = Depends(get_statistics_service)
):
    """Calculate sum for a period"""
    result = service.calculate_sum(
        statistic_id=statistic_id,
        period_start=period_start,
        period_end=period_end
    )
    return {"sum": result, "period_start": period_start, "period_end": period_end}


@router.get("/{statistic_id}/analytics/minmax", dependencies=[Depends(require_permission("statistics:view"))])
async def get_minmax(
    statistic_id: int,
    period_start: datetime = Query(...),
    period_end: datetime = Query(...),
    service: StatisticsService = Depends(get_statistics_service)
):
    """Get min and max values for a period"""
    result = service.calculate_min_max(
        statistic_id=statistic_id,
        period_start=period_start,
        period_end=period_end
    )
    if not result:
        raise HTTPException(status_code=404, detail="No data found for the specified period")
    return {**result, "period_start": period_start, "period_end": period_end}


@router.get("/analytics/summary", dependencies=[Depends(require_permission("statistics:view"))])
async def get_summary(service: StatisticsService = Depends(get_statistics_service)):
    """Get summary statistics about all data"""
    return service.get_statistics_summary()

