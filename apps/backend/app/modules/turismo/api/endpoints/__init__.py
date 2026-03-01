from app.modules.turismo.api.endpoints.operadores_turisticos import router as operadores_turisticos_router
from app.modules.turismo.api.endpoints.agencias_viagens import router as agencias_viagens_router
from app.modules.turismo.api.endpoints.guias_turismo import router as guias_turismo_router
from app.modules.turismo.api.endpoints.hoteis import router as hoteis_router
from app.modules.turismo.api.endpoints.pousadas import router as pousadas_router
from app.modules.turismo.api.endpoints.resorts import router as resorts_router
from app.modules.turismo.api.endpoints.atracao_turisticas import router as atracao_turisticas_router
from app.modules.turismo.api.endpoints.pontos_turisticos import router as pontos_turisticos_router
from app.modules.turismo.api.endpoints.eventos import router as eventos_router
from app.modules.turismo.api.endpoints.pacotes import router as pacotes_router
from app.modules.turismo.api.endpoints.roteiros import router as roteiros_router
from app.modules.turismo.api.endpoints.reservas import router as reservas_router
from app.modules.turismo.api.endpoints.avaliacoes import router as avaliacoes_router
from app.modules.turismo.api.endpoints.reclamacoes_turismo import router as reclamacoes_turismo_router
from app.modules.turismo.api.endpoints.cadastro_turistas import router as cadastro_turistas_router
from app.modules.turismo.api.endpoints.fluxo_turistico import router as fluxo_turistico_router
from app.modules.turismo.api.endpoints.ocupacao_hoteleira import router as ocupacao_hoteleira_router
from app.modules.turismo.api.endpoints.tarifas_hotel import router as tarifas_hotel_router
from app.modules.turismo.api.endpoints.temporadas import router as temporadas_router
from app.modules.turismo.api.endpoints.promocoes_turisticas import router as promocoes_turisticas_router
from app.modules.turismo.api.endpoints.licencas_turismo import router as licencas_turismo_router
from app.modules.turismo.api.endpoints.cadastur import router as cadastur_router
from app.modules.turismo.api.endpoints.registros_guia import router as registros_guia_router
from app.modules.turismo.api.endpoints.fiscalizacoes_turismo import router as fiscalizacoes_turismo_router
from app.modules.turismo.api.endpoints.autos_infracao_turismo import router as autos_infracao_turismo_router
from app.modules.turismo.api.endpoints.multas_turismo import router as multas_turismo_router
from app.modules.turismo.api.endpoints.classificacoes_hoteleiras import router as classificacoes_hoteleiras_router
from app.modules.turismo.api.endpoints.certificacoes_turisticas import router as certificacoes_turisticas_router
from app.modules.turismo.api.endpoints.estatisticas_turismo import router as estatisticas_turismo_router
from app.modules.turismo.api.endpoints.chegadas_turistas import router as chegadas_turistas_router
from app.modules.turismo.api.endpoints.receitas_turisticas import router as receitas_turisticas_router

__all__ = [
    "operadores_turisticos_router",
    "agencias_viagens_router",
    "guias_turismo_router",
    "hoteis_router",
    "pousadas_router",
    "resorts_router",
    "atracao_turisticas_router",
    "pontos_turisticos_router",
    "eventos_router",
    "pacotes_router",
    "roteiros_router",
    "reservas_router",
    "avaliacoes_router",
    "reclamacoes_turismo_router",
    "cadastro_turistas_router",
    "fluxo_turistico_router",
    "ocupacao_hoteleira_router",
    "tarifas_hotel_router",
    "temporadas_router",
    "promocoes_turisticas_router",
    "licencas_turismo_router",
    "cadastur_router",
    "registros_guia_router",
    "fiscalizacoes_turismo_router",
    "autos_infracao_turismo_router",
    "multas_turismo_router",
    "classificacoes_hoteleiras_router",
    "certificacoes_turisticas_router",
    "estatisticas_turismo_router",
    "chegadas_turistas_router",
    "receitas_turisticas_router",
]
