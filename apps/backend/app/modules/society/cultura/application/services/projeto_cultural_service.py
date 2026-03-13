from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.society.cultura.application.events import ProjetoAprovadoEvent, event_bus
from apps.backend.app.modules.society.cultura.application.ports.projeto_cultural_repository_port import ProjetoCulturalRepositoryPort
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.cultura.domain.enums import NaturezaProjetoCultural, StatusProjetoCultural, TipoProjetoCultural
from apps.backend.app.modules.society.cultura.domain.models.projeto_cultural import ProjetoCultural

class ProjetoCulturalService:

    def __init__(self, *, projeto_repo: ProjetoCulturalRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.projeto_repo = projeto_repo
        self.request_service = request_service

    async def cadastrar_projeto(self, *, titulo: str, tipo: TipoProjetoCultural, natureza: NaturezaProjetoCultural, proponente_cpf_cnpj: str, proponente_nome: str, resumo: str, valor_solicitado: Decimal, justificativa: str | None=None, edital_id: UUID | None=None, objetivos: list[str] | None=None, observacoes: str | None=None, submeter: bool=True) -> ProjetoCultural:
        codigo = await self.projeto_repo.next_codigo()
        projeto = ProjetoCultural.cadastrar(codigo_projeto=codigo, titulo=titulo, tipo=tipo, natureza=natureza, proponente_cpf_cnpj=proponente_cpf_cnpj, proponente_nome=proponente_nome, resumo=resumo, valor_solicitado=valor_solicitado, justificativa=justificativa, edital_id=edital_id, objetivos=objetivos, observacoes=observacoes)
        if submeter:
            projeto.submeter()
        saved = await self.projeto_repo.save(projeto)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_PROJETO_CULTURAL', entity_id=saved.id, numero_processo=saved.codigo_projeto, metadata={'codigo_projeto': saved.codigo_projeto, 'tipo': saved.tipo.value, 'status': saved.status.value})
        return saved

    async def buscar_projeto(self, projeto_id: UUID) -> ProjetoCultural:
        item = await self.projeto_repo.get_by_id(projeto_id)
        if item is None:
            raise ValueError('Projeto cultural nao encontrado')
        return item

    async def listar_projetos(self, *, tipo: TipoProjetoCultural | None=None, status: StatusProjetoCultural | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativos: bool=True) -> list[ProjetoCultural]:
        if tipo is not None:
            items = await self.projeto_repo.list_by_tipo(tipo)
        elif status is not None:
            items = await self.projeto_repo.list_by_status(status)
        elif data_inicio is not None and data_fim is not None:
            items = await self.projeto_repo.list_by_periodo(data_inicio, data_fim)
        else:
            items = await self.projeto_repo.list_all()
        if somente_ativos:
            return [item for item in items if item.ativo]
        return items

    async def atualizar_projeto(self, *, projeto_id: UUID, titulo: str | None=None, tipo: TipoProjetoCultural | None=None, natureza: NaturezaProjetoCultural | None=None, resumo: str | None=None, valor_solicitado: Decimal | None=None, justificativa: str | None=None, objetivos: list[str] | None=None, ativo: bool | None=None, observacoes: str | None=None) -> ProjetoCultural:
        item = await self.buscar_projeto(projeto_id)
        item.atualizar(titulo=titulo, tipo=tipo, natureza=natureza, resumo=resumo, valor_solicitado=valor_solicitado, justificativa=justificativa, objetivos=objetivos, ativo=ativo, observacoes=observacoes)
        return await self.projeto_repo.save(item)

    async def aprovar_projeto(self, *, projeto_id: UUID, valor_aprovado: Decimal) -> ProjetoCultural:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.aprovar(valor_aprovado=valor_aprovado)
        saved = await self.projeto_repo.save(projeto)
        await event_bus.publish(ProjetoAprovadoEvent(projeto_id=saved.id, codigo_projeto=saved.codigo_projeto, titulo=saved.titulo, proponente=saved.proponente_nome, valor_aprovado=float(valor_aprovado), edital_id=saved.edital_id))
        return saved

    async def reprovar_projeto(self, projeto_id: UUID) -> ProjetoCultural:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.reprovar()
        return await self.projeto_repo.save(projeto)

    async def iniciar_execucao(self, *, projeto_id: UUID, data_inicio: date) -> ProjetoCultural:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.iniciar_execucao(data_inicio=data_inicio)
        return await self.projeto_repo.save(projeto)

    async def concluir_projeto(self, *, projeto_id: UUID, data_fim: date) -> ProjetoCultural:
        projeto = await self.buscar_projeto(projeto_id)
        projeto.concluir(data_fim=data_fim)
        return await self.projeto_repo.save(projeto)

    async def remover_projeto(self, projeto_id: UUID) -> None:
        deleted = await self.projeto_repo.delete(projeto_id)
        if not deleted:
            raise ValueError('Projeto cultural nao encontrado')