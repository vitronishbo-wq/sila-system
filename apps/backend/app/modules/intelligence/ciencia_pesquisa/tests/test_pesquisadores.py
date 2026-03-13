from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.pesquisador_service import PesquisadorService
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NivelFormacao, StatusVinculoPesquisador, TipoVinculoPesquisador
from apps.backend.app.modules.intelligence.ciencia_pesquisa.tests._fakes import InMemoryInstituicaoPesquisaRepository, InMemoryPesquisadorRepository

def test_cadastrar_pesquisador_sucesso() -> None:

    async def scenario() -> None:
        service = PesquisadorService(pesquisador_repo=InMemoryPesquisadorRepository(), instituicao_repo=InMemoryInstituicaoPesquisaRepository())
        saved = await service.cadastrar_pesquisador(nome_completo='Helena Campos', documento_identificacao='BI998877', email_institucional='helena.campos@pesquisa.ao', area_conhecimento=AreaConhecimento.ENGENHARIAS, nivel_formacao=NivelFormacao.MESTRE, tipo_vinculo=TipoVinculoPesquisador.BOLSISTA)
        assert saved.nome_completo == 'Helena Campos'
        assert saved.status_vinculo == StatusVinculoPesquisador.ATIVO
    asyncio.run(scenario())

def test_cadastrar_pesquisador_duplicado_documento() -> None:

    async def scenario() -> None:
        repo = InMemoryPesquisadorRepository()
        service = PesquisadorService(pesquisador_repo=repo, instituicao_repo=InMemoryInstituicaoPesquisaRepository())
        payload = dict(nome_completo='Carlos Neto', documento_identificacao='BI123123', email_institucional='carlos.neto@pesquisa.ao')
        await service.cadastrar_pesquisador(**payload)
        with pytest.raises(ValueError, match='documento'):
            await service.cadastrar_pesquisador(nome_completo='Carlos Neto Junior', documento_identificacao='BI123123', email_institucional='carlos.jr@pesquisa.ao')
    asyncio.run(scenario())

def test_vincular_e_encerrar_vinculo() -> None:

    async def scenario() -> None:
        instituicao_repo = InMemoryInstituicaoPesquisaRepository()
        pesquisador_repo = InMemoryPesquisadorRepository()
        service = PesquisadorService(pesquisador_repo=pesquisador_repo, instituicao_repo=instituicao_repo)
        from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import NaturezaJuridicaInstituicao, TipoInstituicaoPesquisa
        from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import InstituicaoPesquisa
        instituicao = InstituicaoPesquisa.cadastrar(sigla='INCT', nome='Instituto Nacional de Ciencia e Tecnologia', nif='500000002', tipo=TipoInstituicaoPesquisa.CENTRO_PESQUISA, natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA, pais='Angola', provincia='Luanda', municipio='Belas', endereco='Av. da Tecnologia, 200', email_institucional='contato@inct.ao')
        instituicao = await instituicao_repo.save(instituicao)
        pesquisador = await service.cadastrar_pesquisador(nome_completo='Marta Soares', documento_identificacao='BI889900', email_institucional='marta.soares@inct.ao')
        unidade_id = uuid4()
        vinculado = await service.vincular_instituicao(pesquisador_id=pesquisador.id, instituicao_id=instituicao.id, unidade_pesquisa_id=unidade_id)
        assert vinculado.instituicao_id == instituicao.id
        assert vinculado.unidade_pesquisa_id == unidade_id
        encerrado = await service.encerrar_vinculo(pesquisador_id=pesquisador.id, data_fim_vinculo=date(2026, 3, 2))
        assert encerrado.status_vinculo == StatusVinculoPesquisador.ENCERRADO
        assert encerrado.ativo is False
    asyncio.run(scenario())