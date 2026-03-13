from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.public_security.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.public_security.application.ports.unidade_policial_repository_port import UnidadePolicialRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import StatusUnidadePolicial, TipoUnidadePolicial
from apps.backend.app.modules.public_security.domain.models.unidade_policial import UnidadePolicial

class UnidadePolicialService:

    def __init__(self, *, unidade_repo: UnidadePolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.unidade_repo = unidade_repo
        self.request_service = request_service

    async def cadastrar_unidade(self, *, nome: str, tipo: TipoUnidadePolicial, municipio: str, provincia: str, endereco: str, comandante: str, telefone: str | None=None, email: str | None=None, observacoes: str | None=None) -> UnidadePolicial:
        codigo_unidade = await self.unidade_repo.next_codigo()
        unidade = UnidadePolicial.cadastrar(codigo_unidade=codigo_unidade, nome=nome, tipo=tipo, municipio=municipio, provincia=provincia, endereco=endereco, comandante=comandante, telefone=telefone, email=email, observacoes=observacoes)
        saved = await self.unidade_repo.save(unidade)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_UNIDADE_POLICIAL', entity_id=saved.id, numero_processo=saved.codigo_unidade, metadata={'codigo_unidade': saved.codigo_unidade, 'nome': saved.nome, 'tipo': saved.tipo.value, 'municipio': saved.municipio})
        return saved

    async def buscar_unidade(self, unidade_id: UUID) -> UnidadePolicial:
        unidade = await self.unidade_repo.get_by_id(unidade_id)
        if unidade is None:
            raise ValueError('Unidade policial nao encontrada')
        return unidade

    async def listar_unidades(self, *, municipio: str | None=None, status: StatusUnidadePolicial | None=None) -> list[UnidadePolicial]:
        if municipio:
            return await self.unidade_repo.list_by_municipio(municipio)
        if status is not None:
            return await self.unidade_repo.list_by_status(status)
        return await self.unidade_repo.list_all()

    async def atualizar_status(self, *, unidade_id: UUID, status: StatusUnidadePolicial, motivo: str | None=None) -> UnidadePolicial:
        unidade = await self.buscar_unidade(unidade_id)
        unidade.atualizar_status(status, motivo)
        return await self.unidade_repo.save(unidade)

    async def remover_unidade(self, unidade_id: UUID) -> None:
        deleted = await self.unidade_repo.delete(unidade_id)
        if not deleted:
            raise ValueError('Unidade policial nao encontrada')