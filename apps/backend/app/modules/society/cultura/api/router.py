from fastapi import APIRouter
from apps.backend.app.modules.society.cultura.api.endpoints import artistas_router, bens_culturais_router, editais_router, espacos_culturais_router, eventos_culturais_router, grupos_artisticos_router, patrimonios_imateriais_router, projetos_culturais_router
router = APIRouter(prefix='/cultura', tags=['Cultura'])
router.include_router(artistas_router)
router.include_router(bens_culturais_router)
router.include_router(espacos_culturais_router)
router.include_router(projetos_culturais_router)
router.include_router(editais_router)
router.include_router(eventos_culturais_router)
router.include_router(grupos_artisticos_router)
router.include_router(patrimonios_imateriais_router)