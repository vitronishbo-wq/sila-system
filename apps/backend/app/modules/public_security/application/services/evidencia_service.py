from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.public_security.application.ports.cadeia_custodia_repository_port import (
    CadeiaCustodiaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.evidencia_repository_port import (
    EvidenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.policial_repository_port import (
    PolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.public_security.application.ports.vestigio_repository_port import (
    VestigioRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia, TipoEvidencia
from apps.backend.app.modules.public_security.domain.models.evidencia import Evidencia


class EvidenciaService:
    def __init__(
        self,
        *,
        evidencia_repo: EvidenciaRepositoryPort,
        vestigio_repo: VestigioRepositoryPort,
        cadeia_repo: CadeiaCustodiaRepositoryPort,
        policial_repo: PolicialRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.evidencia_repo = evidencia_repo
        self.vestigio_repo = vestigio_repo
        self.cadeia_repo = cadeia_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def registrar_evidencia(
        self,
        *,
        vestigio_id: UUID,
        tipo: TipoEvidencia,
        descricao: str,
        fonte: str,
        confiabilidade: int = 3,
        analisado_por_id: UUID | None = None,
        observacoes: str | None = None,
        citizen_id: UUID | None = None,
    ) -> Evidencia:
        vestigio = await self.vestigio_repo.get_by_id(vestigio_id)
        if vestigio is None:
            raise ValueError("Vestigio nao encontrado para registro de evidencia")
        cadeia = await self.cadeia_repo.get_by_id(vestigio.cadeia_custodia_id)
        if cadeia is None:
            raise ValueError("Cadeia de custodia do vestigio nao encontrada")
        if analisado_por_id is not None:
            analista = await self.policial_repo.get_by_id(analisado_por_id)
            if analista is None:
                raise ValueError("Analista responsavel da evidencia nao encontrado")
        codigo = await self.evidencia_repo.next_codigo()
        evidencia = Evidencia.registrar(
            codigo_evidencia=codigo,
            vestigio_id=vestigio_id,
            cadeia_custodia_id=vestigio.cadeia_custodia_id,
            tipo=tipo,
            descricao=descricao,
            fonte=fonte,
            confiabilidade=confiabilidade,
            analisado_por_id=analisado_por_id,
            observacoes=observacoes,
        )
        saved = await self.evidencia_repo.save(evidencia)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="REGISTRO_EVIDENCIA",
                entity_id=saved.id,
                numero_processo=saved.codigo_evidencia,
                citizen_id=citizen_id,
                metadata={
                    "codigo_evidencia": saved.codigo_evidencia,
                    "vestigio_id": str(saved.vestigio_id),
                    "cadeia_custodia_id": str(saved.cadeia_custodia_id),
                    "tipo": saved.tipo.value,
                    "confiabilidade": saved.confiabilidade,
                },
            )
        return saved

    async def buscar_evidencia(self, evidencia_id: UUID) -> Evidencia:
        evidencia = await self.evidencia_repo.get_by_id(evidencia_id)
        if evidencia is None:
            raise ValueError("Evidencia nao encontrada")
        return evidencia

    async def listar_evidencias(
        self, *, vestigio_id: UUID | None = None, status: StatusEvidencia | None = None
    ) -> list[Evidencia]:
        if vestigio_id is not None:
            return await self.evidencia_repo.list_by_vestigio(vestigio_id)
        if status is not None:
            return await self.evidencia_repo.list_by_status(status)
        return await self.evidencia_repo.list_all()

    async def atualizar_status(
        self, *, evidencia_id: UUID, status: StatusEvidencia, observacoes: str | None = None
    ) -> Evidencia:
        evidencia = await self.buscar_evidencia(evidencia_id)
        evidencia.atualizar_status(status, observacoes)
        return await self.evidencia_repo.save(evidencia)

    async def remover_evidencia(self, evidencia_id: UUID) -> None:
        deleted = await self.evidencia_repo.delete(evidencia_id)
        if not deleted:
            raise ValueError("Evidencia nao encontrada")
