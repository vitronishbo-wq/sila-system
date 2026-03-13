from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.society.cultura.application.ports.artista_repository_port import ArtistaRepositoryPort
from app.modules.society.cultura.application.ports.educacao_service_port import EducacaoServicePort
from app.modules.society.cultura.application.ports.grupo_artistico_repository_port import GrupoArtisticoRepositoryPort
from app.modules.society.cultura.application.ports.request_service_port import RequestServicePort
from app.modules.society.cultura.domain.enums import TipoGrupoArtistico
from app.modules.society.cultura.domain.models.grupo_artistico import GrupoArtistico

class GrupoArtisticoService:

    def __init__(self, *, grupo_repo: GrupoArtisticoRepositoryPort, artista_repo: ArtistaRepositoryPort, educacao_service: EducacaoServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.grupo_repo = grupo_repo
        self.artista_repo = artista_repo
        self.educacao_service = educacao_service
        self.request_service = request_service

    async def cadastrar_grupo(self, *, nome: str, tipo: TipoGrupoArtistico, lider_artista_id: UUID, descricao: str | None=None, data_fundacao: date | None=None, municipio: str | None=None, provincia: str | None=None, instituicao_educacional_id: UUID | None=None, membros_ids: list[UUID] | None=None, observacoes: str | None=None) -> GrupoArtistico:
        await self._validar_lider(lider_artista_id)
        await self._validar_integracao_educacao(instituicao_educacional_id)
        codigo = await self.grupo_repo.next_codigo()
        grupo = GrupoArtistico.criar(codigo_grupo=codigo, nome=nome, tipo=tipo, lider_artista_id=lider_artista_id, descricao=descricao, data_fundacao=data_fundacao, municipio=municipio, provincia=provincia, instituicao_educacional_id=instituicao_educacional_id, membros_ids=membros_ids, observacoes=observacoes)
        saved = await self.grupo_repo.save(grupo)
        lider = await self.artista_repo.get_by_id(lider_artista_id)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_GRUPO_ARTISTICO', entity_id=saved.id, citizen_id=lider.citizen_id if lider else None, metadata={'codigo_grupo': saved.codigo_grupo, 'nome': saved.nome, 'tipo': saved.tipo.value}, numero_processo=saved.codigo_grupo)
        return saved

    async def buscar_grupo(self, grupo_id: UUID) -> GrupoArtistico:
        item = await self.grupo_repo.get_by_id(grupo_id)
        if item is None:
            raise ValueError('Grupo artistico nao encontrado')
        return item

    async def listar_grupos(self, *, tipo: TipoGrupoArtistico | None=None, municipio: str | None=None, somente_ativos: bool=True) -> list[GrupoArtistico]:
        if tipo is not None:
            itens = await self.grupo_repo.list_by_tipo(tipo)
        elif municipio is not None:
            itens = await self.grupo_repo.list_by_municipio(municipio)
        else:
            itens = await self.grupo_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_grupo(self, *, grupo_id: UUID, nome: str | None=None, tipo: TipoGrupoArtistico | None=None, lider_artista_id: UUID | None=None, descricao: str | None=None, data_fundacao: date | None=None, municipio: str | None=None, provincia: str | None=None, instituicao_educacional_id: UUID | None=None, membros_ids: list[UUID] | None=None, ativo: bool | None=None, observacoes: str | None=None) -> GrupoArtistico:
        item = await self.buscar_grupo(grupo_id)
        if lider_artista_id is not None:
            await self._validar_lider(lider_artista_id)
        await self._validar_integracao_educacao(instituicao_educacional_id)
        item.atualizar(nome=nome, tipo=tipo, lider_artista_id=lider_artista_id, descricao=descricao, data_fundacao=data_fundacao, municipio=municipio, provincia=provincia, instituicao_educacional_id=instituicao_educacional_id, membros_ids=membros_ids, ativo=ativo, observacoes=observacoes)
        return await self.grupo_repo.save(item)

    async def remover_grupo(self, grupo_id: UUID) -> None:
        deleted = await self.grupo_repo.delete(grupo_id)
        if not deleted:
            raise ValueError('Grupo artistico nao encontrado')

    async def _validar_lider(self, lider_artista_id: UUID) -> None:
        lider = await self.artista_repo.get_by_id(lider_artista_id)
        if lider is None:
            raise ValueError('Artista lider nao encontrado')

    async def _validar_integracao_educacao(self, instituicao_educacional_id: UUID | None) -> None:
        if instituicao_educacional_id is not None and self.educacao_service is not None:
            existe = await self.educacao_service.instituicao_exists(instituicao_educacional_id)
            if not existe:
                raise ValueError('Instituicao educacional nao encontrada')