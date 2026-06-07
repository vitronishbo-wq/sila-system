from typing import Any, Protocol


class AggregationServicePort(Protocol):
    def aggregate(self, *args, **kwargs) -> Any: ...
