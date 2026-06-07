from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID

from apps.backend.app.modules.public_security.application.ports.cadeia_custodia_repository_port import (
    CadeiaCustodiaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.evidencia_repository_port import (
    EvidenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.investigacao_repository_port import (
    InvestigacaoRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.laudo_pericial_repository_port import (
    LaudoPericialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.mandado_repository_port import (
    MandadoRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.ocorrencia_repository_port import (
    OcorrenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.policial_repository_port import (
    PolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.prova_pericial_repository_port import (
    ProvaPericialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.public_security.application.ports.unidade_policial_repository_port import (
    UnidadePolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.vestigio_repository_port import (
    VestigioRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import (
    StatusAgente,
    StatusCadeiaCustodia,
    StatusEvidencia,
    StatusInvestigacao,
    StatusLaudo,
    StatusMandado,
    StatusOcorrencia,
    StatusProva,
    StatusUnidadePolicial,
    StatusVestigio,
    TipoAgente,
    TipoLaudo,
    TipoMandado,
    TipoOcorrencia,
    TipoProva,
)
from apps.backend.app.modules.public_security.domain.models.cadeia_custodia import CadeiaCustodia
from apps.backend.app.modules.public_security.domain.models.evidencia import Evidencia
from apps.backend.app.modules.public_security.domain.models.investigacao import Investigacao
from apps.backend.app.modules.public_security.domain.models.laudo_pericial import LaudoPericial
from apps.backend.app.modules.public_security.domain.models.mandado import Mandado
from apps.backend.app.modules.public_security.domain.models.ocorrencia import Ocorrencia
from apps.backend.app.modules.public_security.domain.models.policial import Policial
from apps.backend.app.modules.public_security.domain.models.prova_pericial import ProvaPericial
from apps.backend.app.modules.public_security.domain.models.unidade_policial import UnidadePolicial
from apps.backend.app.modules.public_security.domain.models.vestigio import Vestigio


class InMemoryUnidadePolicialRepository(UnidadePolicialRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, UnidadePolicial] = {}

    async def save(self, unidade: UnidadePolicial) -> UnidadePolicial:
        self._items[unidade.id] = unidade
        return unidade

    async def get_by_id(self, unidade_id: UUID) -> UnidadePolicial | None:
        return self._items.get(unidade_id)

    async def get_by_codigo(self, codigo_unidade: str) -> UnidadePolicial | None:
        normalized = codigo_unidade.strip()
        for item in self._items.values():
            if item.codigo_unidade == normalized:
                return item
        return None

    async def list_all(self) -> list[UnidadePolicial]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[UnidadePolicial]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusUnidadePolicial) -> list[UnidadePolicial]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.nome)

    async def delete(self, unidade_id: UUID) -> bool:
        return self._items.pop(unidade_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"UND/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_unidade.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryPolicialRepository(PolicialRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Policial] = {}

    async def save(self, policial: Policial) -> Policial:
        self._items[policial.id] = policial
        return policial

    async def get_by_id(self, policial_id: UUID) -> Policial | None:
        return self._items.get(policial_id)

    async def get_by_matricula(self, matricula: str) -> Policial | None:
        normalized = matricula.strip()
        for item in self._items.values():
            if item.matricula == normalized:
                return item
        return None

    async def get_by_cpf(self, cpf: str) -> Policial | None:
        normalized = cpf.strip()
        for item in self._items.values():
            if item.cpf == normalized:
                return item
        return None

    async def list_all(self) -> list[Policial]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_unidade(self, unidade_id: UUID) -> list[Policial]:
        items = [item for item in self._items.values() if item.unidade_id == unidade_id]
        return sorted(items, key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoAgente) -> list[Policial]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusAgente) -> list[Policial]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.nome)

    async def delete(self, policial_id: UUID) -> bool:
        return self._items.pop(policial_id, None) is not None

    async def next_matricula(self, unidade_id: UUID) -> str:
        year = date.today().year
        unidade_fragmento = str(unidade_id).split("-")[0].upper()
        prefix = f"POL/{unidade_fragmento}/{year}/"
        count = sum(1 for item in self._items.values() if item.matricula.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryOcorrenciaRepository(OcorrenciaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Ocorrencia] = {}

    async def save(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        self._items[ocorrencia.id] = ocorrencia
        return ocorrencia

    async def get_by_id(self, ocorrencia_id: UUID) -> Ocorrencia | None:
        return self._items.get(ocorrencia_id)

    async def get_by_codigo(self, codigo_ocorrencia: str) -> Ocorrencia | None:
        normalized = codigo_ocorrencia.strip()
        for item in self._items.values():
            if item.codigo_ocorrencia == normalized:
                return item
        return None

    async def list_all(self) -> list[Ocorrencia]:
        return sorted(self._items.values(), key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_unidade(self, unidade_id: UUID) -> list[Ocorrencia]:
        items = [item for item in self._items.values() if item.unidade_id == unidade_id]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_tipo(self, tipo: TipoOcorrencia) -> list[Ocorrencia]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_status(self, status: StatusOcorrencia) -> list[Ocorrencia]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[Ocorrencia]:
        items = [
            item
            for item in self._items.values()
            if item.data_ocorrencia >= inicio and item.data_ocorrencia <= fim
        ]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def delete(self, ocorrencia_id: UUID) -> bool:
        return self._items.pop(ocorrencia_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"OCO/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_ocorrencia.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryMandadoRepository(MandadoRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Mandado] = {}

    async def save(self, mandado: Mandado) -> Mandado:
        self._items[mandado.id] = mandado
        return mandado

    async def get_by_id(self, mandado_id: UUID) -> Mandado | None:
        return self._items.get(mandado_id)

    async def get_by_numero(self, numero_mandado: str) -> Mandado | None:
        normalized = numero_mandado.strip()
        for item in self._items.values():
            if item.numero_mandado == normalized:
                return item
        return None

    async def list_all(self) -> list[Mandado]:
        return sorted(self._items.values(), key=lambda item: item.data_expedicao, reverse=True)

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Mandado]:
        items = [item for item in self._items.values() if item.ocorrencia_id == ocorrencia_id]
        return sorted(items, key=lambda item: item.data_expedicao, reverse=True)

    async def list_by_tipo(self, tipo: TipoMandado) -> list[Mandado]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.data_expedicao, reverse=True)

    async def list_by_status(self, status: StatusMandado) -> list[Mandado]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_expedicao, reverse=True)

    async def delete(self, mandado_id: UUID) -> bool:
        return self._items.pop(mandado_id, None) is not None

    async def next_numero(self) -> str:
        year = date.today().year
        prefix = f"MD/{year}/"
        count = sum(1 for item in self._items.values() if item.numero_mandado.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryInvestigacaoRepository(InvestigacaoRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Investigacao] = {}

    async def save(self, investigacao: Investigacao) -> Investigacao:
        self._items[investigacao.id] = investigacao
        return investigacao

    async def get_by_id(self, investigacao_id: UUID) -> Investigacao | None:
        return self._items.get(investigacao_id)

    async def get_by_codigo(self, codigo_investigacao: str) -> Investigacao | None:
        normalized = codigo_investigacao.strip()
        for item in self._items.values():
            if item.codigo_investigacao == normalized:
                return item
        return None

    async def list_all(self) -> list[Investigacao]:
        return sorted(self._items.values(), key=lambda item: item.data_abertura, reverse=True)

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Investigacao]:
        items = [item for item in self._items.values() if item.ocorrencia_id == ocorrencia_id]
        return sorted(items, key=lambda item: item.data_abertura, reverse=True)

    async def list_by_status(self, status: StatusInvestigacao) -> list[Investigacao]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_abertura, reverse=True)

    async def delete(self, investigacao_id: UUID) -> bool:
        return self._items.pop(investigacao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"INV/{year}/"
        count = sum(
            1 for item in self._items.values() if item.codigo_investigacao.startswith(prefix)
        )
        return f"{prefix}{count + 1:06d}"


class InMemoryProvaPericialRepository(ProvaPericialRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, ProvaPericial] = {}

    async def save(self, prova: ProvaPericial) -> ProvaPericial:
        self._items[prova.id] = prova
        return prova

    async def get_by_id(self, prova_id: UUID) -> ProvaPericial | None:
        return self._items.get(prova_id)

    async def get_by_codigo(self, codigo_prova: str) -> ProvaPericial | None:
        normalized = codigo_prova.strip()
        for item in self._items.values():
            if item.codigo_prova == normalized:
                return item
        return None

    async def list_all(self) -> list[ProvaPericial]:
        return sorted(self._items.values(), key=lambda item: item.data_coleta, reverse=True)

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[ProvaPericial]:
        items = [item for item in self._items.values() if item.ocorrencia_id == ocorrencia_id]
        return sorted(items, key=lambda item: item.data_coleta, reverse=True)

    async def list_by_tipo(self, tipo: TipoProva) -> list[ProvaPericial]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.data_coleta, reverse=True)

    async def list_by_status(self, status: StatusProva) -> list[ProvaPericial]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_coleta, reverse=True)

    async def delete(self, prova_id: UUID) -> bool:
        return self._items.pop(prova_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"PRV/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_prova.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryCadeiaCustodiaRepository(CadeiaCustodiaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, CadeiaCustodia] = {}

    async def save(self, cadeia: CadeiaCustodia) -> CadeiaCustodia:
        self._items[cadeia.id] = cadeia
        return cadeia

    async def get_by_id(self, cadeia_id: UUID) -> CadeiaCustodia | None:
        return self._items.get(cadeia_id)

    async def get_by_codigo(self, codigo_cadeia: str) -> CadeiaCustodia | None:
        normalized = codigo_cadeia.strip()
        for item in self._items.values():
            if item.codigo_cadeia == normalized:
                return item
        return None

    async def get_by_prova(self, prova_id: UUID) -> CadeiaCustodia | None:
        for item in self._items.values():
            if item.prova_id == prova_id:
                return item
        return None

    async def list_all(self) -> list[CadeiaCustodia]:
        return sorted(self._items.values(), key=lambda item: item.data_inicio, reverse=True)

    async def list_by_status(self, status: StatusCadeiaCustodia) -> list[CadeiaCustodia]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_inicio, reverse=True)

    async def delete(self, cadeia_id: UUID) -> bool:
        return self._items.pop(cadeia_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"CCD/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_cadeia.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryLaudoPericialRepository(LaudoPericialRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, LaudoPericial] = {}

    async def save(self, laudo: LaudoPericial) -> LaudoPericial:
        self._items[laudo.id] = laudo
        return laudo

    async def get_by_id(self, laudo_id: UUID) -> LaudoPericial | None:
        return self._items.get(laudo_id)

    async def get_by_numero(self, numero_laudo: str) -> LaudoPericial | None:
        normalized = numero_laudo.strip()
        for item in self._items.values():
            if item.numero_laudo == normalized:
                return item
        return None

    async def list_all(self) -> list[LaudoPericial]:
        return sorted(self._items.values(), key=lambda item: item.data_emissao, reverse=True)

    async def list_by_prova(self, prova_id: UUID) -> list[LaudoPericial]:
        items = [item for item in self._items.values() if item.prova_id == prova_id]
        return sorted(items, key=lambda item: item.data_emissao, reverse=True)

    async def list_by_tipo(self, tipo: TipoLaudo) -> list[LaudoPericial]:
        items = [item for item in self._items.values() if item.tipo_laudo == tipo]
        return sorted(items, key=lambda item: item.data_emissao, reverse=True)

    async def list_by_status(self, status: StatusLaudo) -> list[LaudoPericial]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_emissao, reverse=True)

    async def delete(self, laudo_id: UUID) -> bool:
        return self._items.pop(laudo_id, None) is not None

    async def next_numero(self) -> str:
        year = date.today().year
        prefix = f"LDP/{year}/"
        count = sum(1 for item in self._items.values() if item.numero_laudo.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryVestigioRepository(VestigioRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Vestigio] = {}

    async def save(self, vestigio: Vestigio) -> Vestigio:
        self._items[vestigio.id] = vestigio
        return vestigio

    async def get_by_id(self, vestigio_id: UUID) -> Vestigio | None:
        return self._items.get(vestigio_id)

    async def get_by_codigo(self, codigo_vestigio: str) -> Vestigio | None:
        normalized = codigo_vestigio.strip()
        for item in self._items.values():
            if item.codigo_vestigio == normalized:
                return item
        return None

    async def list_all(self) -> list[Vestigio]:
        return sorted(self._items.values(), key=lambda item: item.data_coleta, reverse=True)

    async def list_by_cadeia(self, cadeia_custodia_id: UUID) -> list[Vestigio]:
        items = [
            item for item in self._items.values() if item.cadeia_custodia_id == cadeia_custodia_id
        ]
        return sorted(items, key=lambda item: item.data_coleta, reverse=True)

    async def list_by_status(self, status: StatusVestigio) -> list[Vestigio]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_coleta, reverse=True)

    async def delete(self, vestigio_id: UUID) -> bool:
        return self._items.pop(vestigio_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"VST/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_vestigio.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class InMemoryEvidenciaRepository(EvidenciaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Evidencia] = {}

    async def save(self, evidencia: Evidencia) -> Evidencia:
        self._items[evidencia.id] = evidencia
        return evidencia

    async def get_by_id(self, evidencia_id: UUID) -> Evidencia | None:
        return self._items.get(evidencia_id)

    async def get_by_codigo(self, codigo_evidencia: str) -> Evidencia | None:
        normalized = codigo_evidencia.strip()
        for item in self._items.values():
            if item.codigo_evidencia == normalized:
                return item
        return None

    async def list_all(self) -> list[Evidencia]:
        return sorted(self._items.values(), key=lambda item: item.data_registro, reverse=True)

    async def list_by_vestigio(self, vestigio_id: UUID) -> list[Evidencia]:
        items = [item for item in self._items.values() if item.vestigio_id == vestigio_id]
        return sorted(items, key=lambda item: item.data_registro, reverse=True)

    async def list_by_status(self, status: StatusEvidencia) -> list[Evidencia]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_registro, reverse=True)

    async def delete(self, evidencia_id: UUID) -> bool:
        return self._items.pop(evidencia_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"EVD/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_evidencia.startswith(prefix))
        return f"{prefix}{count + 1:06d}"


class FakeRequestService(RequestServicePort):
    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        metadata: dict[str, Any] | None = None,
        citizen_id: UUID | None = None,
        numero_processo: str | None = None,
    ) -> UUID | None:
        return None
