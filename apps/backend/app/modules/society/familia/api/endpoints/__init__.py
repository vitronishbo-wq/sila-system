from apps.backend.app.modules.society.familia.api.endpoints.aggregates import (
    router as aggregates_router,
)
from apps.backend.app.modules.society.familia.api.endpoints.dependencies import (
    router as dependencies_router,
)
from apps.backend.app.modules.society.familia.api.endpoints.history import router as history_router
from apps.backend.app.modules.society.familia.api.endpoints.members import router as members_router
from apps.backend.app.modules.society.familia.api.endpoints.projections import (
    router as projections_router,
)
from apps.backend.app.modules.society.familia.api.endpoints.relationships import (
    router as relationships_router,
)

__all__ = [
    "aggregates_router",
    "members_router",
    "relationships_router",
    "dependencies_router",
    "history_router",
    "projections_router",
]
