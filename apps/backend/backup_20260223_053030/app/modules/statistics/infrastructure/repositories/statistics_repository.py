from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import and_, select, delete as sa_delete, func
from sqlalchemy.orm import Session
from ..models.timeseries_model import TimeSeriesModel
from ..models.statistic_model import StatisticModel
from ..models.aggregation_model import AggregationModel


class StatisticsRepository:
    """Repository for Statistics CRUD operations (Sync version for AsyncSession)"""
    
    def __init__(self, session: Session):
        self.session = session

    # ==================== STATISTIC CRUD ====================
    
    def create_statistic(self, name: str, code: str, description: str = None, 
                        unit: str = None, source_module: str = None) -> StatisticModel:
        """Create a new statistic"""
        stat = StatisticModel(
            name=name, 
            code=code, 
            description=description, 
            unit=unit, 
            source_module=source_module
        )
        self.session.add(stat)
        self.session.flush()
        return stat

    def get_statistic(self, statistic_id: int) -> Optional[StatisticModel]:
        """Get statistic by ID"""
        # For AsyncSession, use the sync methods via .sync_session if available
        if hasattr(self.session, 'sync_session'):
            result = self.session.sync_session.query(StatisticModel).filter(
                StatisticModel.id == statistic_id
            ).first()
        else:
            # Fallback for testing
            result = None
        return result

    def get_statistic_by_code(self, code: str) -> Optional[StatisticModel]:
        """Get statistic by code"""
        if hasattr(self.session, 'sync_session'):
            result = self.session.sync_session.query(StatisticModel).filter(
                StatisticModel.code == code
            ).first()
        else:
            result = None
        return result

    def list_statistics(self, skip: int = 0, limit: int = 100) -> List[StatisticModel]:
        """List all statistics with pagination"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(StatisticModel).offset(skip).limit(limit).all()
        else:
            return []

    def list_statistics_by_module(self, module: str) -> List[StatisticModel]:
        """List statistics by source module"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(StatisticModel).filter(
                StatisticModel.source_module == module
            ).all()
        else:
            return []

    def update_statistic(self, statistic_id: int, **kwargs) -> Optional[StatisticModel]:
        """Update statistic fields"""
        stat = self.get_statistic(statistic_id)
        if not stat:
            return None
        for key, value in kwargs.items():
            if hasattr(stat, key):
                setattr(stat, key, value)
        self.session.flush()
        return stat

    def delete_statistic(self, statistic_id: int) -> bool:
        """Delete a statistic and its associated data"""
        stat = self.get_statistic(statistic_id)
        if not stat:
            return False
        # Delete associated timeseries
        if hasattr(self.session, 'sync_session'):
            self.session.sync_session.query(TimeSeriesModel).filter(
                TimeSeriesModel.statistic_id == statistic_id
            ).delete()
            # Delete associated aggregations
            self.session.sync_session.query(AggregationModel).filter(
                AggregationModel.statistic_id == statistic_id
            ).delete()
        # Delete statistic
        self.session.delete(stat)
        self.session.flush()
        return True

    # ==================== TIMESERIES CRUD ====================
    
    def record_value(self, statistic_id: int, value: float, period_start: datetime,
                    period_end: Optional[datetime] = None, dimensions: Dict[str, Any] = None) -> TimeSeriesModel:
        """Record a new timeseries value"""
        ts = TimeSeriesModel(
            statistic_id=statistic_id,
            value=value,
            period_start=period_start,
            period_end=period_end,
            dimensions=dimensions
        )
        self.session.add(ts)
        self.session.flush()
        return ts

    def get_timeseries(self, timeseries_id: int) -> Optional[TimeSeriesModel]:
        """Get timeseries by ID"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(TimeSeriesModel).filter(
                TimeSeriesModel.id == timeseries_id
            ).first()
        return None

    def get_series(self, statistic_id: int, limit: int = 100, 
                   start_date: Optional[datetime] = None, 
                   end_date: Optional[datetime] = None) -> List[TimeSeriesModel]:
        """Get timeseries values for a statistic with optional date range"""
        if hasattr(self.session, 'sync_session'):
            query = self.session.sync_session.query(TimeSeriesModel).filter(
                TimeSeriesModel.statistic_id == statistic_id
            )
            
            if start_date:
                query = query.filter(TimeSeriesModel.period_start >= start_date)
            if end_date:
                query = query.filter(TimeSeriesModel.period_start <= end_date)
            
            return query.order_by(TimeSeriesModel.period_start.desc()).limit(limit).all()
        return []

    def get_latest(self, statistic_id: int) -> Optional[TimeSeriesModel]:
        """Get latest timeseries value for a statistic"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(TimeSeriesModel).filter(
                TimeSeriesModel.statistic_id == statistic_id
            ).order_by(TimeSeriesModel.period_start.desc()).first()
        return None

    def get_series_by_period(self, statistic_id: int, period_start: datetime, 
                            period_end: datetime) -> List[TimeSeriesModel]:
        """Get timeseries values within a period"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(TimeSeriesModel).filter(
                and_(
                    TimeSeriesModel.statistic_id == statistic_id,
                    TimeSeriesModel.period_start >= period_start,
                    TimeSeriesModel.period_start <= period_end
                )
            ).order_by(TimeSeriesModel.period_start.asc()).all()
        return []

    def update_timeseries(self, timeseries_id: int, **kwargs) -> Optional[TimeSeriesModel]:
        """Update timeseries fields"""
        ts = self.get_timeseries(timeseries_id)
        if not ts:
            return None
        for key, value in kwargs.items():
            if hasattr(ts, key):
                setattr(ts, key, value)
        self.session.flush()
        return ts

    def delete_timeseries(self, timeseries_id: int) -> bool:
        """Delete a timeseries value"""
        ts = self.get_timeseries(timeseries_id)
        if not ts:
            return False
        self.session.delete(ts)
        self.session.flush()
        return True

    # ==================== AGGREGATION CRUD ====================
    
    def create_aggregation(self, statistic_id: int, method: str, 
                          parameters: Dict[str, Any] = None) -> AggregationModel:
        """Create a new aggregation rule"""
        agg = AggregationModel(
            statistic_id=statistic_id,
            method=method,
            parameters=parameters
        )
        self.session.add(agg)
        self.session.flush()
        return agg

    def get_aggregation(self, aggregation_id: int) -> Optional[AggregationModel]:
        """Get aggregation by ID"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(AggregationModel).filter(
                AggregationModel.id == aggregation_id
            ).first()
        return None

    def list_aggregations(self, statistic_id: int) -> List[AggregationModel]:
        """List all aggregations for a statistic"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(AggregationModel).filter(
                AggregationModel.statistic_id == statistic_id
            ).all()
        return []

    def update_aggregation(self, aggregation_id: int, **kwargs) -> Optional[AggregationModel]:
        """Update aggregation fields"""
        agg = self.get_aggregation(aggregation_id)
        if not agg:
            return None
        for key, value in kwargs.items():
            if hasattr(agg, key):
                setattr(agg, key, value)
        self.session.flush()
        return agg

    def delete_aggregation(self, aggregation_id: int) -> bool:
        """Delete an aggregation rule"""
        agg = self.get_aggregation(aggregation_id)
        if not agg:
            return False
        self.session.delete(agg)
        self.session.flush()
        return True

    # ==================== BULK OPERATIONS ====================
    
    def bulk_record_values(self, records: List[Dict[str, Any]]) -> List[TimeSeriesModel]:
        """Record multiple timeseries values at once"""
        timeseries_list = []
        for record in records:
            ts = TimeSeriesModel(
                statistic_id=record['statistic_id'],
                value=record['value'],
                period_start=record['period_start'],
                period_end=record.get('period_end'),
                dimensions=record.get('dimensions')
            )
            timeseries_list.append(ts)
        
        self.session.add_all(timeseries_list)
        self.session.flush()
        return timeseries_list

    def delete_series_by_period(self, statistic_id: int, period_start: datetime, 
                                period_end: datetime) -> int:
        """Delete all timeseries values in a period"""
        if hasattr(self.session, 'sync_session'):
            count = self.session.sync_session.query(TimeSeriesModel).filter(
                and_(
                    TimeSeriesModel.statistic_id == statistic_id,
                    TimeSeriesModel.period_start >= period_start,
                    TimeSeriesModel.period_start <= period_end
                )
            ).delete()
        else:
            count = 0
        self.session.flush()
        return count

    # ==================== UTILITIES ====================
    
    def statistic_exists(self, code: str) -> bool:
        """Check if a statistic with given code exists"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(StatisticModel).filter(
                StatisticModel.code == code
            ).first() is not None
        return False

    def count_statistics(self) -> int:
        """Count total statistics"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(StatisticModel).count()
        return 0

    def count_timeseries(self, statistic_id: int) -> int:
        """Count timeseries values for a statistic"""
        if hasattr(self.session, 'sync_session'):
            return self.session.sync_session.query(TimeSeriesModel).filter(
                TimeSeriesModel.statistic_id == statistic_id
            ).count()
        return 0

