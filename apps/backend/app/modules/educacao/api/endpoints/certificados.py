from app.modules.educacao.api.deps import get_certificado_service
from app.modules.educacao.api.endpoints._workflow_endpoints import build_workflow_router
from app.modules.educacao.api.schemas.certificado_schema import CertificadoCancelar, CertificadoConcluir, CertificadoCreate, CertificadoResponse

router = build_workflow_router(
    tag="Educacao - Certificados",
    get_service=get_certificado_service,
    create_schema=CertificadoCreate,
    response_schema=CertificadoResponse,
    concluir_schema=CertificadoConcluir,
    cancelar_schema=CertificadoCancelar,
    routes=[
        ("/certificados/conclusao", "certificado_conclusao"),
        ("/historicos", "historico_escolar"),
        ("/declaracoes", "declaracao_escolar"),
        ("/certificados/universitario", "certificado_universitario"),
    ],
)
