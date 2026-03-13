from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.society.emprego.application.ports import CandidatoRepositoryPort, CitizenServicePort, RequestServicePort
from apps.backend.app.modules.society.emprego.domain.enums import Escolaridade, SituacaoProfissional, StatusCandidato
from apps.backend.app.modules.society.emprego.domain.models.candidato import Candidato
from apps.backend.app.modules.society.emprego.exceptions import CandidatoAlreadyExistsError, CandidatoNotFoundError, CitizenNotFoundError

class CandidatoService:

    def __init__(self, *, candidato_repo: CandidatoRepositoryPort, citizen_repo: CitizenServicePort, request_service: RequestServicePort):
        self.candidato_repo = candidato_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def registrar_candidato(self, *, citizen_id: UUID, escolaridade: Escolaridade, situacao: SituacaoProfissional, areas_interesse: list[str]) -> Candidato:
        citizen = await self.citizen_repo.get_citizen(citizen_id)
        if not citizen:
            raise CitizenNotFoundError(f'Cidadao {citizen_id} nao encontrado')
        existente = await self.candidato_repo.get_by_citizen(citizen_id)
        if existente and existente.status == StatusCandidato.ATIVO:
            raise CandidatoAlreadyExistsError('Cidadao ja possui cadastro ativo')
        numero = await self.candidato_repo.next_numero_processo(date.today().year)
        candidato = Candidato.criar(citizen_id=citizen_id, escolaridade=escolaridade, situacao=situacao, areas_interesse=areas_interesse, numero_processo=numero)
        saved = await self.candidato_repo.save(candidato)
        await self.request_service.create_request(request_type='registro_candidato_emprego', entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.numero_processo, metadata={'escolaridade': saved.escolaridade.value, 'situacao': saved.situacao.value, 'areas_interesse': saved.areas_interesse})
        return saved

    async def obter_por_id(self, candidato_id: UUID) -> Optional[Candidato]:
        return await self.candidato_repo.get_by_id(candidato_id)

    async def buscar_candidatos(self, *, escolaridade: Optional[Escolaridade]=None, situacao: Optional[SituacaoProfissional]=None, area: Optional[str]=None) -> list[Candidato]:
        return await self.candidato_repo.list_by_filtros(escolaridade=escolaridade, situacao=situacao, area_interesse=area)

    async def desativar_candidato(self, *, candidato_id: UUID, motivo: str, actor_id: UUID) -> Candidato:
        candidato = await self.candidato_repo.get_by_id(candidato_id)
        if not candidato:
            raise CandidatoNotFoundError('Candidato nao encontrado')
        candidato.desativar(motivo)
        updated = await self.candidato_repo.save(candidato)
        await self.request_service.complete_request(entity_id=updated.id, actor_id=actor_id, metadata={'status': updated.status.value, 'motivo': motivo})
        return updated