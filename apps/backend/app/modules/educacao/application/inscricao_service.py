from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.ports import EscolaRepositoryPort, InscricaoRepositoryPort
from apps.backend.app.modules.educacao.domain.enums import TipoInscricao
from apps.backend.app.modules.educacao.domain.models.inscricao_basica import InscricaoBasica
from apps.backend.app.modules.educacao.domain.models.inscricao_secundaria import InscricaoSecundaria
from apps.backend.app.modules.educacao.domain.models.inscricao_superior import InscricaoSuperior
from apps.backend.app.modules.educacao.domain.models.inscricao_tecnico import InscricaoTecnico
from apps.backend.app.modules.educacao.exceptions import CitizenNotFoundError, EscolaNotFoundError

class InscricaoService:

    def __init__(self, inscricao_repo: InscricaoRepositoryPort, escola_repo: EscolaRepositoryPort, citizen_repo: CitizenRepositoryPort, request_service: ServiceRequestLifecycleBridge):
        self.inscricao_repo = inscricao_repo
        self.escola_repo = escola_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def criar_inscricao_basica(self, *, citizen_id: UUID, escola_id: UUID, observacoes: Optional[str]=None):
        return await self._criar_inscricao(tipo=TipoInscricao.BASICA, citizen_id=citizen_id, escola_id=escola_id, observacoes=observacoes)

    async def criar_inscricao_secundaria(self, *, citizen_id: UUID, escola_id: UUID, observacoes: Optional[str]=None):
        return await self._criar_inscricao(tipo=TipoInscricao.SECUNDARIA, citizen_id=citizen_id, escola_id=escola_id, observacoes=observacoes)

    async def criar_inscricao_superior(self, *, citizen_id: UUID, escola_id: UUID, observacoes: Optional[str]=None):
        return await self._criar_inscricao(tipo=TipoInscricao.SUPERIOR, citizen_id=citizen_id, escola_id=escola_id, observacoes=observacoes)

    async def criar_inscricao_tecnico(self, *, citizen_id: UUID, escola_id: UUID, observacoes: Optional[str]=None):
        return await self._criar_inscricao(tipo=TipoInscricao.TECNICO, citizen_id=citizen_id, escola_id=escola_id, observacoes=observacoes)

    async def confirmar_inscricao(self, inscricao_id: UUID, actor_id: UUID):
        inscricao = await self.inscricao_repo.get_by_id(inscricao_id)
        if not inscricao:
            raise ValueError('Inscricao nao encontrada')
        inscricao.confirmar()
        updated = await self.inscricao_repo.save(inscricao)
        await self.request_service.mark_education_request_completed(entity_id=updated.id, actor_id=actor_id, metadata={'status': 'confirmada', 'tipo': updated.tipo.value})
        return updated

    async def cancelar_inscricao(self, inscricao_id: UUID, actor_id: UUID, motivo: str):
        inscricao = await self.inscricao_repo.get_by_id(inscricao_id)
        if not inscricao:
            raise ValueError('Inscricao nao encontrada')
        inscricao.cancelar(motivo)
        updated = await self.inscricao_repo.save(inscricao)
        await self.request_service.mark_education_request_completed(entity_id=updated.id, actor_id=actor_id, metadata={'status': 'cancelada', 'motivo': motivo, 'tipo': updated.tipo.value})
        return updated

    async def listar_por_cidadao(self, citizen_id: UUID, tipo: TipoInscricao | None=None):
        return await self.inscricao_repo.get_by_citizen(citizen_id, tipo)

    async def _criar_inscricao(self, *, tipo: TipoInscricao, citizen_id: UUID, escola_id: UUID, observacoes: Optional[str]):
        citizen = await self.citizen_repo.get_by_id(citizen_id)
        if not citizen:
            raise CitizenNotFoundError(f'Cidadao {citizen_id} nao encontrado')
        escola = await self.escola_repo.get_by_id(escola_id)
        if not escola:
            raise EscolaNotFoundError(f'Escola {escola_id} nao encontrada')
        exists = await self.inscricao_repo.exists_active_for_citizen(citizen_id, tipo)
        if exists:
            raise ValueError('Cidadao ja possui inscricao pendente/confirmada para este tipo')
        numero = await self.inscricao_repo.next_numero_processo(date.today().year, tipo)
        if tipo == TipoInscricao.BASICA:
            inscricao = InscricaoBasica(id=uuid4(), numero_processo=numero, citizen_id=citizen_id, escola_id=escola_id, data_inscricao=date.today(), observacoes=observacoes)
        elif tipo == TipoInscricao.SECUNDARIA:
            inscricao = InscricaoSecundaria(id=uuid4(), numero_processo=numero, citizen_id=citizen_id, escola_id=escola_id, data_inscricao=date.today(), observacoes=observacoes)
        elif tipo == TipoInscricao.SUPERIOR:
            inscricao = InscricaoSuperior(id=uuid4(), numero_processo=numero, citizen_id=citizen_id, escola_id=escola_id, data_inscricao=date.today(), observacoes=observacoes)
        else:
            inscricao = InscricaoTecnico(id=uuid4(), numero_processo=numero, citizen_id=citizen_id, escola_id=escola_id, data_inscricao=date.today(), observacoes=observacoes)
        saved = await self.inscricao_repo.save(inscricao)
        await self.request_service.create_education_request(entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.numero_processo, escola_nome=escola.nome, ano_letivo=str(date.today().year))
        return saved