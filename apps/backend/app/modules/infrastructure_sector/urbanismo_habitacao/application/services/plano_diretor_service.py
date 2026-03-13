from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.plano_diretor_repository_port import PlanoDiretorRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusPlanoDiretor, TipoPlanoDiretor
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.plano_diretor import PlanoDiretor
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import PlanoDiretorAlreadyExistsError, PlanoDiretorNotFoundError

class PlanoDiretorService:

    def __init__(self, *, plano_diretor_repo: PlanoDiretorRepositoryPort) -> None:
        self._plano_diretor_repo = plano_diretor_repo

    async def criar(self, *, nome: str, tipo: TipoPlanoDiretor, provincia: str, ano_elaboracao: int, orgao_responsavel_id: UUID, municipio: str | None=None, codigo_plano: str | None=None) -> PlanoDiretor:
        codigo = codigo_plano or await self._plano_diretor_repo.next_codigo()
        existente = await self._plano_diretor_repo.get_by_codigo(codigo)
        if existente:
            raise PlanoDiretorAlreadyExistsError('Ja existe plano diretor com este codigo')
        item = PlanoDiretor.criar(codigo_plano=codigo, nome=nome, tipo=tipo, provincia=provincia, ano_elaboracao=ano_elaboracao, orgao_responsavel_id=orgao_responsavel_id, municipio=municipio)
        return await self._plano_diretor_repo.save(item)

    async def iniciar_consulta_publica(self, codigo_plano: str) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.iniciar_consulta_publica()
        return await self._plano_diretor_repo.save(item)

    async def realizar_audiencia_publica(self, codigo_plano: str, *, participantes: int) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.realizar_audiencia_publica(participantes)
        return await self._plano_diretor_repo.save(item)

    async def aprovar_camara(self, codigo_plano: str, *, lei_aprovacao: str, ano_aprovacao: int) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.aprovar_camara(lei=lei_aprovacao, ano=ano_aprovacao)
        return await self._plano_diretor_repo.save(item)

    async def aprovar_prefeitura(self, codigo_plano: str) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.aprovar_prefeitura()
        return await self._plano_diretor_repo.save(item)

    async def sancionar(self, codigo_plano: str, *, data_publicacao: date) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.sancionar(data_publicacao=data_publicacao)
        return await self._plano_diretor_repo.save(item)

    async def publicar(self, codigo_plano: str) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.publicar()
        return await self._plano_diretor_repo.save(item)

    async def definir_validade(self, codigo_plano: str, *, data_inicio: date, data_fim: date) -> PlanoDiretor:
        item = await self._obter_ou_erro(codigo_plano)
        item.definir_validade(data_inicio=data_inicio, data_fim=data_fim)
        return await self._plano_diretor_repo.save(item)

    async def obter_por_codigo(self, codigo_plano: str) -> PlanoDiretor:
        return await self._obter_ou_erro(codigo_plano)

    async def listar(self, *, status: StatusPlanoDiretor | None=None, tipo: TipoPlanoDiretor | None=None, provincia: str | None=None) -> list[PlanoDiretor]:
        return await self._plano_diretor_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_plano: str) -> PlanoDiretor:
        item = await self._plano_diretor_repo.get_by_codigo(codigo_plano)
        if not item:
            raise PlanoDiretorNotFoundError('Plano diretor nao encontrado')
        return item