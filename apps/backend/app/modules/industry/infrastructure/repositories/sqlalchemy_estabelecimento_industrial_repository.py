from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.industry.application.ports import EstabelecimentoIndustrialRepositoryPort
from apps.backend.app.modules.industry.domain.enums import RamoIndustrial, StatusEstabelecimento
from apps.backend.app.modules.industry.domain.models import EstabelecimentoIndustrial
from apps.backend.app.modules.industry.infrastructure.models import EstabelecimentoIndustrialModel

class SQLAlchemyEstabelecimentoIndustrialRepository(EstabelecimentoIndustrialRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, EstabelecimentoIndustrialModel] = {}

    async def save(self, item: EstabelecimentoIndustrial) -> EstabelecimentoIndustrial:
        model = EstabelecimentoIndustrialModel(id=item.id, cnpj=item.cnpj, razao_social=item.razao_social, ramo=item.ramo, porte=item.porte, tipo=item.tipo, cnae_principal=item.cnae_principal, data_abertura=item.data_abertura, endereco=item.endereco, bairro=item.bairro, municipio=item.municipio, provincia=item.provincia, status=item.status, nome_fantasia=item.nome_fantasia, inscricao_estadual=item.inscricao_estadual, inscricao_municipal=item.inscricao_municipal, telefone=item.telefone, email=item.email, data_inicio_atividades=item.data_inicio_atividades, data_encerramento=item.data_encerramento, licenca_operacao_id=item.licenca_operacao_id, licenca_ambiental_id=item.licenca_ambiental_id, alvara_id=item.alvara_id, created_at=item.created_at, updated_at=item.updated_at, audit_log=list(item.audit_log), observacoes=item.observacoes)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> EstabelecimentoIndustrial | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> EstabelecimentoIndustrial | None:
        lookup = cnpj.strip()
        for model in self._items.values():
            if model.cnpj == lookup:
                return self._to_domain(model)
        return None

    async def list(self, *, status: StatusEstabelecimento | None=None, ramo: RamoIndustrial | None=None, municipio: str | None=None) -> list[EstabelecimentoIndustrial]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if ramo:
            values = [item for item in values if item.ramo == ramo]
        if municipio:
            values = [item for item in values if item.municipio.lower() == municipio.lower()]
        values.sort(key=lambda item: item.razao_social.lower())
        return [self._to_domain(item) for item in values]

    @staticmethod
    def _to_domain(model: EstabelecimentoIndustrialModel) -> EstabelecimentoIndustrial:
        return EstabelecimentoIndustrial(id=model.id, cnpj=model.cnpj, razao_social=model.razao_social, ramo=model.ramo, porte=model.porte, tipo=model.tipo, cnae_principal=model.cnae_principal, data_abertura=model.data_abertura, endereco=model.endereco, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, status=model.status, nome_fantasia=model.nome_fantasia, inscricao_estadual=model.inscricao_estadual, inscricao_municipal=model.inscricao_municipal, telefone=model.telefone, email=model.email, data_inicio_atividades=model.data_inicio_atividades, data_encerramento=model.data_encerramento, licenca_operacao_id=model.licenca_operacao_id, licenca_ambiental_id=model.licenca_ambiental_id, alvara_id=model.alvara_id, created_at=model.created_at, updated_at=model.updated_at, audit_log=list(model.audit_log), observacoes=model.observacoes)
