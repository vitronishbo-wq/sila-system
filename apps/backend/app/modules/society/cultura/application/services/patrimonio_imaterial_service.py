from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.cultura.application.ports.educacao_service_port import (
    EducacaoServicePort,
)
from apps.backend.app.modules.society.cultura.application.ports.patrimonio_imaterial_repository_port import (
    PatrimonioImaterialRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.cultura.application.ports.turismo_service_port import (
    TurismoServicePort,
)
from apps.backend.app.modules.society.cultura.domain.enums import (
    CategoriaPatrimonioImaterial,
    StatusPatrimonioImaterial,
)
from apps.backend.app.modules.society.cultura.domain.models.patrimonio_imaterial import (
    PatrimonioImaterial,
)


class PatrimonioImaterialService:
    def __init__(
        self,
        *,
        patrimonio_repo: PatrimonioImaterialRepositoryPort,
        turismo_service: TurismoServicePort | None = None,
        educacao_service: EducacaoServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.patrimonio_repo = patrimonio_repo
        self.turismo_service = turismo_service
        self.educacao_service = educacao_service
        self.request_service = request_service

    async def registrar_patrimonio(
        self,
        *,
        nome: str,
        categoria: CategoriaPatrimonioImaterial,
        descricao: str,
        comunidade: str,
        municipio: str,
        provincia: str,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        plano_salvaguarda: str | None = None,
        observacoes: str | None = None,
    ) -> PatrimonioImaterial:
        await self._validar_integracoes(
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
        )
        registro = await self.patrimonio_repo.next_registro()
        patrimonio = PatrimonioImaterial.registrar(
            registro_pni=registro,
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            comunidade=comunidade,
            municipio=municipio,
            provincia=provincia,
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
            plano_salvaguarda=plano_salvaguarda,
            observacoes=observacoes,
        )
        saved = await self.patrimonio_repo.save(patrimonio)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="REGISTRO_PATRIMONIO_IMATERIAL",
                entity_id=saved.id,
                metadata={
                    "registro_pni": saved.registro_pni,
                    "categoria": saved.categoria.value,
                    "municipio": saved.municipio,
                },
                numero_processo=saved.registro_pni,
            )
        return saved

    async def buscar_patrimonio(self, patrimonio_id: UUID) -> PatrimonioImaterial:
        item = await self.patrimonio_repo.get_by_id(patrimonio_id)
        if item is None:
            raise ValueError("Patrimonio imaterial nao encontrado")
        return item

    async def listar_patrimonios(
        self,
        *,
        categoria: CategoriaPatrimonioImaterial | None = None,
        municipio: str | None = None,
        status: StatusPatrimonioImaterial | None = None,
        somente_ativos: bool = True,
    ) -> list[PatrimonioImaterial]:
        if categoria is not None:
            itens = await self.patrimonio_repo.list_by_categoria(categoria)
        elif municipio is not None:
            itens = await self.patrimonio_repo.list_by_municipio(municipio)
        elif status is not None:
            itens = await self.patrimonio_repo.list_by_status(status)
        else:
            itens = await self.patrimonio_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_patrimonio(
        self,
        *,
        patrimonio_id: UUID,
        nome: str | None = None,
        categoria: CategoriaPatrimonioImaterial | None = None,
        descricao: str | None = None,
        comunidade: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        plano_salvaguarda: str | None = None,
        status: StatusPatrimonioImaterial | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> PatrimonioImaterial:
        item = await self.buscar_patrimonio(patrimonio_id)
        await self._validar_integracoes(
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
        )
        item.atualizar(
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            comunidade=comunidade,
            municipio=municipio,
            provincia=provincia,
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
            plano_salvaguarda=plano_salvaguarda,
            status=status,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.patrimonio_repo.save(item)

    async def remover_patrimonio(self, patrimonio_id: UUID) -> None:
        deleted = await self.patrimonio_repo.delete(patrimonio_id)
        if not deleted:
            raise ValueError("Patrimonio imaterial nao encontrado")

    async def _validar_integracoes(
        self, *, atracao_turistica_id: UUID | None, instituicao_educacional_id: UUID | None
    ) -> None:
        if atracao_turistica_id is not None and self.turismo_service is not None:
            existe = await self.turismo_service.atracao_exists(atracao_turistica_id)
            if not existe:
                raise ValueError("Atracao turistica nao encontrada")
        if instituicao_educacional_id is not None and self.educacao_service is not None:
            existe = await self.educacao_service.instituicao_exists(instituicao_educacional_id)
            if not existe:
                raise ValueError("Instituicao educacional nao encontrada")
