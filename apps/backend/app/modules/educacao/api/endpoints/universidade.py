from apps.backend.app.modules.educacao.api.deps import get_universidade_service
from apps.backend.app.modules.educacao.api.endpoints._workflow_endpoints import (
    build_workflow_router,
)
from apps.backend.app.modules.educacao.api.schemas.universidade_schema import (
    UniversidadeCancelar,
    UniversidadeConcluir,
    UniversidadeCreate,
    UniversidadeResponse,
)

router = build_workflow_router(
    tag="Educacao - Superior",
    get_service=get_universidade_service,
    create_schema=UniversidadeCreate,
    response_schema=UniversidadeResponse,
    concluir_schema=UniversidadeConcluir,
    cancelar_schema=UniversidadeCancelar,
    routes=[
        ("/matriculas/universidade", "matricula_universidade"),
        ("/reconhecimentos/diploma", "reconhecimento_diploma"),
        ("/reconhecimentos/grau", "reconhecimento_grau"),
        ("/parcerias/universidade", "parceria_universidade"),
        ("/avaliacoes/institucional", "avaliacao_institucional"),
        ("/acreditacoes/universitaria", "acreditacao_universitaria"),
        ("/mobilidade/academica", "mobilidade_academica"),
        ("/estatisticas/superior", "estatistica_superior"),
    ],
)
