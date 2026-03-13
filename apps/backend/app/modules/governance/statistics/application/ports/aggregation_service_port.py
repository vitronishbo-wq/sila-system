from typing import Protocol, Any

class AggregationServicePort(Protocol):

    def aggregate(self, *args, **kwargs) -> Any:
        ...