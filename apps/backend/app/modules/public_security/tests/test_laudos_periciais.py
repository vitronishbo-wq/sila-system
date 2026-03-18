from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4
import pytest
from apps.backend.app.modules.public_security.application.services.laudo_pericial_service import LaudoPericialService
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import ProvaPericialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusLaudo, StatusProva, TipoAgente, TipoLaudo, TipoOcorrencia, TipoProva, TipoUnidadePolicial, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryLaudoPericialRepository, InMemoryOcorrenciaRepository, InMemoryPolicialRepository, InMemoryProvaPericialRepository, InMemoryUnidadePolicialRepository

def test_emitir_laudo_pericial_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        laudo_repo = InMemoryLaudoPericialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        laudo_service = LaudoPericialService(laudo_repo=laudo_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Instituto Pericial', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua Forense', comandante='Diretor Forense')
        perito = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Perito Almeida', data_nascimento=date.today() - timedelta(days=365 * 38), cpf='222.777.999-00', rg='RG227799', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=perito.id, tipo=TipoOcorrencia.CORRUPCAO, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(days=1), descricao='Apreensao de dispositivo para analise digital', municipio='Luanda', provincia='Luanda')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DIGITAL, descricao='Notebook apreendido no local', local_coleta='Laboratorio digital', coletado_por_id=perito.id)
        laudo = await laudo_service.emitir_laudo(prova_id=prova.id, tipo_laudo=TipoLaudo.INFORMATICA, perito_id=perito.id, conclusao='Foram encontrados artefatos digitais compatíveis com a investigacao.')
        prova_atualizada = await prova_service.buscar_prova(prova.id)
        assert laudo.numero_laudo.startswith('LDP/')
        assert laudo.status == StatusLaudo.EMITIDO
        assert prova_atualizada.status == StatusProva.VALIDADA
    asyncio.run(scenario())

def test_emitir_laudo_pericial_falha_prova_inexistente() -> None:

    async def scenario() -> None:
        service = LaudoPericialService(laudo_repo=InMemoryLaudoPericialRepository(), prova_repo=InMemoryProvaPericialRepository(), policial_repo=InMemoryPolicialRepository())
        with pytest.raises(ValueError, match='Prova pericial nao encontrada'):
            await service.emitir_laudo(prova_id=uuid4(), tipo_laudo=TipoLaudo.BALISTICO, perito_id=uuid4(), conclusao='Laudo sem prova deve falhar por regra de dominio.')
    asyncio.run(scenario())

def test_atualizar_status_laudo_pericial() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        laudo_repo = InMemoryLaudoPericialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        laudo_service = LaudoPericialService(laudo_repo=laudo_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Laboratorio Balistico', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Bengo', provincia='Bengo', endereco='Rua Balistica', comandante='Chefe Balistico')
        perito = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Perito Balistico', data_nascimento=date.today() - timedelta(days=365 * 39), cpf='444.555.666-77', rg='RG445566', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=perito.id, tipo=TipoOcorrencia.POSSE_ARMA, prioridade=PrioridadeOcorrencia.MEDIA, data_ocorrencia=datetime.now() - timedelta(hours=12), descricao='Arma apreendida para exame balistico', municipio='Bengo', provincia='Bengo')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.BALISTICA, descricao='Projetil e arma para confronto', local_coleta='Sala de custodia', coletado_por_id=perito.id)
        laudo = await laudo_service.emitir_laudo(prova_id=prova.id, tipo_laudo=TipoLaudo.BALISTICO, perito_id=perito.id, conclusao='Correspondencia entre arma apreendida e vestigios analisados.')
        atualizado = await laudo_service.atualizar_status(laudo_id=laudo.id, status=StatusLaudo.RETIFICADO, observacoes='Ajuste de metadados do exame')
        assert atualizado.status == StatusLaudo.RETIFICADO
        assert atualizado.ativo is True
    asyncio.run(scenario())