from __future__ import annotations
from typing import Optional
from uuid import UUID
from app.modules.resources.agricultura.application.ports import CitizenServicePort, ProdutorRepositoryPort, RequestServicePort
from app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor
from app.modules.resources.agricultura.domain.models.produtor import Produtor
from app.modules.resources.agricultura.exceptions import CitizenInactiveError, ProdutorAlreadyExistsError, ProdutorNotFoundError

class ProdutorService:

    def __init__(self, produtor_repo: ProdutorRepositoryPort, citizen_service: CitizenServicePort | None=None, request_service: RequestServicePort | None=None):
        self.produtor_repo = produtor_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_produtor(self, *, nome: str, documento: str, documento_tipo: str, tipo: TipoProdutor, citizen_id: UUID | None=None, empresa_id: UUID | None=None, telefone: str | None=None, email: str | None=None, endereco: str | None=None, observacoes: str | None=None) -> Produtor:
        existente = await self.produtor_repo.get_by_documento(documento)
        if existente and existente.status in {StatusProdutor.PENDENTE, StatusProdutor.ATIVO, StatusProdutor.SUSPENSO}:
            raise ProdutorAlreadyExistsError('Ja existe produtor para este documento')
        if citizen_id and self.citizen_service:
            ativo = await self.citizen_service.is_citizen_active(citizen_id)
            if not ativo:
                raise CitizenInactiveError('Cidadao informado nao esta ativo')
        produtor = Produtor.criar(nome=nome, documento=documento, documento_tipo=documento_tipo, tipo=tipo, citizen_id=citizen_id, empresa_id=empresa_id, telefone=telefone, email=email, endereco=endereco, observacoes=observacoes)
        produtor.cadastro_produtor = await self.produtor_repo.next_cadastro()
        saved = await self.produtor_repo.save(produtor)
        if self.request_service and citizen_id:
            await self.request_service.create_request(request_type='cadastro_produtor', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.cadastro_produtor, metadata={'tipo': saved.tipo.value, 'documento': saved.documento})
        return saved

    async def ativar_produtor(self, cadastro_produtor: str, actor_id: UUID | None=None) -> Produtor:
        produtor = await self.produtor_repo.get_by_cadastro(cadastro_produtor)
        if not produtor:
            raise ProdutorNotFoundError('Produtor nao encontrado')
        produtor.ativar()
        saved = await self.produtor_repo.save(produtor)
        if self.request_service and actor_id:
            await self.request_service.complete_request(entity_id=saved.id, actor_id=actor_id, metadata={'status': saved.status.value})
        return saved

    async def obter_por_cadastro(self, cadastro_produtor: str) -> Produtor | None:
        return await self.produtor_repo.get_by_cadastro(cadastro_produtor)

    async def listar(self, status: Optional[StatusProdutor]=None) -> list[Produtor]:
        return await self.produtor_repo.list_by_status(status=status)