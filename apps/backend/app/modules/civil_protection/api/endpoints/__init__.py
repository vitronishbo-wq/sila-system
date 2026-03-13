from app.modules.civil_protection.api.endpoints.atendimentos import router as atendimentos_router
from app.modules.civil_protection.api.endpoints.bombeiros import router as bombeiros_router
from app.modules.civil_protection.api.endpoints.corporacoes import router as corporacoes_router
from app.modules.civil_protection.api.endpoints.despachos import router as despachos_router
from app.modules.civil_protection.api.endpoints.ocorrencias_emergenciais import router as ocorrencias_emergenciais_router
__all__ = ['corporacoes_router', 'bombeiros_router', 'ocorrencias_emergenciais_router', 'despachos_router', 'atendimentos_router']