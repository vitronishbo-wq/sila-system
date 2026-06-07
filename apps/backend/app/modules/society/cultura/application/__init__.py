from apps.backend.app.modules.society.cultura.application.handlers import register_handlers
from apps.backend.app.modules.society.cultura.application.services import (
    ArtistaService,
    BemCulturalService,
    EditalService,
    EspacoCulturalService,
    EventoCulturalService,
    GrupoArtisticoService,
    PatrimonioImaterialService,
    ProjetoCulturalService,
)

__all__ = [
    "register_handlers",
    "ArtistaService",
    "BemCulturalService",
    "EspacoCulturalService",
    "ProjetoCulturalService",
    "EditalService",
    "EventoCulturalService",
    "GrupoArtisticoService",
    "PatrimonioImaterialService",
]
