from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.juventude.application.ports.programa_repository_port import (
    ProgramaRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma
from apps.backend.app.modules.society.juventude.domain.models.programa_juvenil import (
    ProgramaJuvenil,
)


class ProgramaService:
    def __init__(
        self,
        *,
        programa_repo: ProgramaRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.programa_repo = programa_repo
        self.request_service = request_service

    async def criar_programa(
        self,
        *,
        nome: str,
        tipo: TipoPrograma,
        data_inicio: date,
        data_fim: date | None = None,
        vagas: int | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        observacoes: str | None = None,
    ) -> ProgramaJuvenil:
        codigo = await self.programa_repo.next_codigo()
        programa = ProgramaJuvenil.criar(
            codigo_programa=codigo,
            nome=nome,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            vagas=vagas,
            municipio=municipio,
            provincia=provincia,
            observacoes=observacoes,
        )
        saved = await self.programa_repo.save(programa)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_PROGRAMA_JUVENTUDE",
                entity_id=saved.id,
                numero_processo=saved.codigo_programa,
                metadata={
                    "codigo_programa": saved.codigo_programa,
                    "nome": saved.nome,
                    "tipo": saved.tipo.value,
                },
            )
        return saved

    async def buscar_programa(self, programa_id: UUID) -> ProgramaJuvenil:
        programa = await self.programa_repo.get_by_id(programa_id)
        if programa is None:
            raise ValueError("Programa nao encontrado")
        return programa

    async def listar_programas(
        self, *, tipo: TipoPrograma | None = None, status: StatusPrograma | None = None
    ) -> list[ProgramaJuvenil]:
        if tipo is not None:
            return await self.programa_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.programa_repo.list_by_status(status)
        return await self.programa_repo.list_all()

    async def atualizar_status(
        self, *, programa_id: UUID, status: StatusPrograma
    ) -> ProgramaJuvenil:
        programa = await self.buscar_programa(programa_id)
        programa.atualizar_status(status)
        return await self.programa_repo.save(programa)

    async def remover_programa(self, programa_id: UUID) -> None:
        deleted = await self.programa_repo.delete(programa_id)
        if not deleted:
            raise ValueError("Programa nao encontrado")
