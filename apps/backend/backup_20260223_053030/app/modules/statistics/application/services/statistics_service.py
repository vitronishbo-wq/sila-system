from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.modules.statistics.infrastructure.repositories.statistics_repository import StatisticsRepository
from app.modules.statistics.infrastructure.models.statistic_model import StatisticModel
from app.modules.statistics.infrastructure.models.timeseries_model import TimeSeriesModel


class StatisticsService:
    """Service layer for Statistics business logic"""
    
    def __init__(self, session: Session):
        self.repo = StatisticsRepository(session)
        self.session = session

    # ==================== STATISTIC MANAGEMENT ====================
    
    def register_statistic(self, name: str, code: str, description: str = None, 
                          unit: str = None, source_module: str = None) -> Dict[str, Any]:
        """Register a new statistic with validation"""
        # Validate code uniqueness
        if self.repo.statistic_exists(code):
            raise ValueError(f"Statistic with code '{code}' already exists")
        
        # Validate required fields
        if not name or not code:
            raise ValueError("Name and code are required")
        
        stat = self.repo.create_statistic(
            name=name,
            code=code,
            description=description,
            unit=unit,
            source_module=source_module
        )
        
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "unit": stat.unit,
            "source_module": stat.source_module,
            "created_at": stat.created_at.isoformat() if stat.created_at else None
        }

    def get_statistic_details(self, statistic_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a statistic"""
        stat = self.repo.get_statistic(statistic_id)
        if not stat:
            return None
        
        count = self.repo.count_timeseries(statistic_id)
        latest = self.repo.get_latest(statistic_id)
        
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "description": stat.description,
            "unit": stat.unit,
            "source_module": stat.source_module,
            "created_at": stat.created_at.isoformat() if stat.created_at else None,
            "total_records": count,
            "latest_value": {
                "value": latest.value,
                "period_start": latest.period_start.isoformat() if latest.period_start else None
            } if latest else None
        }

    def list_all_statistics(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List all statistics with pagination"""
        stats = self.repo.list_statistics(skip=skip, limit=limit)
        return [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "unit": s.unit,
                "source_module": s.source_module,
                "created_at": s.created_at.isoformat() if s.created_at else None
            }
            for s in stats
        ]

    def list_statistics_by_module(self, module: str) -> List[Dict[str, Any]]:
        """List all statistics for a specific module"""
        stats = self.repo.list_statistics_by_module(module)
        return [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "unit": s.unit,
                "source_module": s.source_module
            }
            for s in stats
        ]

    def update_statistic(self, statistic_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a statistic"""
        stat = self.repo.update_statistic(statistic_id, **kwargs)
        if not stat:
            return None
        
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "unit": stat.unit,
            "source_module": stat.source_module
        }

    def delete_statistic(self, statistic_id: int) -> bool:
        """Delete a statistic and all associated data"""
        return self.repo.delete_statistic(statistic_id)

    # ==================== TIMESERIES OPERATIONS ====================
    
    def record_value(self, statistic_id: int, value: float, period_start: datetime,
                    period_end: Optional[datetime] = None, dimensions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Record a new timeseries value with validation"""
        # Validate statistic exists
        stat = self.repo.get_statistic(statistic_id)
        if not stat:
            raise ValueError(f"Statistic with ID {statistic_id} not found")
        
        # Validate value is numeric
        try:
            float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Value must be numeric, got {type(value).__name__}")
        
        ts = self.repo.record_value(
            statistic_id=statistic_id,
            value=value,
            period_start=period_start,
            period_end=period_end,
            dimensions=dimensions
        )
        
        return {
            "id": ts.id,
            "statistic_id": ts.statistic_id,
            "value": ts.value,
            "period_start": ts.period_start.isoformat() if ts.period_start else None,
            "period_end": ts.period_end.isoformat() if ts.period_end else None,
            "created_at": ts.created_at.isoformat() if ts.created_at else None
        }

    def get_series(self, statistic_id: int, limit: int = 100,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get timeseries values with optional date range filtering"""
        series = self.repo.get_series(
            statistic_id=statistic_id,
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )
        
        return [
            {
                "id": ts.id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None,
                "period_end": ts.period_end.isoformat() if ts.period_end else None,
                "dimensions": ts.dimensions
            }
            for ts in series
        ]

    def get_latest(self, statistic_id: int) -> Optional[Dict[str, Any]]:
        """Get the latest value for a statistic"""
        ts = self.repo.get_latest(statistic_id)
        if not ts:
            return None
        
        return {
            "id": ts.id,
            "value": ts.value,
            "period_start": ts.period_start.isoformat() if ts.period_start else None,
            "period_end": ts.period_end.isoformat() if ts.period_end else None,
            "dimensions": ts.dimensions
        }

    def get_series_by_period(self, statistic_id: int, period_start: datetime,
                            period_end: datetime) -> List[Dict[str, Any]]:
        """Get timeseries values for a specific period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id,
            period_start=period_start,
            period_end=period_end
        )
        
        return [
            {
                "id": ts.id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None,
                "period_end": ts.period_end.isoformat() if ts.period_end else None
            }
            for ts in series
        ]

    def bulk_record_values(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Record multiple values at once"""
        # Validate all records before inserting
        for record in records:
            if 'statistic_id' not in record or 'value' not in record or 'period_start' not in record:
                raise ValueError("Each record must have statistic_id, value, and period_start")
        
        timeseries_list = self.repo.bulk_record_values(records)
        
        return [
            {
                "id": ts.id,
                "statistic_id": ts.statistic_id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None
            }
            for ts in timeseries_list
        ]

    def delete_timeseries(self, timeseries_id: int) -> bool:
        """Delete a timeseries value"""
        return self.repo.delete_timeseries(timeseries_id)

    def delete_series_by_period(self, statistic_id: int, period_start: datetime,
                               period_end: datetime) -> Dict[str, Any]:
        """Delete all timeseries values in a period"""
        count = self.repo.delete_series_by_period(
            statistic_id=statistic_id,
            period_start=period_start,
            period_end=period_end
        )
        
        return {
            "deleted_count": count,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat()
        }

    # ==================== ANALYTICS ====================
    
    def calculate_average(self, statistic_id: int, period_start: datetime,
                         period_end: datetime) -> Optional[float]:
        """Calculate average value for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id,
            period_start=period_start,
            period_end=period_end
        )
        
        if not series:
            return None
        
        return sum(ts.value for ts in series) / len(series)

    def calculate_sum(self, statistic_id: int, period_start: datetime,
                     period_end: datetime) -> float:
        """Calculate sum for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id,
            period_start=period_start,
            period_end=period_end
        )
        
        return sum(ts.value for ts in series) if series else 0.0

    def calculate_min_max(self, statistic_id: int, period_start: datetime,
                         period_end: datetime) -> Optional[Dict[str, float]]:
        """Get min and max values for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id,
            period_start=period_start,
            period_end=period_end
        )
        
        if not series:
            return None
        
        values = [ts.value for ts in series]
        return {
            "min": min(values),
            "max": max(values)
        }

    def get_statistics_summary(self) -> Dict[str, Any]:
        """Get summary statistics about all data"""
        total_stats = self.repo.count_statistics()
        
        return {
            "total_statistics": total_stats,
            "timestamp": datetime.now().isoformat()
        }

