from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.resources.ambiente.application.ports import (
    EstudoRepositoryPort,
    LicencaRepositoryPort,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import (
    StatusEstudoAmbiental,
    TipoEstudoAmbiental,
)
from apps.backend.app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto
from apps.backend.app.modules.resources.ambiente.exceptions import (
    EstudoNotFoundError,
    LicencaNotFoundError,
)


class EstudoService:
    def __init__(
        self, *, licenca_repo: LicencaRepositoryPort, estudo_repo: EstudoRepositoryPort
    ) -> None:
        self._licenca_repo = licenca_repo
        self._estudo_repo = estudo_repo

    async def submeter(
        self,
        *,
        numero_licenca: str,
        tipo: TipoEstudoAmbiental,
        descricao: str,
        responsavel_tecnico: str,
    ) -> EstudoImpacto:
        licenca = await self._licenca_repo.get_by_numero(numero_licenca)
        if not licenca:
            raise LicencaNotFoundError("Licenca ambiental nao encontrada")
        item = EstudoImpacto.submeter(
            numero_licenca=numero_licenca,
            tipo=tipo,
            descricao=descricao,
            responsavel_tecnico=responsavel_tecnico,
        )
        item.numero_estudo = await self._estudo_repo.next_numero()
        return await self._estudo_repo.save(item)

    async def iniciar_analise(self, numero_estudo: str) -> EstudoImpacto:
        item = await self._estudo_repo.get_by_numero(numero_estudo)
        if not item:
            raise EstudoNotFoundError("Estudo ambiental nao encontrado")
        item.iniciar_analise()
        return await self._estudo_repo.save(item)

    async def aprovar(self, numero_estudo: str, analista_id: UUID) -> EstudoImpacto:
        item = await self._estudo_repo.get_by_numero(numero_estudo)
        if not item:
            raise EstudoNotFoundError("Estudo ambiental nao encontrado")
        item.aprovar(analista_id)
        return await self._estudo_repo.save(item)

    async def solicitar_complementacao(
        self, numero_estudo: str, analista_id: UUID, motivo: str
    ) -> EstudoImpacto:
        item = await self._estudo_repo.get_by_numero(numero_estudo)
        if not item:
            raise EstudoNotFoundError("Estudo ambiental nao encontrado")
        item.solicitar_complementacao(analista_id, motivo)
        return await self._estudo_repo.save(item)

    async def obter_por_numero(self, numero_estudo: str) -> EstudoImpacto:
        item = await self._estudo_repo.get_by_numero(numero_estudo)
        if not item:
            raise EstudoNotFoundError("Estudo ambiental nao encontrado")
        return item

    async def listar(
        self,
        *,
        numero_licenca: str | None = None,
        tipo: TipoEstudoAmbiental | None = None,
        status: StatusEstudoAmbiental | None = None,
    ) -> list[EstudoImpacto]:
        return await self._estudo_repo.list(numero_licenca=numero_licenca, tipo=tipo, status=status)
