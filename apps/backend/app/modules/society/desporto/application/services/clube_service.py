from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.desporto.application.ports.clube_repository_port import (
    ClubeRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.educacao_service_port import (
    EducacaoServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import (
    ObrasPublicasServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube
from apps.backend.app.modules.society.desporto.domain.models.clube import Clube


class ClubeService:
    def __init__(
        self,
        *,
        clube_repo: ClubeRepositoryPort,
        educacao_service: EducacaoServicePort | None = None,
        obras_publicas_service: ObrasPublicasServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.clube_repo = clube_repo
        self.educacao_service = educacao_service
        self.obras_publicas_service = obras_publicas_service
        self.request_service = request_service

    async def cadastrar_clube(
        self,
        *,
        nome: str,
        sigla: str,
        tipo: TipoClube,
        modalidade_principal: ModalidadeDesportiva,
        municipio: str,
        provincia: str,
        data_fundacao: date | None = None,
        codigo_obra_instalacao: str | None = None,
        instituicao_educacional_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Clube:
        await self._validar_integracoes(
            codigo_obra_instalacao=codigo_obra_instalacao,
            instituicao_educacional_id=instituicao_educacional_id,
        )
        codigo = await self.clube_repo.next_codigo()
        clube = Clube.cadastrar(
            codigo_clube=codigo,
            nome=nome,
            sigla=sigla,
            tipo=tipo,
            modalidade_principal=modalidade_principal,
            municipio=municipio,
            provincia=provincia,
            data_fundacao=data_fundacao,
            codigo_obra_instalacao=codigo_obra_instalacao,
            instituicao_educacional_id=instituicao_educacional_id,
            observacoes=observacoes,
        )
        saved = await self.clube_repo.save(clube)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_CLUBE",
                entity_id=saved.id,
                metadata={
                    "codigo": saved.codigo_clube,
                    "nome": saved.nome,
                    "sigla": saved.sigla,
                    "tipo": saved.tipo.value,
                    "modalidade_principal": saved.modalidade_principal.value,
                },
                numero_processo=saved.codigo_clube,
            )
        return saved

    async def buscar_clube(self, clube_id: UUID) -> Clube:
        item = await self.clube_repo.get_by_id(clube_id)
        if item is None:
            raise ValueError("Clube nao encontrado")
        return item

    async def listar_clubes(
        self,
        *,
        tipo: TipoClube | None = None,
        modalidade: ModalidadeDesportiva | None = None,
        municipio: str | None = None,
        somente_ativos: bool = True,
    ) -> list[Clube]:
        if municipio is not None:
            itens = await self.clube_repo.list_by_municipio(municipio)
        elif modalidade is not None:
            itens = await self.clube_repo.list_by_modalidade(modalidade)
        elif tipo is not None:
            itens = await self.clube_repo.list_by_tipo(tipo)
        else:
            itens = await self.clube_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_clube(
        self,
        *,
        clube_id: UUID,
        nome: str | None = None,
        sigla: str | None = None,
        tipo: TipoClube | None = None,
        modalidade_principal: ModalidadeDesportiva | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        data_fundacao: date | None = None,
        codigo_obra_instalacao: str | None = None,
        instituicao_educacional_id: UUID | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> Clube:
        item = await self.buscar_clube(clube_id)
        await self._validar_integracoes(
            codigo_obra_instalacao=codigo_obra_instalacao,
            instituicao_educacional_id=instituicao_educacional_id,
        )
        item.atualizar(
            nome=nome,
            sigla=sigla,
            tipo=tipo,
            modalidade_principal=modalidade_principal,
            municipio=municipio,
            provincia=provincia,
            data_fundacao=data_fundacao,
            codigo_obra_instalacao=codigo_obra_instalacao,
            instituicao_educacional_id=instituicao_educacional_id,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.clube_repo.save(item)

    async def remover_clube(self, clube_id: UUID) -> None:
        deleted = await self.clube_repo.delete(clube_id)
        if not deleted:
            raise ValueError("Clube nao encontrado")

    async def _validar_integracoes(
        self, *, codigo_obra_instalacao: str | None, instituicao_educacional_id: UUID | None
    ) -> None:
        if codigo_obra_instalacao and self.obras_publicas_service is not None:
            obra_ok = await self.obras_publicas_service.obra_exists(codigo_obra_instalacao)
            if not obra_ok:
                raise ValueError("Obra de instalacao informada nao encontrada")
        if instituicao_educacional_id is not None and self.educacao_service is not None:
            instituicao_ok = await self.educacao_service.instituicao_exists(
                instituicao_educacional_id
            )
            if not instituicao_ok:
                raise ValueError("Instituicao educacional informada nao encontrada")
