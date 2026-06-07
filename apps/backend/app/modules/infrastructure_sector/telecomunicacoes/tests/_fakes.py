from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import (
    AssinanteRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.espectro_repository_port import (
    EspectroRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.indicador_qualidade_repository_port import (
    IndicadorQualidadeRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.infraestrutura_repository_port import (
    InfraestruturaRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import (
    OperadoraRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outorga_espectro_repository_port import (
    OutorgaEspectroRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.qualidade_servico_repository_port import (
    QualidadeServicoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.sla_repository_port import (
    SLARepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusEspectro,
    StatusIndicadorQualidade,
    StatusOutorga,
    StatusQualidadeServico,
    StatusSLA,
    TipoEspectro,
    TipoServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.assinante import (
    Assinante,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.espectro import (
    Espectro,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.indicador_qualidade import (
    IndicadorQualidade,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.infraestrutura_telco import (
    InfraestruturaTelco,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.operadora import (
    Operadora,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.outorga_espectro import (
    OutorgaEspectro,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.qualidade_servico import (
    QualidadeServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.sla import SLA


class InMemoryOperadoraRepository(OperadoraRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Operadora] = {}

    async def save(self, operadora: Operadora) -> Operadora:
        self._items[operadora.id] = operadora
        return operadora

    async def get_by_id(self, operadora_id: UUID) -> Operadora | None:
        return self._items.get(operadora_id)

    async def get_by_cnpj(self, cnpj: str) -> Operadora | None:
        normalized = cnpj.strip()
        for item in self._items.values():
            if item.cnpj == normalized:
                return item
        return None

    async def list_all(self) -> list[Operadora]:
        return sorted(self._items.values(), key=lambda item: item.razao_social)

    async def list_by_servico(self, servico: TipoServico) -> list[Operadora]:
        items = [item for item in self._items.values() if servico in item.servicos_autorizados]
        return sorted(items, key=lambda item: item.razao_social)

    async def list_by_municipio(self, municipio: str) -> list[Operadora]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.razao_social)

    async def list_ativas(self) -> list[Operadora]:
        items = [item for item in self._items.values() if item.ativo]
        return sorted(items, key=lambda item: item.razao_social)

    async def delete(self, operadora_id: UUID) -> bool:
        return self._items.pop(operadora_id, None) is not None


class InMemoryAssinanteRepository(AssinanteRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Assinante] = {}

    async def save(self, assinante: Assinante) -> Assinante:
        self._items[assinante.id] = assinante
        return assinante

    async def get_by_id(self, assinante_id: UUID) -> Assinante | None:
        return self._items.get(assinante_id)

    async def get_by_codigo(self, codigo_assinante: str) -> Assinante | None:
        normalized = codigo_assinante.strip()
        for item in self._items.values():
            if item.codigo_assinante == normalized:
                return item
        return None

    async def get_by_citizen(self, citizen_id: UUID) -> Assinante | None:
        for item in sorted(self._items.values(), key=lambda row: row.data_adesao, reverse=True):
            if item.citizen_id == citizen_id:
                return item
        return None

    async def list_all(self) -> list[Assinante]:
        return sorted(self._items.values(), key=lambda item: item.codigo_assinante)

    async def list_by_operadora(self, operadora_id: UUID) -> list[Assinante]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.codigo_assinante)

    async def list_by_municipio(self, municipio: str) -> list[Assinante]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.codigo_assinante)

    async def list_ativos(self) -> list[Assinante]:
        items = [item for item in self._items.values() if item.ativo]
        return sorted(items, key=lambda item: item.codigo_assinante)

    async def delete(self, assinante_id: UUID) -> bool:
        return self._items.pop(assinante_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"ASS/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_assinante.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryInfraestruturaRepository(InfraestruturaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, InfraestruturaTelco] = {}

    async def save(self, infraestrutura: InfraestruturaTelco) -> InfraestruturaTelco:
        self._items[infraestrutura.id] = infraestrutura
        return infraestrutura

    async def get_by_id(self, infraestrutura_id: UUID) -> InfraestruturaTelco | None:
        return self._items.get(infraestrutura_id)

    async def get_by_codigo(self, codigo_infra: str) -> InfraestruturaTelco | None:
        normalized = codigo_infra.strip()
        for item in self._items.values():
            if item.codigo_infra == normalized:
                return item
        return None

    async def list_all(self) -> list[InfraestruturaTelco]:
        return sorted(self._items.values(), key=lambda item: item.codigo_infra)

    async def list_by_operadora(self, operadora_id: UUID) -> list[InfraestruturaTelco]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.codigo_infra)

    async def list_by_municipio(self, municipio: str) -> list[InfraestruturaTelco]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.codigo_infra)

    async def list_ativas(self) -> list[InfraestruturaTelco]:
        items = [item for item in self._items.values() if item.ativo]
        return sorted(items, key=lambda item: item.codigo_infra)

    async def delete(self, infraestrutura_id: UUID) -> bool:
        return self._items.pop(infraestrutura_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"INF/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_infra.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryOutorgaEspectroRepository(OutorgaEspectroRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, OutorgaEspectro] = {}

    async def save(self, outorga: OutorgaEspectro) -> OutorgaEspectro:
        self._items[outorga.id] = outorga
        return outorga

    async def get_by_id(self, outorga_id: UUID) -> OutorgaEspectro | None:
        return self._items.get(outorga_id)

    async def get_by_numero(self, numero_outorga: str) -> OutorgaEspectro | None:
        normalized = numero_outorga.strip()
        for item in self._items.values():
            if item.numero_outorga == normalized:
                return item
        return None

    async def list_all(self) -> list[OutorgaEspectro]:
        return sorted(self._items.values(), key=lambda item: item.numero_outorga)

    async def list_by_operadora(self, operadora_id: UUID) -> list[OutorgaEspectro]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.numero_outorga)

    async def list_by_status(self, status: StatusOutorga) -> list[OutorgaEspectro]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.numero_outorga)

    async def delete(self, outorga_id: UUID) -> bool:
        return self._items.pop(outorga_id, None) is not None

    async def next_numero(self) -> str:
        year = date.today().year
        prefix = f"OUT/{year}/"
        count = sum(1 for item in self._items.values() if item.numero_outorga.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryEspectroRepository(EspectroRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Espectro] = {}

    async def save(self, espectro: Espectro) -> Espectro:
        self._items[espectro.id] = espectro
        return espectro

    async def get_by_id(self, espectro_id: UUID) -> Espectro | None:
        return self._items.get(espectro_id)

    async def get_by_codigo(self, codigo_espectro: str) -> Espectro | None:
        normalized = codigo_espectro.strip()
        for item in self._items.values():
            if item.codigo_espectro == normalized:
                return item
        return None

    async def list_all(self) -> list[Espectro]:
        return sorted(self._items.values(), key=lambda item: item.codigo_espectro)

    async def list_by_tipo(self, tipo: TipoEspectro) -> list[Espectro]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.codigo_espectro)

    async def list_by_municipio(self, municipio: str) -> list[Espectro]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.codigo_espectro)

    async def list_by_status(self, status: StatusEspectro) -> list[Espectro]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.codigo_espectro)

    async def delete(self, espectro_id: UUID) -> bool:
        return self._items.pop(espectro_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"ESP/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_espectro.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemorySLARepository(SLARepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, SLA] = {}

    async def save(self, sla: SLA) -> SLA:
        self._items[sla.id] = sla
        return sla

    async def get_by_id(self, sla_id: UUID) -> SLA | None:
        return self._items.get(sla_id)

    async def get_by_codigo(self, codigo_sla: str) -> SLA | None:
        normalized = codigo_sla.strip()
        for item in self._items.values():
            if item.codigo_sla == normalized:
                return item
        return None

    async def find_ativo_por_operadora_servico(
        self, operadora_id: UUID, servico: TipoServico
    ) -> SLA | None:
        for item in sorted(self._items.values(), key=lambda row: row.data_inicio, reverse=True):
            if (
                item.operadora_id == operadora_id
                and item.servico == servico
                and (item.status == StatusSLA.ATIVO)
            ):
                return item
        return None

    async def list_all(self) -> list[SLA]:
        return sorted(self._items.values(), key=lambda item: item.codigo_sla)

    async def list_by_operadora(self, operadora_id: UUID) -> list[SLA]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.codigo_sla)

    async def list_by_status(self, status: StatusSLA) -> list[SLA]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.codigo_sla)

    async def delete(self, sla_id: UUID) -> bool:
        return self._items.pop(sla_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"SLA/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_sla.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryQualidadeServicoRepository(QualidadeServicoRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, QualidadeServico] = {}

    async def save(self, medicao: QualidadeServico) -> QualidadeServico:
        self._items[medicao.id] = medicao
        return medicao

    async def get_by_id(self, medicao_id: UUID) -> QualidadeServico | None:
        return self._items.get(medicao_id)

    async def get_by_codigo(self, codigo_medicao: str) -> QualidadeServico | None:
        normalized = codigo_medicao.strip()
        for item in self._items.values():
            if item.codigo_medicao == normalized:
                return item
        return None

    async def list_all(self) -> list[QualidadeServico]:
        return sorted(self._items.values(), key=lambda item: item.codigo_medicao)

    async def list_by_operadora(self, operadora_id: UUID) -> list[QualidadeServico]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.codigo_medicao)

    async def list_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> list[QualidadeServico]:
        items = [
            item
            for item in self._items.values()
            if item.operadora_id == operadora_id
            and item.data_medicao.year == referencia_ano
            and (item.data_medicao.month == referencia_mes)
        ]
        return sorted(items, key=lambda item: item.codigo_medicao)

    async def list_by_assinante(self, assinante_id: UUID) -> list[QualidadeServico]:
        items = [item for item in self._items.values() if item.assinante_id == assinante_id]
        return sorted(items, key=lambda item: item.codigo_medicao)

    async def list_by_status(self, status: StatusQualidadeServico) -> list[QualidadeServico]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.codigo_medicao)

    async def delete(self, medicao_id: UUID) -> bool:
        return self._items.pop(medicao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"QLT/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_medicao.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryIndicadorQualidadeRepository(IndicadorQualidadeRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, IndicadorQualidade] = {}

    async def save(self, indicador: IndicadorQualidade) -> IndicadorQualidade:
        self._items[indicador.id] = indicador
        return indicador

    async def get_by_id(self, indicador_id: UUID) -> IndicadorQualidade | None:
        return self._items.get(indicador_id)

    async def get_by_codigo(self, codigo_indicador: str) -> IndicadorQualidade | None:
        normalized = codigo_indicador.strip()
        for item in self._items.values():
            if item.codigo_indicador == normalized:
                return item
        return None

    async def get_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> IndicadorQualidade | None:
        for item in self._items.values():
            if (
                item.operadora_id == operadora_id
                and item.referencia_ano == referencia_ano
                and (item.referencia_mes == referencia_mes)
            ):
                return item
        return None

    async def list_all(self) -> list[IndicadorQualidade]:
        return sorted(self._items.values(), key=lambda item: item.codigo_indicador)

    async def list_by_operadora(self, operadora_id: UUID) -> list[IndicadorQualidade]:
        items = [item for item in self._items.values() if item.operadora_id == operadora_id]
        return sorted(items, key=lambda item: item.codigo_indicador)

    async def list_by_status(self, status: StatusIndicadorQualidade) -> list[IndicadorQualidade]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.codigo_indicador)

    async def delete(self, indicador_id: UUID) -> bool:
        return self._items.pop(indicador_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"IND/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_indicador.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class FakeCitizenService(CitizenServicePort):
    def __init__(self, *, active: bool = True) -> None:
        self.active = active

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        return self.active


class FakeRequestService(RequestServicePort):
    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        metadata: dict | None = None,
        citizen_id: UUID | None = None,
        numero_processo: str | None = None,
    ) -> UUID | None:
        return None
