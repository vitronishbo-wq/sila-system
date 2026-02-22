from fastapi import APIRouter, status

# Router principal do módulo training
router = APIRouter(tags=["Training"])


# Health check endpoint
@router.get("/ping")
async def ping():
    """Health check para o módulo training"""
    return {"status": "ok", "module": "training"}


# Status check endpoint
@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Status Check for Training Module",
)
async def get_training_status():
    """
    Status check para o módulo training
    """
    return {
        "module": "training",
        "status": "operational",
        "timestamp": status.HTTP_200_OK,
    }
