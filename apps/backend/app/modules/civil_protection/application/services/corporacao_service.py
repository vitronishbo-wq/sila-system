from __future__ import annotations
from uuid import UUID
from app.modules.civil_protection.application.ports.corporacao_repository_port import CorporacaoRepositoryPort
from app.modules.civil_protection.application.ports.request_service_port import RequestServicePort
from app.modules.civil_protection.domain.enums import StatusCorporacao
from app.modules.civil_protection.domain.models.corporacao import Corporacao

class CorporacaoService:

    def __init__(self, *, corporacao_repo: CorporacaoRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.corporacao_repo = corporacao_repo
        self.request_service = request_service

    async def cadastrar_corporacao(self, *, nome: str, municipio: str, provincia: str, endereco: str, comandante: str, telefone: str | None=None, email: str | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> Corporacao:
        codigo_corporacao = await self.corporacao_repo.next_codigo()
        corporacao = Corporacao.cadastrar(codigo_corporacao=codigo_corporacao, nome=nome, municipio=municipio, provincia=provincia, endereco=endereco, comandante=comandante, telefone=telefone, email=email, observacoes=observacoes)
        saved = await self.corporacao_repo.save(corporacao)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_CORPORACAO', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.codigo_corporacao, metadata={'codigo_corporacao': saved.codigo_corporacao, 'nome': saved.nome, 'municipio': saved.municipio})
        return saved

    async def buscar_corporacao(self, corporacao_id: UUID) -> Corporacao:
        corporacao = await self.corporacao_repo.get_by_id(corporacao_id)
        if corporacao is None:
            raise ValueError('Corporacao nao encontrada')
        return corporacao

    async def listar_corporacoes(self, *, municipio: str | None=None, status: StatusCorporacao | None=None) -> list[Corporacao]:
        if municipio:
            return await self.corporacao_repo.list_by_municipio(municipio)
        if status is not None:
            return await self.corporacao_repo.list_by_status(status)
        return await self.corporacao_repo.list_all()

    async def atualizar_status(self, *, corporacao_id: UUID, status: StatusCorporacao, motivo: str | None=None) -> Corporacao:
        corporacao = await self.buscar_corporacao(corporacao_id)
        corporacao.atualizar_status(status, motivo)
        return await self.corporacao_repo.save(corporacao)

    async def remover_corporacao(self, corporacao_id: UUID) -> None:
        deleted = await self.corporacao_repo.delete(corporacao_id)
        if not deleted:
            raise ValueError('Corporacao nao encontrada')