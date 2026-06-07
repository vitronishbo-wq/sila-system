from apps.backend.app.modules.resources.florestas.application.ports.agricultura_service_port import (
    AgriculturaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.alerta_desmatamento_repository_port import (
    AlertaDesmatamentoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.ambiente_service_port import (
    AmbienteServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.apreensao_madeira_repository_port import (
    ApreensaoMadeiraRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.arvore_repository_port import (
    ArvoreRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.auto_infracao_florestal_repository_port import (
    AutoInfracaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.autorizacao_supressao_repository_port import (
    AutorizacaoSupressaoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.car_repository_port import (
    CarRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.certificacao_florestal_repository_port import (
    CertificacaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.combate_incendio_repository_port import (
    CombateIncendioRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.comercializacao_florestal_repository_port import (
    ComercializacaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.comercio_externo_service_port import (
    ComercioExternoServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.comunidade_repository_port import (
    ComunidadeRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.concessao_florestal_repository_port import (
    ConcessaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.concessionario_florestal_repository_port import (
    ConcessionarioFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.cra_repository_port import (
    CraRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.credito_carbono_repository_port import (
    CreditoCarbonoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.desmatamento_ilegal_repository_port import (
    DesmatamentoIlegalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.dof_repository_port import (
    DofRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.embargo_florestal_repository_port import (
    EmbargoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.empresa_florestal_repository_port import (
    EmpresaFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.energia_service_port import (
    EnergiaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.especie_florestal_repository_port import (
    EspecieFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.estatistica_florestal_repository_port import (
    EstatisticaFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.exploracao_florestal_repository_port import (
    ExploracaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.exportacao_madeira_repository_port import (
    ExportacaoMadeiraRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.fiscalizacao_florestal_repository_port import (
    FiscalizacaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.foco_calor_repository_port import (
    FocoCalorRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.gestao_fundiaria_service_port import (
    GestaoFundiariaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.incendio_florestal_repository_port import (
    IncendioFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.inventario_florestal_repository_port import (
    InventarioFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.licenca_manejo_repository_port import (
    LicencaManejoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.madeira_repository_port import (
    MadeiraRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.monitoramento_satelite_repository_port import (
    MonitoramentoSateliteRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.multa_florestal_repository_port import (
    MultaFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.ocorrencia_incendio_repository_port import (
    OcorrenciaIncendioRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.outorga_florestal_repository_port import (
    OutorgaFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.plano_manejo_florestal_repository_port import (
    PlanoManejoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.pnfm_repository_port import (
    PnfmRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.produto_florestal_repository_port import (
    ProdutoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.projeto_carbono_repository_port import (
    ProjetoCarbonoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.recuperacao_area_repository_port import (
    RecuperacaoAreaRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.redd_repository_port import (
    ReddRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.reflorestamento_repository_port import (
    ReflorestamentoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.reposicao_florestal_repository_port import (
    ReposicaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.reserva_legal_repository_port import (
    ReservaLegalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.talhao_florestal_repository_port import (
    TalhaoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.unidade_manejo_repository_port import (
    UnidadeManejoRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.viveiro_repository_port import (
    ViveiroRepositoryPort,
)

__all__ = [
    "AgriculturaServicePort",
    "AlertaDesmatamentoRepositoryPort",
    "AmbienteServicePort",
    "ApreensaoMadeiraRepositoryPort",
    "ArvoreRepositoryPort",
    "AutoInfracaoFlorestalRepositoryPort",
    "AutorizacaoSupressaoRepositoryPort",
    "CarRepositoryPort",
    "CertificacaoFlorestalRepositoryPort",
    "CitizenServicePort",
    "CombateIncendioRepositoryPort",
    "ComercializacaoFlorestalRepositoryPort",
    "ComercioExternoServicePort",
    "ComunidadeRepositoryPort",
    "ConcessaoFlorestalRepositoryPort",
    "ConcessionarioFlorestalRepositoryPort",
    "CraRepositoryPort",
    "CreditoCarbonoRepositoryPort",
    "DesmatamentoIlegalRepositoryPort",
    "DofRepositoryPort",
    "EmbargoFlorestalRepositoryPort",
    "EmpresaFlorestalRepositoryPort",
    "EnergiaServicePort",
    "EspecieFlorestalRepositoryPort",
    "EstatisticaFlorestalRepositoryPort",
    "ExploracaoFlorestalRepositoryPort",
    "ExportacaoMadeiraRepositoryPort",
    "FiscalizacaoFlorestalRepositoryPort",
    "FocoCalorRepositoryPort",
    "GeosampaServicePort",
    "GestaoFundiariaServicePort",
    "IncendioFlorestalRepositoryPort",
    "InventarioFlorestalRepositoryPort",
    "LicencaManejoRepositoryPort",
    "MadeiraRepositoryPort",
    "MonitoramentoSateliteRepositoryPort",
    "MultaFlorestalRepositoryPort",
    "OcorrenciaIncendioRepositoryPort",
    "OutorgaFlorestalRepositoryPort",
    "PlanoManejoFlorestalRepositoryPort",
    "PnfmRepositoryPort",
    "ProdutoFlorestalRepositoryPort",
    "ProjetoCarbonoRepositoryPort",
    "RecuperacaoAreaRepositoryPort",
    "ReddRepositoryPort",
    "ReflorestamentoRepositoryPort",
    "ReposicaoFlorestalRepositoryPort",
    "RequestServicePort",
    "ReservaLegalRepositoryPort",
    "TalhaoFlorestalRepositoryPort",
    "UnidadeManejoRepositoryPort",
    "ViveiroRepositoryPort",
]
