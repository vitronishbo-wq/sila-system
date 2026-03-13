from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4
import pytest
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import ProvaPericialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusProva, TipoAgente, TipoOcorrencia, TipoProva, TipoUnidadePolicial, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryOcorrenciaRepository, InMemoryPolicialRepository, InMemoryProvaPericialRepository, InMemoryUnidadePolicialRepository

def test_coletar_prova_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Delegacia Cientifica', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua Cientifica', comandante='Delegado Pericial')
        perito = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Perito Ferreira', data_nascimento=date.today() - timedelta(days=365 * 36), cpf='666.777.888-99', rg='RG667788', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=perito.id, tipo=TipoOcorrencia.FALSIDADE, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=4), descricao='Apreensao de documentos com suspeita de falsificacao', municipio='Luanda', provincia='Luanda')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DOCUMENTAL, descricao='Documentos apreendidos para exame', local_coleta='Arquivo central', coletado_por_id=perito.id)
        assert prova.codigo_prova.startswith('PRV/')
        assert prova.status == StatusProva.COLETADA
    asyncio.run(scenario())

def test_coletar_prova_falha_ocorrencia_inexistente() -> None:

    async def scenario() -> None:
        service = ProvaPericialService(prova_repo=InMemoryProvaPericialRepository(), ocorrencia_repo=InMemoryOcorrenciaRepository(), policial_repo=InMemoryPolicialRepository())
        with pytest.raises(ValueError, match='Ocorrencia nao encontrada'):
            await service.coletar_prova(ocorrencia_id=uuid4(), tipo=TipoProva.BIOLOGICA, descricao='Vestigio biologico coletado no local', local_coleta='Laboratorio')
    asyncio.run(scenario())

def test_vincular_cadeia_custodia_prova() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Base Custodia', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Bengo', provincia='Bengo', endereco='Zona B', comandante='Comandante BC')
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, tipo=TipoOcorrencia.TRAFICO, prioridade=PrioridadeOcorrencia.CRITICA, data_ocorrencia=datetime.now() - timedelta(days=1), descricao='Apreensao de substancia entorpecente', municipio='Bengo', provincia='Bengo')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.MATERIAL, descricao='Amostra de substancia apreendida', local_coleta='Viatura operacional')
        cadeia_id = uuid4()
        atualizada = await prova_service.vincular_cadeia_custodia(prova_id=prova.id, cadeia_custodia_id=cadeia_id)
        assert atualizada.cadeia_custodia_id == cadeia_id
    asyncio.run(scenario())