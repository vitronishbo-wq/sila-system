"""Router endpoints for module"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/intelligence", tags=["endpoints"])


@router.get("/", summary="List Module Endpoints")
async def list_endpoints() -> dict[str, Any]:
    """
    List all available endpoints in this module.

    Returns:
        Dict with endpoint information
    """
    return {"module": __name__.split(".")[3], "version": "1.0.0", "endpoints": []}
