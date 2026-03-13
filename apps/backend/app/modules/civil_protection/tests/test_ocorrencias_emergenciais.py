from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
import pytest
from apps.backend.app.modules.civil_protection.application.services.bombeiro_service import BombeiroService
from apps.backend.app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from apps.backend.app.modules.civil_protection.application.services.ocorrencia_emergencial_service import OcorrenciaEmergencialService
from apps.backend.app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.tests._fakes import InMemoryBombeiroRepository, InMemoryCorporacaoRepository, InMemoryOcorrenciaEmergencialRepository

def test_registrar_ocorrencia_emergencial_sucesso() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
        ocorrencia_service = OcorrenciaEmergencialService(ocorrencia_repo=ocorrencia_repo, corporacao_repo=corporacao_repo, bombeiro_repo=bombeiro_repo)
        corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo de Bombeiros Leste', municipio='Luanda', provincia='Luanda', endereco='Rua Leste', comandante='Comandante Leste')
        bombeiro = await bombeiro_service.cadastrar_bombeiro(corporacao_id=corporacao.id, nome='Rui Pereira', data_nascimento=date.today() - timedelta(days=365 * 34), cpf='111.222.333-44', rg='RG111222')
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(corporacao_id=corporacao.id, bombeiro_responsavel_id=bombeiro.id, tipo=TipoOcorrenciaEmergencial.INUNDACAO, prioridade=PrioridadeAtendimento.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=2), descricao='Inundacao em area residencial com risco de isolamento', municipio='Luanda', provincia='Luanda', vitimas=2, desalojados=8)
        assert ocorrencia.codigo_ocorrencia.startswith('OCE/')
        assert ocorrencia.status == StatusOcorrenciaEmergencial.RECEBIDA
    asyncio.run(scenario())

def test_registrar_ocorrencia_falha_bombeiro_outra_corporacao() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
        ocorrencia_service = OcorrenciaEmergencialService(ocorrencia_repo=ocorrencia_repo, corporacao_repo=corporacao_repo, bombeiro_repo=bombeiro_repo)
        corp_a = await corporacao_service.cadastrar_corporacao(nome='Corpo A', municipio='Luanda', provincia='Luanda', endereco='Rua A', comandante='Comandante A')
        corp_b = await corporacao_service.cadastrar_corporacao(nome='Corpo B', municipio='Luanda', provincia='Luanda', endereco='Rua B', comandante='Comandante B')
        bombeiro_b = await bombeiro_service.cadastrar_bombeiro(corporacao_id=corp_b.id, nome='Paulo B', data_nascimento=date.today() - timedelta(days=365 * 32), cpf='555.666.777-88', rg='RG667788')
        with pytest.raises(ValueError, match='nao pertence'):
            await ocorrencia_service.registrar_ocorrencia(corporacao_id=corp_a.id, bombeiro_responsavel_id=bombeiro_b.id, tipo=TipoOcorrenciaEmergencial.DESABAMENTO, prioridade=PrioridadeAtendimento.MEDIA, data_ocorrencia=datetime.now() - timedelta(hours=1), descricao='Desabamento parcial em mercado municipal', municipio='Luanda', provincia='Luanda')
    asyncio.run(scenario())

def test_atualizar_status_ocorrencia_emergencial() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        ocorrencia_service = OcorrenciaEmergencialService(ocorrencia_repo=ocorrencia_repo, corporacao_repo=corporacao_repo, bombeiro_repo=bombeiro_repo)
        corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo C', municipio='Bengo', provincia='Bengo', endereco='Rua C', comandante='Comandante C')
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(corporacao_id=corporacao.id, tipo=TipoOcorrenciaEmergencial.INCENDIO_URBANO, prioridade=PrioridadeAtendimento.MEDIA, data_ocorrencia=datetime.now() - timedelta(days=1), descricao='Incendio urbano controlado sem vitimas graves', municipio='Bengo', provincia='Bengo')
        atualizada = await ocorrencia_service.atualizar_status(ocorrencia_id=ocorrencia.id, status=StatusOcorrenciaEmergencial.EM_ATENDIMENTO, observacoes='Equipe em campo')
        assert atualizada.status == StatusOcorrenciaEmergencial.EM_ATENDIMENTO
        assert atualizada.ativo is True
    asyncio.run(scenario())