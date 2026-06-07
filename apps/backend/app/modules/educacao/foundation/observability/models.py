from dataclasses import dataclass
from typing import Any


@dataclass
class MetricSample:
    name: str
    labels: dict[str, Any]
    value: Any
