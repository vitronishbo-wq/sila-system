from __future__ import annotations
import asyncio
from datetime import date
from decimal import Decimal
from apps.backend.app.modules.society.cultura.application.services.projeto_cultural_service import ProjetoCulturalService
from apps.backend.app.modules.society.cultura.domain.enums import NaturezaProjetoCultural, StatusProjetoCultural, TipoProjetoCultural
from apps.backend.app.modules.society.cultura.tests._fakes import FakeRequestService, InMemoryProjetoCulturalRepository

def test_cadastrar_e_aprovar_projeto() -> None:

    async def scenario() -> None:
        service = ProjetoCulturalService(projeto_repo=InMemoryProjetoCulturalRepository(), request_service=FakeRequestService())
        projeto = await service.cadastrar_projeto(titulo='Festival de Musica Tradicional', tipo=TipoProjetoCultural.PRODUCAO, natureza=NaturezaProjetoCultural.CULTURAL, proponente_cpf_cnpj='12345678901', proponente_nome='Associacao Cultura Viva', resumo='Projeto para difusao musical em comunidades locais.', valor_solicitado=Decimal('50000.00'), objetivos=['Difundir artistas locais', 'Fortalecer economia criativa'])
        aprovado = await service.aprovar_projeto(projeto_id=projeto.id, valor_aprovado=Decimal('45000.00'))
        assert projeto.codigo_projeto.startswith('PROJ/')
        assert aprovado.status == StatusProjetoCultural.APROVADO
        assert aprovado.valor_aprovado == Decimal('45000.00')
    asyncio.run(scenario())

def test_fluxo_execucao_projeto() -> None:

    async def scenario() -> None:
        service = ProjetoCulturalService(projeto_repo=InMemoryProjetoCulturalRepository())
        projeto = await service.cadastrar_projeto(titulo='Projeto de Preservacao', tipo=TipoProjetoCultural.PRESERVACAO, natureza=NaturezaProjetoCultural.TECNICA, proponente_cpf_cnpj='0099887766', proponente_nome='Instituto Memoria', resumo='Projeto para preservar acervo historico local.', valor_solicitado=Decimal('20000.00'), submeter=True)
        await service.aprovar_projeto(projeto_id=projeto.id, valor_aprovado=Decimal('20000.00'))
        iniciado = await service.iniciar_execucao(projeto_id=projeto.id, data_inicio=date(2026, 4, 1))
        assert iniciado.status == StatusProjetoCultural.EM_EXECUCAO
        concluido = await service.concluir_projeto(projeto_id=projeto.id, data_fim=date(2026, 6, 1))
        assert concluido.status == StatusProjetoCultural.CONCLUIDO
    asyncio.run(scenario())