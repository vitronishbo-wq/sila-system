from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.pecuaria.application.ports import CitizenServicePort, PecuaristaRepositoryPort, RequestServicePort
from app.modules.resources.pecuaria.domain.enums import StatusPecuarista
from app.modules.resources.pecuaria.domain.models.pecuarista import Pecuarista

class PecuaristaService:

    def __init__(self, pecuarista_repo: PecuaristaRepositoryPort, citizen_service: CitizenServicePort | None=None, request_service: RequestServicePort | None=None):
        self.pecuarista_repo = pecuarista_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_pecuarista(self, *, nome: str, documento: str, documento_tipo: str, telefone: str | None=None, email: str | None=None, endereco: str | None=None, citizen_id: UUID | None=None, empresa_id: UUID | None=None, observacoes: str | None=None) -> Pecuarista:
        existente = await self.pecuarista_repo.get_by_documento(documento)
        if existente and existente.status in {StatusPecuarista.PENDENTE, StatusPecuarista.ATIVO, StatusPecuarista.SUSPENSO}:
            raise ValueError('Ja existe pecuarista para este documento')
        if citizen_id and self.citizen_service:
            ativo = await self.citizen_service.is_citizen_active(citizen_id)
            if not ativo:
                raise ValueError('Cidadao informado nao esta ativo')
        item = Pecuarista.criar(nome=nome, documento=documento, documento_tipo=documento_tipo, telefone=telefone, email=email, endereco=endereco, citizen_id=citizen_id, empresa_id=empresa_id, observacoes=observacoes)
        item.cadastro_pecuarista = await self.pecuarista_repo.next_cadastro()
        saved = await self.pecuarista_repo.save(item)
        if self.request_service and citizen_id:
            await self.request_service.create_request(request_type='cadastro_pecuarista', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.cadastro_pecuarista, metadata={'documento': saved.documento})
        return saved

    async def ativar_pecuarista(self, cadastro_pecuarista: str, actor_id: UUID | None=None) -> Pecuarista:
        item = await self.pecuarista_repo.get_by_cadastro(cadastro_pecuarista)
        if not item:
            raise ValueError('Pecuarista nao encontrado')
        item.ativar()
        saved = await self.pecuarista_repo.save(item)
        if self.request_service and actor_id:
            await self.request_service.complete_request(entity_id=saved.id, actor_id=actor_id, metadata={'status': saved.status.value, 'data': str(date.today())})
        return saved

    async def obter_por_cadastro(self, cadastro_pecuarista: str) -> Pecuarista | None:
        return await self.pecuarista_repo.get_by_cadastro(cadastro_pecuarista)

    async def listar(self, status: StatusPecuarista | None=None) -> list[Pecuarista]:
        return await self.pecuarista_repo.list_by_status(status=status)