from fastapi import APIRouter
from app.modules.society.familia.api.endpoints import aggregates_router, dependencies_router, history_router, members_router, projections_router, relationships_router
router = APIRouter(prefix='/familia', tags=['Familia'])
router.include_router(aggregates_router)
router.include_router(members_router)
router.include_router(relationships_router)
router.include_router(dependencies_router)
router.include_router(history_router)
router.include_router(projections_router)