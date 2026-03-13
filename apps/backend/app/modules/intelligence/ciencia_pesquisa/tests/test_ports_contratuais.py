from __future__ import annotations
import asyncio
from uuid import uuid4
from app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NaturezaJuridicaInstituicao, NivelFormacao, TipoInstituicaoPesquisa, TipoVinculoPesquisador
from app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import InstituicaoPesquisa
from app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import Pesquisador
from app.modules.intelligence.ciencia_pesquisa.domain.models.projeto_pesquisa import ProjetoPesquisa
from app.modules.intelligence.ciencia_pesquisa.tests._fakes import InMemoryInstituicaoPesquisaRepository, InMemoryPesquisadorRepository, InMemoryProjetoPesquisaRepository

def test_contract_pesquisador_repository_crud_e_vinculacao() -> None:

    async def scenario() -> None:
        repo = InMemoryPesquisadorRepository()
        pesquisador = Pesquisador.cadastrar(nome_completo='Ana Paula Silva', documento_identificacao='BI123456', email_institucional='ana.silva@inst.ao', area_conhecimento=AreaConhecimento.CIENCIAS_SAUDE, nivel_formacao=NivelFormacao.DOUTOR, tipo_vinculo=TipoVinculoPesquisador.EFETIVO)
        saved = await repo.save(pesquisador)
        by_id = await repo.get_by_id(saved.id)
        by_doc = await repo.get_by_documento('BI123456')
        by_email = await repo.get_by_email('ana.silva@inst.ao')
        assert by_id is not None
        assert by_doc is not None
        assert by_email is not None
        instituicao_id = uuid4()
        vinculado = await repo.vincular_instituicao(pesquisador_id=saved.id, instituicao_id=instituicao_id, unidade_pesquisa_id=None)
        assert vinculado is not None
        assert vinculado.instituicao_id == instituicao_id
        vinculados = await repo.list_by_instituicao(instituicao_id)
        assert len(vinculados) == 1
        all_items = await repo.list_all()
        assert len(all_items) == 1
        deleted = await repo.delete(saved.id)
        assert deleted is True
        assert await repo.get_by_id(saved.id) is None
    asyncio.run(scenario())

def test_contract_instituicao_repository_crud() -> None:

    async def scenario() -> None:
        repo = InMemoryInstituicaoPesquisaRepository()
        instituicao = InstituicaoPesquisa.cadastrar(sigla='INIS', nome='Instituto Nacional de Investigacao em Saude', nif='500000001', tipo=TipoInstituicaoPesquisa.INSTITUTO, natureza_juridica=NaturezaJuridicaInstituicao.PUBLICA, pais='Angola', provincia='Luanda', municipio='Luanda', endereco='Rua da Ciencia, 10', email_institucional='contato@inis.ao')
        saved = await repo.save(instituicao)
        by_id = await repo.get_by_id(saved.id)
        by_sigla = await repo.get_by_sigla('inis')
        by_nif = await repo.get_by_nif('500000001')
        assert by_id is not None
        assert by_sigla is not None
        assert by_nif is not None
        all_items = await repo.list_all()
        ativas = await repo.list_ativas()
        assert len(all_items) == 1
        assert len(ativas) == 1
        deleted = await repo.delete(saved.id)
        assert deleted is True
        assert await repo.get_by_id(saved.id) is None
    asyncio.run(scenario())

def test_contract_projeto_repository_crud_e_vinculacao() -> None:

    async def scenario() -> None:
        repo = InMemoryProjetoPesquisaRepository()
        instituicao_id = uuid4()
        coordenador_id = uuid4()
        projeto = ProjetoPesquisa.cadastrar(codigo_projeto=await repo.next_codigo(), titulo='Projeto de Vigilancia Epidemiologica', resumo='Projeto para ampliar a capacidade de pesquisa epidemiologica.', instituicao_id=instituicao_id, coordenador_id=coordenador_id, equipe_pesquisadores_ids=[], area_conhecimento=AreaConhecimento.CIENCIAS_SAUDE)
        saved = await repo.save(projeto)
        by_id = await repo.get_by_id(saved.id)
        by_codigo = await repo.get_by_codigo(saved.codigo_projeto)
        assert by_id is not None
        assert by_codigo is not None
        pesquisador_extra = uuid4()
        atualizado = await repo.vincular_pesquisadores(projeto_id=saved.id, pesquisador_ids=[pesquisador_extra])
        assert atualizado is not None
        assert pesquisador_extra in atualizado.equipe_pesquisadores_ids
        by_instituicao = await repo.list_by_instituicao(instituicao_id)
        by_pesquisador = await repo.list_by_pesquisador(coordenador_id)
        assert len(by_instituicao) == 1
        assert len(by_pesquisador) == 1
        deleted = await repo.delete(saved.id)
        assert deleted is True
        assert await repo.get_by_id(saved.id) is None
    asyncio.run(scenario())