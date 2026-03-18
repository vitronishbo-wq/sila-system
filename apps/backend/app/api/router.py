from fastapi import APIRouter
api_router = APIRouter()
try:
    from app.api.routers.events import router as events_router
    api_router.include_router(events_router)
except Exception as e:
    import logging
    logging.warning(f'Failed to include events router: {e}')
try:
    from app.presentation.api.citizen_routes import router as citizen_router
    api_router.include_router(citizen_router)
except Exception:
    pass
try:
    from app.presentation.api.citizen_document_routes import router as citizen_documents_router
    api_router.include_router(citizen_documents_router)
except Exception:
    pass
try:
    from app.modules.wallet.router import router as wallet_router
    api_router.include_router(wallet_router)
except Exception:
    pass
try:
    from app.modules.notifications.router import router as notifications_router
    api_router.include_router(notifications_router)
except Exception:
    pass
try:
    from app.core.sla_engine import sla_router, sla_admin_router
    api_router.include_router(sla_router)
    api_router.include_router(sla_admin_router)
except Exception as e:
    import logging
    logging.warning(f'Failed to include SLA engine routers: {e}')
