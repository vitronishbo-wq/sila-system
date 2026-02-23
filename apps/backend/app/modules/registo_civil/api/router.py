from fastapi import APIRouter
from .events.birth_routes import router as birth_events
from .events.marriage_routes import router as marriage_events
from .events.death_routes import router as death_events
from .certificates.certificate_routes import router as certificates

router = APIRouter()

# middleware será adicionado na app principal

# Eventos Civis
router.include_router(birth_events, prefix="/events")
router.include_router(marriage_events, prefix="/events")
router.include_router(death_events, prefix="/events")

# Certidões
router.include_router(certificates, prefix="/certificates")
