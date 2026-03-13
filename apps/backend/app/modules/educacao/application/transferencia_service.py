from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import EscolaRepositoryPort, MatriculaRepositoryPort, TransferenciaRepositoryPort, TurmaRepositoryPort
from app.modules.educacao.domain.enums import StatusFluxo
from app.modules.educacao.domain.models import Matricula, StatusMatricula
from app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from app.modules.educacao.exceptions import CitizenNotFoundError, EscolaNotFoundError, InvalidMatriculaStateError, MatriculaNotFoundError, TransferenciaDuplicadaError, TransferenciaEstadoInvalidoError, TransferenciaNotFoundError, TurmaNotFoundError, TurmaSemVagasError

class TransferenciaService:

    def __init__(self, repository: TransferenciaRepositoryPort, matricula_repo: MatriculaRepositoryPort, escola_repo: EscolaRepositoryPort, turma_repo: TurmaRepositoryPort, citizen_repo: CitizenRepositoryPort | None=None, request_service: ServiceRequestLifecycleBridge | None=None):
        self.repository = repository
        self.matricula_repo = matricula_repo
        self.escola_repo = escola_repo
        self.turma_repo = turma_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service
        self.process_prefix = 'TRF'
        self.service_type = 'transferencia'

    async def solicitar_transferencia(self, *, matricula_id: UUID, escola_destino_id: UUID, turma_destino_id: UUID, motivo: str, observacoes: Optional[str]=None) -> WorkflowRecord:
        matricula = await self.matricula_repo.get_by_id(matricula_id)
        if not matricula:
            raise MatriculaNotFoundError('Matricula nao encontrada')
        if matricula.status != StatusMatricula.ATIVA:
            raise InvalidMatriculaStateError('Apenas matriculas ativas podem ser transferidas')
        if self.citizen_repo is not None:
            citizen = await self.citizen_repo.get_by_id(matricula.citizen_id)
            if not citizen:
                raise CitizenNotFoundError(f'Cidadao {matricula.citizen_id} nao encontrado')
        escola_destino = await self.escola_repo.get_by_id(escola_destino_id)
        if not escola_destino:
            raise EscolaNotFoundError(f'Escola destino {escola_destino_id} nao encontrada')
        turma_destino = await self.turma_repo.get_by_id(turma_destino_id)
        self._validar_turma_destino(turma_destino=turma_destino, turma_destino_id=turma_destino_id, escola_destino_id=escola_destino_id, ano_letivo_id=matricula.ano_letivo_id)
        ocupacao_turma = await self.turma_repo.count_matriculas_ativas(turma_destino_id, matricula.ano_letivo_id)
        if ocupacao_turma >= turma_destino.capacidade:
            raise TurmaSemVagasError('Turma destino sem vagas disponiveis')
        transferencia_ativa = await self.repository.get_active_by_matricula(matricula_id)
        if transferencia_ativa is not None:
            raise TransferenciaDuplicadaError('Ja existe solicitacao ativa de transferencia para esta matricula')
        numero = await self.repository.next_numero_processo(date.today().year, self.service_type, self.process_prefix)
        record = WorkflowRecord(id=uuid4(), numero_processo=numero, service_type=self.service_type, citizen_id=matricula.citizen_id, instituicao_id=escola_destino_id, data_registo=date.today(), status=StatusFluxo.EM_ANALISE, observacoes=observacoes, metadata={'matricula_origem_id': str(matricula.id), 'escola_origem_id': str(matricula.escola_id), 'turma_origem_id': str(matricula.turma_id), 'escola_destino_id': str(escola_destino_id), 'turma_destino_id': str(turma_destino_id), 'ano_letivo_id': str(matricula.ano_letivo_id), 'motivo': motivo.strip()})
        saved = await self.repository.save(record)
        if self.request_service is not None:
            await self.request_service.create_education_request(entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.numero_processo, escola_nome=escola_destino.nome, ano_letivo=str(matricula.ano_letivo_id))
        return saved

    async def aprovar_transferencia(self, *, transferencia_id: UUID, actor_id: UUID, resumo: Optional[str]=None) -> WorkflowRecord:
        transferencia = await self.repository.get_by_id(transferencia_id)
        if not transferencia:
            raise TransferenciaNotFoundError('Transferencia nao encontrada')
        self._validar_estado_processavel(transferencia.status)
        metadata = dict(transferencia.metadata or {})
        matricula_origem_id = self._metadata_uuid(metadata, 'matricula_origem_id')
        escola_destino_id = self._metadata_uuid(metadata, 'escola_destino_id')
        turma_destino_id = self._metadata_uuid(metadata, 'turma_destino_id')
        matricula_origem = await self.matricula_repo.get_by_id(matricula_origem_id)
        if not matricula_origem:
            raise MatriculaNotFoundError('Matricula de origem nao encontrada')
        if matricula_origem.status != StatusMatricula.ATIVA:
            raise InvalidMatriculaStateError('Matricula de origem precisa estar ativa para concluir a transferencia')
        turma_destino = await self.turma_repo.get_by_id(turma_destino_id)
        self._validar_turma_destino(turma_destino=turma_destino, turma_destino_id=turma_destino_id, escola_destino_id=escola_destino_id, ano_letivo_id=matricula_origem.ano_letivo_id)
        ocupacao_turma = await self.turma_repo.count_matriculas_ativas(turma_destino_id, matricula_origem.ano_letivo_id)
        if ocupacao_turma >= turma_destino.capacidade:
            raise TurmaSemVagasError('Turma destino sem vagas disponiveis')
        matricula_origem.transferir()
        matricula_origem.observacoes = f'Transferida pelo processo {transferencia.numero_processo} em {date.today().isoformat()}'
        await self.matricula_repo.save(matricula_origem)
        numero_nova_matricula = await self.matricula_repo.next_numero_processo(date.today().year, escola_destino_id)
        nova_matricula = Matricula(id=uuid4(), numero_processo=numero_nova_matricula, citizen_id=matricula_origem.citizen_id, escola_id=escola_destino_id, turma_id=turma_destino_id, ano_letivo_id=matricula_origem.ano_letivo_id, data_matricula=date.today(), status=StatusMatricula.ATIVA, observacoes=f'Matricula criada por transferencia {transferencia.numero_processo}')
        saved_nova_matricula = await self.matricula_repo.save(nova_matricula)
        transferencia.status = StatusFluxo.APROVADA
        transferencia.observacoes = resumo or transferencia.observacoes
        metadata['nova_matricula_id'] = str(saved_nova_matricula.id)
        metadata['data_aprovacao'] = date.today().isoformat()
        metadata['aprovado_por'] = str(actor_id)
        transferencia.metadata = metadata
        updated = await self.repository.save(transferencia)
        if self.request_service is not None:
            await self.request_service.mark_education_request_completed(entity_id=updated.id, actor_id=actor_id, metadata={'status': 'aprovada', 'nova_matricula_id': str(saved_nova_matricula.id)})
        return updated

    async def rejeitar_transferencia(self, *, transferencia_id: UUID, actor_id: UUID, motivo: str) -> WorkflowRecord:
        transferencia = await self.repository.get_by_id(transferencia_id)
        if not transferencia:
            raise TransferenciaNotFoundError('Transferencia nao encontrada')
        self._validar_estado_processavel(transferencia.status)
        transferencia.status = StatusFluxo.REJEITADA
        transferencia.observacoes = motivo.strip()
        metadata = dict(transferencia.metadata or {})
        metadata['data_rejeicao'] = date.today().isoformat()
        metadata['rejeitado_por'] = str(actor_id)
        transferencia.metadata = metadata
        updated = await self.repository.save(transferencia)
        if self.request_service is not None:
            await self.request_service.mark_education_request_completed(entity_id=updated.id, actor_id=actor_id, metadata={'status': 'rejeitada', 'motivo': motivo.strip()})
        return updated

    async def get_record(self, transferencia_id: UUID) -> WorkflowRecord | None:
        return await self.repository.get_by_id(transferencia_id)

    async def list_records(self, citizen_id: UUID) -> list[WorkflowRecord]:
        return await self.repository.list_by_citizen(citizen_id, self.service_type)

    @staticmethod
    def _metadata_uuid(metadata: dict, key: str) -> UUID:
        value = metadata.get(key)
        if not value:
            raise TransferenciaEstadoInvalidoError(f'Transferencia sem metadado obrigatorio: {key}')
        return UUID(str(value))

    @staticmethod
    def _validar_estado_processavel(status: StatusFluxo) -> None:
        if status in {StatusFluxo.REJEITADA, StatusFluxo.CANCELADA, StatusFluxo.APROVADA}:
            raise TransferenciaEstadoInvalidoError(f'Transferencia ja finalizada com status {status.value}')

    @staticmethod
    def _validar_turma_destino(*, turma_destino, turma_destino_id: UUID, escola_destino_id: UUID, ano_letivo_id: UUID) -> None:
        if not turma_destino:
            raise TurmaNotFoundError(f'Turma destino {turma_destino_id} nao encontrada')
        if not turma_destino.ativa:
            raise InvalidMatriculaStateError('Turma destino esta inativa')
        if turma_destino.escola_id != escola_destino_id:
            raise InvalidMatriculaStateError('Turma destino nao pertence a escola destino')
        if turma_destino.ano_letivo_id != ano_letivo_id:
            raise InvalidMatriculaStateError('Turma destino nao pertence ao mesmo ano letivo')