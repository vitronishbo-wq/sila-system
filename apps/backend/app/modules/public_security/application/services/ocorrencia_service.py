from __future__ import annotations
from datetime import datetime
from uuid import UUID
from app.modules.public_security.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from app.modules.public_security.application.ports.request_service_port import RequestServicePort
from app.modules.public_security.application.ports.unidade_policial_repository_port import UnidadePolicialRepositoryPort
from app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusOcorrencia, TipoOcorrencia
from app.modules.public_security.domain.models.ocorrencia import Ocorrencia

class OcorrenciaService:

    def __init__(self, *, ocorrencia_repo: OcorrenciaRepositoryPort, unidade_repo: UnidadePolicialRepositoryPort, policial_repo: PolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.ocorrencia_repo = ocorrencia_repo
        self.unidade_repo = unidade_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def registrar_ocorrencia(self, *, unidade_id: UUID, tipo: TipoOcorrencia, prioridade: PrioridadeOcorrencia, data_ocorrencia: datetime, descricao: str, municipio: str, provincia: str, policial_responsavel_id: UUID | None=None, endereco: str | None=None, vitimas: int=0, suspeitos: int=0, preso_em_flagrante: bool=False, observacoes: str | None=None, citizen_id: UUID | None=None) -> Ocorrencia:
        unidade = await self.unidade_repo.get_by_id(unidade_id)
        if unidade is None:
            raise ValueError('Unidade policial nao encontrada')
        if policial_responsavel_id is not None:
            policial = await self.policial_repo.get_by_id(policial_responsavel_id)
            if policial is None:
                raise ValueError('Policial responsavel nao encontrado')
            if policial.unidade_id != unidade_id:
                raise ValueError('Policial responsavel nao pertence a unidade informada')
        codigo = await self.ocorrencia_repo.next_codigo()
        ocorrencia = Ocorrencia.registrar(codigo_ocorrencia=codigo, unidade_id=unidade_id, tipo=tipo, prioridade=prioridade, data_ocorrencia=data_ocorrencia, descricao=descricao, municipio=municipio, provincia=provincia, policial_responsavel_id=policial_responsavel_id, endereco=endereco, vitimas=vitimas, suspeitos=suspeitos, preso_em_flagrante=preso_em_flagrante, observacoes=observacoes)
        saved = await self.ocorrencia_repo.save(ocorrencia)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='REGISTRO_OCORRENCIA_SEGURANCA', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.codigo_ocorrencia, metadata={'codigo_ocorrencia': saved.codigo_ocorrencia, 'tipo': saved.tipo.value, 'prioridade': saved.prioridade.value, 'unidade_id': str(saved.unidade_id)})
        return saved

    async def buscar_ocorrencia(self, ocorrencia_id: UUID) -> Ocorrencia:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError('Ocorrencia nao encontrada')
        return ocorrencia

    async def listar_ocorrencias(self, *, unidade_id: UUID | None=None, tipo: TipoOcorrencia | None=None, status: StatusOcorrencia | None=None, inicio: datetime | None=None, fim: datetime | None=None) -> list[Ocorrencia]:
        if unidade_id is not None:
            return await self.ocorrencia_repo.list_by_unidade(unidade_id)
        if tipo is not None:
            return await self.ocorrencia_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.ocorrencia_repo.list_by_status(status)
        if inicio is not None and fim is not None:
            return await self.ocorrencia_repo.list_by_periodo(inicio, fim)
        return await self.ocorrencia_repo.list_all()

    async def atualizar_status(self, *, ocorrencia_id: UUID, status: StatusOcorrencia, observacoes: str | None=None) -> Ocorrencia:
        ocorrencia = await self.buscar_ocorrencia(ocorrencia_id)
        ocorrencia.atualizar_status(status, observacoes)
        return await self.ocorrencia_repo.save(ocorrencia)

    async def remover_ocorrencia(self, ocorrencia_id: UUID) -> None:
        deleted = await self.ocorrencia_repo.delete(ocorrencia_id)
        if not deleted:
            raise ValueError('Ocorrencia nao encontrada')