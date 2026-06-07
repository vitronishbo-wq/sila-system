from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.alvara_schema import (
    AlvaraCreate,
    AlvaraDeferimentoInput,
    AlvaraMotivoInput,
    AlvaraResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.habite_se_schema import (
    HabiteSeCreate,
    HabiteSeEmissaoInput,
    HabiteSeMotivoInput,
    HabiteSeResponse,
    HabiteSeVistoriaInput,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.licenca_urbanistica_schema import (
    LicencaUrbanisticaCreate,
    LicencaUrbanisticaDeferimentoInput,
    LicencaUrbanisticaMotivoInput,
    LicencaUrbanisticaResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.loteamento_schema import (
    LoteamentoConclusaoInput,
    LoteamentoCreate,
    LoteamentoImplantacaoInput,
    LoteamentoInicioInput,
    LoteamentoMotivoInput,
    LoteamentoResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.operacao_urbana_schema import (
    OperacaoUrbanaConclusaoInput,
    OperacaoUrbanaCreate,
    OperacaoUrbanaExecucaoInput,
    OperacaoUrbanaInicioInput,
    OperacaoUrbanaMotivoInput,
    OperacaoUrbanaResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.parcelamento_schema import (
    ParcelamentoConclusaoInput,
    ParcelamentoCreate,
    ParcelamentoMotivoInput,
    ParcelamentoResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.plano_diretor_schema import (
    PlanoDiretorAprovacaoCamaraInput,
    PlanoDiretorAudienciaInput,
    PlanoDiretorCreate,
    PlanoDiretorResponse,
    PlanoDiretorSancaoInput,
    PlanoDiretorValidadeInput,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.zoneamento_schema import (
    ZoneamentoCreate,
    ZoneamentoMotivoInput,
    ZoneamentoParametrosInput,
    ZoneamentoResponse,
    ZoneamentoVigenciaInput,
)

__all__ = [
    "PlanoDiretorCreate",
    "PlanoDiretorAudienciaInput",
    "PlanoDiretorAprovacaoCamaraInput",
    "PlanoDiretorSancaoInput",
    "PlanoDiretorValidadeInput",
    "PlanoDiretorResponse",
    "ZoneamentoCreate",
    "ZoneamentoVigenciaInput",
    "ZoneamentoMotivoInput",
    "ZoneamentoParametrosInput",
    "ZoneamentoResponse",
    "OperacaoUrbanaCreate",
    "OperacaoUrbanaInicioInput",
    "OperacaoUrbanaExecucaoInput",
    "OperacaoUrbanaConclusaoInput",
    "OperacaoUrbanaMotivoInput",
    "OperacaoUrbanaResponse",
    "ParcelamentoCreate",
    "ParcelamentoConclusaoInput",
    "ParcelamentoMotivoInput",
    "ParcelamentoResponse",
    "LoteamentoCreate",
    "LoteamentoInicioInput",
    "LoteamentoImplantacaoInput",
    "LoteamentoConclusaoInput",
    "LoteamentoMotivoInput",
    "LoteamentoResponse",
    "LicencaUrbanisticaCreate",
    "LicencaUrbanisticaDeferimentoInput",
    "LicencaUrbanisticaMotivoInput",
    "LicencaUrbanisticaResponse",
    "AlvaraCreate",
    "AlvaraDeferimentoInput",
    "AlvaraMotivoInput",
    "AlvaraResponse",
    "HabiteSeCreate",
    "HabiteSeVistoriaInput",
    "HabiteSeEmissaoInput",
    "HabiteSeMotivoInput",
    "HabiteSeResponse",
]
