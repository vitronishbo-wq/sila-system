from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    AtendimentoRepositoryPort,
    BeneficiarioRepositoryPort,
    BeneficioRepositoryPort,
    CadastroUnicoRepositoryPort,
    CitizenServicePort,
    CriancaRiscoRepositoryPort,
    EducacaoServicePort,
    EmpregoServicePort,
    IdosoVulneravelRepositoryPort,
    JuventudeServicePort,
    PCDRepositoryPort,
    ProgramaSocialRepositoryPort,
    RequestServicePort,
    SaudeServicePort,
    SituacaoRuaRepositoryPort,
    VisitaDomiciliarRepositoryPort,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import (
    Atendimento,
    Beneficiario,
    Beneficio,
    CadastroUnico,
    CriancaRisco,
    IdosoVulneravel,
    PessoaComDeficiencia,
    ProgramaSocial,
    SituacaoRua,
    VisitaDomiciliar,
)


class _BaseInMemoryRepo:
    def __init__(self) -> None:
        self._items: dict[UUID, object] = {}

    async def delete(self, entity_id: UUID) -> bool:
        return self._items.pop(entity_id, None) is not None


class InMemoryBeneficiarioRepo(_BaseInMemoryRepo, BeneficiarioRepositoryPort):
    async def save(self, entity: Beneficiario) -> Beneficiario:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> Beneficiario | None:
        return self._items.get(entity_id)

    async def get_by_citizen(self, citizen_id: UUID) -> Beneficiario | None:
        for item in self._items.values():
            if item.citizen_id == citizen_id:
                return item
        return None

    async def list_all(self) -> list[Beneficiario]:
        return list(self._items.values())


class InMemoryCadastroUnicoRepo(_BaseInMemoryRepo, CadastroUnicoRepositoryPort):
    async def save(self, entity: CadastroUnico) -> CadastroUnico:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> CadastroUnico | None:
        return self._items.get(entity_id)

    async def get_by_citizen(self, citizen_id: UUID) -> CadastroUnico | None:
        for item in self._items.values():
            if item.citizen_id_responsavel == citizen_id:
                return item
        return None

    async def list_all(self) -> list[CadastroUnico]:
        return list(self._items.values())


class InMemoryProgramaRepo(_BaseInMemoryRepo, ProgramaSocialRepositoryPort):
    async def save(self, entity: ProgramaSocial) -> ProgramaSocial:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> ProgramaSocial | None:
        return self._items.get(entity_id)

    async def get_by_codigo(self, codigo: str) -> ProgramaSocial | None:
        for item in self._items.values():
            if item.codigo == codigo:
                return item
        return None

    async def list_all(self) -> list[ProgramaSocial]:
        return list(self._items.values())


class InMemoryBeneficioRepo(_BaseInMemoryRepo, BeneficioRepositoryPort):
    async def save(self, entity: Beneficio) -> Beneficio:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> Beneficio | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[Beneficio]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[Beneficio]:
        return list(self._items.values())


class InMemoryPCDRepo(_BaseInMemoryRepo, PCDRepositoryPort):
    async def save(self, entity: PessoaComDeficiencia) -> PessoaComDeficiencia:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> PessoaComDeficiencia | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[PessoaComDeficiencia]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[PessoaComDeficiencia]:
        return list(self._items.values())


class InMemoryAtendimentoRepo(_BaseInMemoryRepo, AtendimentoRepositoryPort):
    async def save(self, entity: Atendimento) -> Atendimento:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> Atendimento | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[Atendimento]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[Atendimento]:
        return list(self._items.values())


class InMemoryVisitaRepo(_BaseInMemoryRepo, VisitaDomiciliarRepositoryPort):
    async def save(self, entity: VisitaDomiciliar) -> VisitaDomiciliar:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> VisitaDomiciliar | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[VisitaDomiciliar]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[VisitaDomiciliar]:
        return list(self._items.values())


class InMemorySituacaoRuaRepo(_BaseInMemoryRepo, SituacaoRuaRepositoryPort):
    async def save(self, entity: SituacaoRua) -> SituacaoRua:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> SituacaoRua | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[SituacaoRua]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[SituacaoRua]:
        return list(self._items.values())


class InMemoryCriancaRiscoRepo(_BaseInMemoryRepo, CriancaRiscoRepositoryPort):
    async def save(self, entity: CriancaRisco) -> CriancaRisco:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> CriancaRisco | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[CriancaRisco]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[CriancaRisco]:
        return list(self._items.values())


class InMemoryIdosoRepo(_BaseInMemoryRepo, IdosoVulneravelRepositoryPort):
    async def save(self, entity: IdosoVulneravel) -> IdosoVulneravel:
        self._items[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> IdosoVulneravel | None:
        return self._items.get(entity_id)

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[IdosoVulneravel]:
        return [item for item in self._items.values() if item.beneficiario_id == beneficiario_id]

    async def list_all(self) -> list[IdosoVulneravel]:
        return list(self._items.values())


class FakeCitizenService(CitizenServicePort):
    def __init__(self, *, active: bool = True):
        self.active = active

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        _ = citizen_id
        return self.active


class FakeEducacaoService(EducacaoServicePort):
    def __init__(self, estudantes_ativos: set[UUID] | None = None):
        self.estudantes_ativos = estudantes_ativos or set()

    async def is_estudante_ativo(self, citizen_id: UUID) -> bool:
        return citizen_id in self.estudantes_ativos


class FakeJuventudeService(JuventudeServicePort):
    def __init__(self, jovens_em_risco: set[UUID] | None = None):
        self.jovens_em_risco = jovens_em_risco or set()

    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        return citizen_id in self.jovens_em_risco


class FakeSaudeService(SaudeServicePort):
    def __init__(self, laudos_invalidos: set[UUID] | None = None, cobertura: bool = True):
        self.laudos_invalidos = laudos_invalidos or set()
        self.cobertura = cobertura

    async def validar_laudo_pcd(self, *, citizen_id: UUID, laudo_id: UUID, cid: str) -> bool:
        return bool(citizen_id and cid) and laudo_id not in self.laudos_invalidos

    async def verificar_cobertura_idoso(self, *, citizen_id: UUID) -> bool:
        _ = citizen_id
        return self.cobertura


class FakeEmpregoService(EmpregoServicePort):
    def __init__(self, previdenciarios: set[UUID] | None = None):
        self.previdenciarios = previdenciarios or set()

    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        _ = citizen_id
        return False

    async def has_beneficio_previdenciario(self, citizen_id: UUID) -> bool:
        return citizen_id in self.previdenciarios


class FakeRequestService(RequestServicePort):
    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        citizen_id: UUID,
        numero_processo: str,
        metadata: dict | None = None,
    ):
        self.calls.append(
            {
                "request_type": request_type,
                "entity_id": entity_id,
                "citizen_id": citizen_id,
                "numero_processo": numero_processo,
                "metadata": metadata or {},
            }
        )
        return None
