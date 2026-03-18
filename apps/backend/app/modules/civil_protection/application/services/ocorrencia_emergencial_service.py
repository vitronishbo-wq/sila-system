from __future__ import annotations
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.civil_protection.domain.ports.bombeiro_repository_port import BombeiroRepositoryPort
from apps.backend.app.modules.civil_protection.domain.ports.corporacao_repository_port import CorporacaoRepositoryPort
from apps.backend.app.modules.civil_protection.domain.ports.ocorrencia_emergencial_repository_port import OcorrenciaEmergencialRepositoryPort
from apps.backend.app.modules.civil_protection.domain.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.domain.models.ocorrencia_emergencial import OcorrenciaEmergencial

class OcorrenciaEmergencialService:

    def __init__(self, *, ocorrencia_repo: OcorrenciaEmergencialRepositoryPort, corporacao_repo: CorporacaoRepositoryPort, bombeiro_repo: BombeiroRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.ocorrencia_repo = ocorrencia_repo
        self.corporacao_repo = corporacao_repo
        self.bombeiro_repo = bombeiro_repo
        self.request_service = request_service

    async def registrar_ocorrencia(self, *, corporacao_id: UUID, tipo: TipoOcorrenciaEmergencial, prioridade: PrioridadeAtendimento, data_ocorrencia: datetime, descricao: str, municipio: str, provincia: str, bombeiro_responsavel_id: UUID | None=None, endereco: str | None=None, vitimas: int=0, desalojados: int=0, obitos: int=0, observacoes: str | None=None, citizen_id: UUID | None=None) -> OcorrenciaEmergencial:
        corporacao = await self.corporacao_repo.get_by_id(corporacao_id)
        if corporacao is None:
            raise ValueError('Corporacao nao encontrada')
        if bombeiro_responsavel_id is not None:
            bombeiro = await self.bombeiro_repo.get_by_id(bombeiro_responsavel_id)
            if bombeiro is None:
                raise ValueError('Bombeiro responsavel nao encontrado')
            if bombeiro.corporacao_id != corporacao_id:
                raise ValueError('Bombeiro responsavel nao pertence a corporacao informada')
        codigo_ocorrencia = await self.ocorrencia_repo.next_codigo()
        ocorrencia = OcorrenciaEmergencial.registrar(codigo_ocorrencia=codigo_ocorrencia, corporacao_id=corporacao_id, tipo=tipo, prioridade=prioridade, data_ocorrencia=data_ocorrencia, descricao=descricao, municipio=municipio, provincia=provincia, bombeiro_responsavel_id=bombeiro_responsavel_id, endereco=endereco, vitimas=vitimas, desalojados=desalojados, obitos=obitos, observacoes=observacoes)
        saved = await self.ocorrencia_repo.save(ocorrencia)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_OCORRENCIA_EMERGENCIAL', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.codigo_ocorrencia, metadata={'codigo_ocorrencia': saved.codigo_ocorrencia, 'tipo': saved.tipo.value, 'prioridade': saved.prioridade.value, 'municipio': saved.municipio})
        return saved

    async def buscar_ocorrencia(self, ocorrencia_id: UUID) -> OcorrenciaEmergencial:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError('Ocorrencia emergencial nao encontrada')
        return ocorrencia

    async def listar_ocorrencias(self, *, corporacao_id: UUID | None=None, tipo: TipoOcorrenciaEmergencial | None=None, status: StatusOcorrenciaEmergencial | None=None) -> list[OcorrenciaEmergencial]:
        if corporacao_id is not None:
            return await self.ocorrencia_repo.list_by_corporacao(corporacao_id)
        if tipo is not None:
            return await self.ocorrencia_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.ocorrencia_repo.list_by_status(status)
        return await self.ocorrencia_repo.list_all()

    async def atualizar_status(self, *, ocorrencia_id: UUID, status: StatusOcorrenciaEmergencial, observacoes: str | None=None) -> OcorrenciaEmergencial:
        ocorrencia = await self.buscar_ocorrencia(ocorrencia_id)
        ocorrencia.atualizar_status(status, observacoes)
        return await self.ocorrencia_repo.save(ocorrencia)

    async def remover_ocorrencia(self, ocorrencia_id: UUID) -> None:
        deleted = await self.ocorrencia_repo.delete(ocorrencia_id)
        if not deleted:
            raise ValueError('Ocorrencia emergencial nao encontrada')