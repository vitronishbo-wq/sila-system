"""Cache metrics and statistics tracking"""

from typing import Optional, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    errors: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def total_requests(self) -> int:
        """Total get operations"""
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        """Cache hit rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100
    
    @property
    def uptime(self) -> timedelta:
        """Time since metrics started"""
        return datetime.now() - self.start_time
    
    def record_hit(self):
        """Record cache hit"""
        self.hits += 1
    
    def record_miss(self):
        """Record cache miss"""
        self.misses += 1
    
    def record_set(self):
        """Record cache set operation"""
        self.sets += 1
    
    def record_delete(self):
        """Record cache delete operation"""
        self.deletes += 1
    
    def record_error(self):
        """Record cache error"""
        self.errors += 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'sets': self.sets,
            'deletes': self.deletes,
            'errors': self.errors,
            'total_requests': self.total_requests,
            'hit_rate': round(self.hit_rate, 2),
            'uptime_seconds': self.uptime.total_seconds(),
        }
    
    def reset(self):
        """Reset all metrics"""
        self.hits = 0
        self.misses = 0
        self.sets = 0
        self.deletes = 0
        self.errors = 0
        self.start_time = datetime.now()


# Global metrics instance
_metrics_instance: Optional[CacheMetrics] = None


def get_metrics() -> CacheMetrics:
    """Get global cache metrics instance"""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = CacheMetrics()
    return _metrics_instance


def reset_metrics():
    """Reset global metrics"""
    global _metrics_instance
    if _metrics_instance:
        _metrics_instance.reset()
    else:
        _metrics_instance = CacheMetrics()


def report_metrics() -> Dict:
    """Get metrics report"""
    metrics = get_metrics()
    return metrics.to_dict()
