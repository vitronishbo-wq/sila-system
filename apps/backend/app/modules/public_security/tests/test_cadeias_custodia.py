from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
import pytest
from apps.backend.app.modules.public_security.application.services.cadeia_custodia_service import CadeiaCustodiaService
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import ProvaPericialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusCadeiaCustodia, TipoAgente, TipoOcorrencia, TipoProva, TipoUnidadePolicial, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryCadeiaCustodiaRepository, InMemoryOcorrenciaRepository, InMemoryPolicialRepository, InMemoryProvaPericialRepository, InMemoryUnidadePolicialRepository

def test_iniciar_cadeia_custodia_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Base Custodia Central', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Luanda', provincia='Luanda', endereco='Zona Industrial', comandante='Comandante Base')
        perito = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Perito Matias', data_nascimento=date.today() - timedelta(days=365 * 35), cpf='777.111.222-33', rg='RG771122', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=perito.id, tipo=TipoOcorrencia.TRAFICO, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=2), descricao='Apreensao de material para pericia', municipio='Luanda', provincia='Luanda')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.MATERIAL, descricao='Material embalado para custodia', local_coleta='Armazem principal', coletado_por_id=perito.id)
        cadeia = await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Cofre central', responsavel_id=perito.id)
        assert cadeia.codigo_cadeia.startswith('CCD/')
        assert cadeia.status == StatusCadeiaCustodia.INICIADA
    asyncio.run(scenario())

def test_iniciar_cadeia_custodia_falha_duplicidade_prova() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Base Custodia Norte', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Bengo', provincia='Bengo', endereco='Zona Norte', comandante='Comandante Norte')
        responsavel = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Agente Custodia', data_nascimento=date.today() - timedelta(days=365 * 32), cpf='555.444.333-22', rg='RG554433', tipo=TipoAgente.POLICIAL, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, tipo=TipoOcorrencia.FURTO, prioridade=PrioridadeOcorrencia.MEDIA, data_ocorrencia=datetime.now() - timedelta(days=1), descricao='Material apreendido para analise', municipio='Bengo', provincia='Bengo')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DOCUMENTAL, descricao='Documentacao sensivel', local_coleta='Arquivo local')
        await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Deposito A', responsavel_id=responsavel.id)
        with pytest.raises(ValueError, match='Ja existe cadeia de custodia'):
            await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Deposito B', responsavel_id=responsavel.id)
    asyncio.run(scenario())

def test_registrar_movimentacao_cadeia_custodia() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Base Custodia Sul', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Luanda', provincia='Luanda', endereco='Zona Sul', comandante='Comandante Sul')
        responsavel = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Operador Custodia', data_nascimento=date.today() - timedelta(days=365 * 31), cpf='888.777.666-55', rg='RG887766', tipo=TipoAgente.POLICIAL, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=responsavel.id, tipo=TipoOcorrencia.DANO, prioridade=PrioridadeOcorrencia.BAIXA, data_ocorrencia=datetime.now() - timedelta(hours=8), descricao='Dano em equipamento publico', municipio='Luanda', provincia='Luanda')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DIGITAL, descricao='Imagem digital do equipamento danificado', local_coleta='Centro de monitoramento', coletado_por_id=responsavel.id)
        cadeia = await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Sala 01', responsavel_id=responsavel.id)
        atualizada = await cadeia_service.registrar_movimentacao(cadeia_id=cadeia.id, status=StatusCadeiaCustodia.EM_TRANSITO, local_atual='Laboratorio forense', responsavel_id=responsavel.id, observacao='Transferencia para analise')
        assert atualizada.status == StatusCadeiaCustodia.EM_TRANSITO
        assert len(atualizada.historico_movimentacoes) == 2
    asyncio.run(scenario())