from __future__ import annotations
import asyncio
from datetime import date, timedelta
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.application.services.jovem_service import JovemService
from apps.backend.app.modules.society.juventude.application.services.risco_evasao_service import RiscoEvasaoService
from apps.backend.app.modules.society.juventude.domain.enums import Escolaridade, RiscoSocial, SituacaoOcupacional, TipoVulnerabilidade
from apps.backend.app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, FakeRequestService, InMemoryJovemRepository, InMemoryRiscoEvasaoRepository

class _RequestRecorder(FakeRequestService):

    def __init__(self) -> None:
        self.requests: list[tuple[str, UUID]] = []

    async def create_request(self, *, request_type: str, entity_id: UUID, metadata: dict | None=None, citizen_id: UUID | None=None, numero_processo: str | None=None):
        self.requests.append((request_type, entity_id))
        return None

def test_avaliar_risco_critico_sem_matricula_ativa() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        recorder = _RequestRecorder()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=False), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        risco_service = RiscoEvasaoService(risco_repo=InMemoryRiscoEvasaoRepository(), jovem_repo=jovem_repo, educacao_service=FakeEducacaoService(matricula_ativa=False), request_service=recorder)
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Alto Risco', data_nascimento=date.today() - timedelta(days=365 * 19), genero='F', naturalidade='Luanda', escolaridade=Escolaridade.MEDIO_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.NAO_ESTUDA_NAO_TRABALHA, endereco='Rua Risco', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        await jovem_service.adicionar_vulnerabilidade(jovem_id=jovem.id, vulnerabilidade=TipoVulnerabilidade.BAIXA_RENDA)
        await jovem_service.adicionar_vulnerabilidade(jovem_id=jovem.id, vulnerabilidade=TipoVulnerabilidade.SITUACAO_RUA)
        risco = await risco_service.avaliar_risco(jovem_id=jovem.id)
        assert risco.nivel_risco == RiscoSocial.CRITICO
        assert risco.pontuacao >= 75
        assert recorder.requests
    asyncio.run(scenario())

def test_avaliar_risco_baixo_com_matricula_ativa() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        risco_service = RiscoEvasaoService(risco_repo=InMemoryRiscoEvasaoRepository(), jovem_repo=jovem_repo, educacao_service=FakeEducacaoService(matricula_ativa=True), request_service=FakeRequestService())
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Baixo Risco', data_nascimento=date.today() - timedelta(days=365 * 17), genero='M', naturalidade='Benguela', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua Escola', municipio='Benguela', provincia='Benguela', citizen_id=uuid4())
        risco = await risco_service.avaliar_risco(jovem_id=jovem.id)
        assert risco.matricula_ativa is True
        assert risco.nivel_risco == RiscoSocial.BAIXO
        assert risco.pontuacao < 25
    asyncio.run(scenario())

def test_buscar_risco_ativo_por_jovem() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        risco_repo = InMemoryRiscoEvasaoRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=False), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        risco_service = RiscoEvasaoService(risco_repo=risco_repo, jovem_repo=jovem_repo, educacao_service=FakeEducacaoService(matricula_ativa=False))
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Consulta Risco', data_nascimento=date.today() - timedelta(days=365 * 20), genero='F', naturalidade='Huambo', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO, endereco='Rua Consulta', municipio='Huambo', provincia='Huambo', citizen_id=uuid4())
        created = await risco_service.avaliar_risco(jovem_id=jovem.id)
        found = await risco_service.buscar_risco_ativo_por_jovem(jovem.id)
        assert found.id == created.id
    asyncio.run(scenario())