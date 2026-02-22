from fastapi import APIRouter

# Create an APIRouter instance to be imported by __init__.py
router = APIRouter(
    prefix="/appointments",  # Base path for all routes in this module
    tags=["Appointments"],  # Tag used in Swagger/OpenAPI documentation
)


# Health check endpoint
@router.get("/ping")
async def ping():
    """Health check para o módulo appointments"""
    return {"status": "ok", "module": "appointments"}
