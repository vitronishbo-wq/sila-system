# X-Road Ports Pattern: Breaking Circular Dependencies

This pattern ensures modules can integrate without creating circular imports or tight coupling.

## Problem: Point-to-Point Adapters

Before consolidation, adapters created chaos:

```python
# ❌ BAD: Justice module directly imports Health adapters
from app.modules.health.adapters import HealthCheckAdapter
from app.modules.finance.adapters import BillingAdapter

class CitizenService:
    def __init__(self):
        self.health = HealthCheckAdapter()  # Direct dependency
        self.finance = BillingAdapter()      # Direct dependency

    def register_citizen(self, citizen):
        # Circular: Health module might import Justice
        self.health.check_status(citizen.id)
```

**Results**:
- Module A → B, Module B → A = circular (import fails at runtime)
- 900 modules with point-to-point = 900×899 possible circular paths
- Impossible to test modules independently

## Solution: Standardized Ports

Each module defines **inbound ports** (interfaces) for what it needs. External callers provide implementations.

### Pattern: Port as Interface

In `app/modules/justice/core/infrastructure/ports/`:

```python
# ports/health_check_port.py
"""Port defining how Justice interacts with Health module."""
from abc import ABC, abstractmethod

class HealthCheckPort(ABC):
    """Interface for health-related queries (agnostic to implementation)"""
    
    @abstractmethod
    async def citizen_has_active_health_record(self, citizen_id: str) -> bool:
        """Check if citizen has active health record"""
        pass
    
    @abstractmethod
    async def get_health_status(self, citizen_id: str) -> str:
        """Get health status (values: 'active', 'inactive', 'suspended')"""
        pass
```

```python
# application/services/citizen_service.py
"""Application service using ports, not concrete adapters."""
from dataclasses import dataclass
from .ports.health_check_port import HealthCheckPort

@dataclass
class CitizenService:
    health_port: HealthCheckPort  # Injected, not imported
    
    async def register_citizen(self, citizen):
        # Call via port (resolution happens externally)
        status = await self.health_port.get_health_status(citizen.id)
        # ... rest of logic
```

### Implementation: X-Road Adapter

The adapter **lives in infrastructure** and implements the port:

```python
# app/modules/justice/core/infrastructure/adapters/xroad_health_adapter.py
"""X-Road implementation of health port."""
import httpx
from ..ports.health_check_port import HealthCheckPort

class XRoadHealthAdapter(HealthCheckPort):
    def __init__(self, xroad_endpoint: str):
        self.xroad_endpoint = xroad_endpoint
    
    async def citizen_has_active_health_record(self, citizen_id: str) -> bool:
        # Call Health module via X-Road (not direct import)
        response = await httpx.get(
            f"{self.xroad_endpoint}/health/citizen/{citizen_id}/record"
        )
        return response.json().get("exists", False)
    
    async def get_health_status(self, citizen_id: str) -> str:
        response = await httpx.get(
            f"{self.xroad_endpoint}/health/citizen/{citizen_id}/status"
        )
        return response.json().get("status", "unknown")
```

### Wiring: Dependency Injection

**No imports between core modules. Resolution happens at application bootstrap.**

```python
# app/startup.py or app/dependencies.py
"""Application dependency injection container."""
from app.modules.justice.core.application.services import CitizenService
from app.modules.justice.core.infrastructure.adapters import XRoadHealthAdapter
from app.modules.justice.core.infrastructure.adapters import XRoadBillingAdapter

# Resolution happens here, not in service code
health_adapter = XRoadHealthAdapter(
    xroad_endpoint=config.XROAD_HEALTH_ENDPOINT
)
billing_adapter = XRoadBillingAdapter(
    xroad_endpoint=config.XROAD_FINANCE_ENDPOINT
)

citizen_service = CitizenService(
    health_port=health_adapter,
    billing_port=billing_adapter
)
```

### Result: Clean Boundary

```
Justice Module:
┌─────────────────────────────────────┐
│ application/                        │
│  └─ services/                       │
│       └─ CitizenService             │
│          (depends on ports)         │
├─────────────────────────────────────┤
│ infrastructure/                     │
│  ├─ ports/                          │
│  │  ├─ health_check_port.py (ABC)   │
│  │  └─ billing_port.py (ABC)        │
│  └─ adapters/                       │
│     ├─ xroad_health_adapter.py      │
│     └─ xroad_billing_adapter.py     │
└─────────────────────────────────────┘
         ⬇ (HTTP calls only)
    External Modules
    (via X-Road)
```

## Rules

### For Every Module
1. **Define ports in `infrastructure/ports/`** for every external dependency
2. **Services depend on ports (ABC)**, not concrete adapters
3. **Adapters implement ports** and live in `infrastructure/adapters/`
4. **No imports between core modules** — only through ports

### For Adapters
1. **HTTP/X-Road calls only** (no SDKs with circular back-references)
2. **Stateless** (all state in domain or repositories)
3. **Error handling** — timeouts, retries, circuit breakers
4. **Typed** — use dataclasses for request/response DTOs

### For Testing
1. **Mock ports** in unit tests (no real X-Road calls)
2. **Integration tests** use real adapters with Docker services
3. **Contract tests** verify X-Road compatibility

## Example: Health Module's BI Verification Port

**Reverse: Health module depends on Justice (to verify BI)**

```python
# app/modules/health/core/infrastructure/ports/bi_verifier_port.py
"""Port for BI verification (implemented by Justice module)"""
from abc import ABC, abstractmethod

class BIVerifierPort(ABC):
    @abstractmethod
    async def verify_bi_authenticity(self, bi_number: str) -> bool:
        """Verify BI is authentic and not revoked"""
        pass
```

```python
# app/modules/health/core/infrastructure/adapters/xroad_bi_adapter.py
class BIVerifierXRoadAdapter(BIVerifierPort):
    async def verify_bi_authenticity(self, bi_number: str) -> bool:
        response = await httpx.get(
            f"{self.xroad_endpoint}/justice/bi/verify/{bi_number}"
        )
        return response.json().get("authentic", False)
```

**Result**: 
- Justice doesn't import Health
- Health doesn't import Justice
- Both use X-Road as neutral intermediary
- No circular dependencies possible

## Scaling to 900 Services

With this pattern:
- Each module ≤ 20 ports (interfaces)
- 900 modules × 20 ports = 18,000 total port definitions
- All resolvable at boot time (dependency injection container)
- No runtime import errors
- Audit-safe (every cross-module call visible in application bootstrap)

## Anti-Patterns to Avoid

❌ **Direct imports between modules**
```python
# BAD
from app.modules.health.services import HealthService
```

❌ **Service directly creating adapters**
```python
# BAD
class CitizenService:
    def __init__(self):
        self.health = HealthServiceDirectly()  # Creates its own dependency
```

❌ **Adapters with complex logic**
```python
# BAD: Adapter should only translate, not enrich
class HealthAdapter:
    def check_and_enrich(self, citizen):
        # Business logic shouldn't be here
        pass
```

✅ **Services use injected ports**
```python
# GOOD
class CitizenService:
    def __init__(self, health_port: HealthCheckPort):
        self.health_port = health_port  # Injected abstraction
```

✅ **Adapters are thin translators**
```python
# GOOD: Call X-Road, return data
class XRoadHealthAdapter(HealthCheckPort):
    async def get_status(self, id: str) -> str:
        response = await httpx.get(f"{self.endpoint}/status/{id}")
        return response.json()["status"]
```
