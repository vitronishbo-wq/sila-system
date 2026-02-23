from fastapi import APIRouter

# Module temporarily disabled due to missing dependencies
# TODO: Fix saude_primaria deps before re-enabling
# from .api.router import router

def get_module_router() -> APIRouter:
    # Returning empty router until saude_primaria is fixed
    return APIRouter()

__all__ = ["get_module_router"]