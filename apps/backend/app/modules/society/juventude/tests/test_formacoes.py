from __future__ import annotations
import asyncio
from datetime import date, timedelta
from uuid import uuid4
import pytest
from app.modules.society.juventude.application.services.formacao_service import FormacaoService
from app.modules.society.juventude.application.services.jovem_service import JovemService
from app.modules.society.juventude.application.services.programa_service import ProgramaService
from app.modules.society.juventude.domain.enums import Escolaridade, SituacaoOcupacional, StatusFormacao, TipoPrograma
from app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, InMemoryFormacaoRepository, InMemoryJovemRepository, InMemoryProgramaRepository

def test_registrar_formacao_sucesso() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        programa_repo = InMemoryProgramaRepository()
        formacao_repo = InMemoryFormacaoRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        programa_service = ProgramaService(programa_repo=programa_repo)
        formacao_service = FormacaoService(formacao_repo=formacao_repo, jovem_repo=jovem_repo, programa_repo=programa_repo)
        jovem = await jovem_service.cadastrar_jovem(nome='Joana Formacao', data_nascimento=date.today() - timedelta(days=365 * 20), genero='F', naturalidade='Luanda', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua F', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        programa = await programa_service.criar_programa(nome='Programa Capacitacao Digital', tipo=TipoPrograma.CAPACITACAO, data_inicio=date.today(), vagas=80)
        formacao = await formacao_service.registrar_formacao(jovem_id=jovem.id, programa_id=programa.id, nome_curso='Tecnologias Web', instituicao='Centro Juvenil Digital', carga_horaria=120, data_inicio=date.today())
        assert formacao.codigo_formacao.startswith('FRM/')
        assert formacao.status == StatusFormacao.INSCRITO
    asyncio.run(scenario())

def test_registrar_formacao_falha_sem_jovem() -> None:

    async def scenario() -> None:
        service = FormacaoService(formacao_repo=InMemoryFormacaoRepository(), jovem_repo=InMemoryJovemRepository(), programa_repo=InMemoryProgramaRepository())
        with pytest.raises(ValueError, match='Jovem'):
            await service.registrar_formacao(jovem_id=uuid4(), nome_curso='Curso Teste', instituicao='Instituto Teste', carga_horaria=40, data_inicio=date.today())
    asyncio.run(scenario())

def test_atualizar_status_formacao() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        programa_repo = InMemoryProgramaRepository()
        formacao_repo = InMemoryFormacaoRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        formacao_service = FormacaoService(formacao_repo=formacao_repo, jovem_repo=jovem_repo, programa_repo=programa_repo)
        jovem = await jovem_service.cadastrar_jovem(nome='Carlos Formacao', data_nascimento=date.today() - timedelta(days=365 * 23), genero='M', naturalidade='Benguela', escolaridade=Escolaridade.SUPERIOR_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO, endereco='Rua G', municipio='Benguela', provincia='Benguela', citizen_id=uuid4())
        formacao = await formacao_service.registrar_formacao(jovem_id=jovem.id, nome_curso='Gestao de Projetos', instituicao='Academia Jovem', carga_horaria=60, data_inicio=date.today())
        atualizada = await formacao_service.atualizar_status(formacao_id=formacao.id, status=StatusFormacao.CONCLUIDA, certificado_emitido=True)
        assert atualizada.status == StatusFormacao.CONCLUIDA
        assert atualizada.certificado_emitido is True
    asyncio.run(scenario())