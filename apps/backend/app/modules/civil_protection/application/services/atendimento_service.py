from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.civil_protection.domain.enums import (
    StatusAtendimento,
    StatusDespacho,
    StatusOcorrenciaEmergencial,
)
from apps.backend.app.modules.civil_protection.domain.models.atendimento import Atendimento
from apps.backend.app.modules.civil_protection.domain.ports.atendimento_repository_port import (
    AtendimentoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.bombeiro_repository_port import (
    BombeiroRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.despacho_repository_port import (
    DespachoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.ocorrencia_emergencial_repository_port import (
    OcorrenciaEmergencialRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.request_service_port import (
    RequestServicePort,
)


class AtendimentoService:
    def __init__(
        self,
        *,
        atendimento_repo: AtendimentoRepositoryPort,
        despacho_repo: DespachoRepositoryPort,
        ocorrencia_repo: OcorrenciaEmergencialRepositoryPort,
        bombeiro_repo: BombeiroRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.atendimento_repo = atendimento_repo
        self.despacho_repo = despacho_repo
        self.ocorrencia_repo = ocorrencia_repo
        self.bombeiro_repo = bombeiro_repo
        self.request_service = request_service

    async def registrar_atendimento(
        self,
        *,
        despacho_id: UUID,
        local_atendimento: str,
        vitimas_atendidas: int = 0,
        desalojados_atendidos: int = 0,
        obitos_confirmados: int = 0,
        equipe_responsavel_id: UUID | None = None,
        observacoes: str | None = None,
        citizen_id: UUID | None = None,
    ) -> Atendimento:
        despacho = await self.despacho_repo.get_by_id(despacho_id)
        if despacho is None:
            raise ValueError("Despacho nao encontrado")
        ocorrencia = await self.ocorrencia_repo.get_by_id(despacho.ocorrencia_id)
        if ocorrencia is None:
            raise ValueError("Ocorrencia emergencial do despacho nao encontrada")
        if equipe_responsavel_id is not None:
            bombeiro = await self.bombeiro_repo.get_by_id(equipe_responsavel_id)
            if bombeiro is None:
                raise ValueError("Bombeiro responsavel nao encontrado")
            if bombeiro.corporacao_id != ocorrencia.corporacao_id:
                raise ValueError("Bombeiro responsavel nao pertence a corporacao da ocorrencia")
        codigo_atendimento = await self.atendimento_repo.next_codigo()
        atendimento = Atendimento.iniciar(
            codigo_atendimento=codigo_atendimento,
            despacho_id=despacho.id,
            ocorrencia_id=despacho.ocorrencia_id,
            local_atendimento=local_atendimento,
            vitimas_atendidas=vitimas_atendidas,
            desalojados_atendidos=desalojados_atendidos,
            obitos_confirmados=obitos_confirmados,
            equipe_responsavel_id=equipe_responsavel_id,
            observacoes=observacoes,
        )
        saved = await self.atendimento_repo.save(atendimento)
        if despacho.status in {StatusDespacho.GERADO, StatusDespacho.EM_DESLOCAMENTO}:
            despacho.atualizar_status(
                StatusDespacho.CONCLUIDO, "Despacho operacional concluido com atendimento iniciado"
            )
            await self.despacho_repo.save(despacho)
        if ocorrencia.status == StatusOcorrenciaEmergencial.RECEBIDA:
            ocorrencia.atualizar_status(
                StatusOcorrenciaEmergencial.EM_ATENDIMENTO, "Atendimento iniciado para ocorrencia"
            )
            await self.ocorrencia_repo.save(ocorrencia)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="REGISTRO_ATENDIMENTO",
                entity_id=saved.id,
                citizen_id=citizen_id,
                numero_processo=saved.codigo_atendimento,
                metadata={
                    "codigo_atendimento": saved.codigo_atendimento,
                    "despacho_id": str(saved.despacho_id),
                    "status": saved.status.value,
                },
            )
        return saved

    async def finalizar_atendimento(
        self, *, atendimento_id: UUID, resumo: str | None = None, observacoes: str | None = None
    ) -> Atendimento:
        atendimento = await self.buscar_atendimento(atendimento_id)
        atendimento.finalizar(resumo=resumo, observacoes=observacoes)
        saved = await self.atendimento_repo.save(atendimento)
        ocorrencia = await self.ocorrencia_repo.get_by_id(atendimento.ocorrencia_id)
        if ocorrencia is not None and ocorrencia.status != StatusOcorrenciaEmergencial.CONCLUIDA:
            ocorrencia.atualizar_status(
                StatusOcorrenciaEmergencial.CONCLUIDA,
                "Ocorrencia concluida apos finalizacao do atendimento",
            )
            await self.ocorrencia_repo.save(ocorrencia)
        return saved

    async def buscar_atendimento(self, atendimento_id: UUID) -> Atendimento:
        atendimento = await self.atendimento_repo.get_by_id(atendimento_id)
        if atendimento is None:
            raise ValueError("Atendimento nao encontrado")
        return atendimento

    async def listar_atendimentos(
        self,
        *,
        ocorrencia_id: UUID | None = None,
        despacho_id: UUID | None = None,
        status: StatusAtendimento | None = None,
    ) -> list[Atendimento]:
        if ocorrencia_id is not None:
            return await self.atendimento_repo.list_by_ocorrencia(ocorrencia_id)
        if despacho_id is not None:
            return await self.atendimento_repo.list_by_despacho(despacho_id)
        if status is not None:
            return await self.atendimento_repo.list_by_status(status)
        return await self.atendimento_repo.list_all()

    async def atualizar_status(
        self, *, atendimento_id: UUID, status: StatusAtendimento, observacoes: str | None = None
    ) -> Atendimento:
        atendimento = await self.buscar_atendimento(atendimento_id)
        atendimento.atualizar_status(status, observacoes)
        return await self.atendimento_repo.save(atendimento)

    async def remover_atendimento(self, atendimento_id: UUID) -> None:
        deleted = await self.atendimento_repo.delete(atendimento_id)
        if not deleted:
            raise ValueError("Atendimento nao encontrado")
