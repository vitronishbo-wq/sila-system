from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.assinante_schema import (
    AssinanteCreate,
    AssinanteResponse,
    AssinanteStatusUpdate,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.espectro_schema import (
    EspectroCreate,
    EspectroResponse,
    EspectroStatusUpdate,
    EspectroVincularOutorga,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.fatura_schema import (
    FaturaGerarInput,
    FaturaTelecomResponse,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.indicador_qualidade_schema import (
    IndicadorQualidadeGerar,
    IndicadorQualidadeResponse,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.infraestrutura_schema import (
    InfraestruturaCreate,
    InfraestruturaResponse,
    InfraestruturaStatusUpdate,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.operadora_schema import (
    OperadoraAuthorize,
    OperadoraCreate,
    OperadoraResponse,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.outorga_espectro_schema import (
    OutorgaEspectroCreate,
    OutorgaEspectroResponse,
    OutorgaEspectroStatusUpdate,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.qualidade_servico_schema import (
    QualidadeServicoCreate,
    QualidadeServicoResponse,
    QualidadeServicoStatusUpdate,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.reclamacao_schema import (
    ReclamacaoCreate,
    ReclamacaoResponse,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.sla_schema import (
    SLACreate,
    SLAResponse,
    SLAStatusUpdate,
)

__all__ = [
    "OperadoraCreate",
    "OperadoraAuthorize",
    "OperadoraResponse",
    "AssinanteCreate",
    "AssinanteStatusUpdate",
    "AssinanteResponse",
    "InfraestruturaCreate",
    "InfraestruturaStatusUpdate",
    "InfraestruturaResponse",
    "OutorgaEspectroCreate",
    "OutorgaEspectroStatusUpdate",
    "OutorgaEspectroResponse",
    "EspectroCreate",
    "EspectroStatusUpdate",
    "EspectroVincularOutorga",
    "EspectroResponse",
    "FaturaGerarInput",
    "FaturaTelecomResponse",
    "SLACreate",
    "SLAStatusUpdate",
    "SLAResponse",
    "QualidadeServicoCreate",
    "QualidadeServicoStatusUpdate",
    "QualidadeServicoResponse",
    "IndicadorQualidadeGerar",
    "IndicadorQualidadeResponse",
    "ReclamacaoCreate",
    "ReclamacaoResponse",
]
