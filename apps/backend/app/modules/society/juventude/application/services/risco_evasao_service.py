from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.educacao_service_port import EducacaoServicePort
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.juventude.application.ports.risco_evasao_repository_port import RiscoEvasaoRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import RiscoSocial
from apps.backend.app.modules.society.juventude.domain.models.risco_evasao import RiscoEvasao

class RiscoEvasaoService:

    def __init__(self, *, risco_repo: RiscoEvasaoRepositoryPort, jovem_repo: JovemRepositoryPort, educacao_service: EducacaoServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.risco_repo = risco_repo
        self.jovem_repo = jovem_repo
        self.educacao_service = educacao_service
        self.request_service = request_service

    async def avaliar_risco(self, *, jovem_id: UUID, observacoes: str | None=None) -> RiscoEvasao:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError('Jovem nao encontrado para avaliacao de risco')
        matricula_ativa = False
        if jovem.citizen_id is not None and self.educacao_service is not None:
            matricula_ativa = await self.educacao_service.has_matricula_ativa(jovem.citizen_id)
        codigo = await self.risco_repo.next_codigo()
        risco = RiscoEvasao.avaliar(codigo_risco=codigo, jovem_id=jovem.id, citizen_id=jovem.citizen_id, matricula_ativa=matricula_ativa, situacao_ocupacional=jovem.situacao_ocupacional, vulnerabilidades=jovem.vulnerabilidades, observacoes=observacoes)
        saved = await self.risco_repo.save(risco)
        if self.request_service is not None and saved.citizen_id is not None and (saved.nivel_risco in {RiscoSocial.ALTO, RiscoSocial.CRITICO}):
            await self.request_service.create_request(request_type='RISCO_EVASAO_JUVENTUDE', entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.codigo_risco, metadata={'jovem_id': str(saved.jovem_id), 'pontuacao': saved.pontuacao, 'nivel_risco': saved.nivel_risco.value, 'fatores': saved.fatores})
        return saved

    async def buscar_risco(self, risco_id: UUID) -> RiscoEvasao:
        item = await self.risco_repo.get_by_id(risco_id)
        if item is None:
            raise ValueError('Avaliacao de risco nao encontrada')
        return item

    async def buscar_risco_ativo_por_jovem(self, jovem_id: UUID) -> RiscoEvasao:
        item = await self.risco_repo.get_ativo_by_jovem(jovem_id)
        if item is None:
            raise ValueError('Nao existe risco ativo para o jovem informado')
        return item

    async def listar_riscos(self, *, nivel: RiscoSocial | None=None) -> list[RiscoEvasao]:
        if nivel is not None:
            return await self.risco_repo.list_by_nivel(nivel)
        return await self.risco_repo.list_all()