from __future__ import annotations
from uuid import UUID
from app.modules.economy.trade.services.application.ports import EstabelecimentoComercialRepositoryPort
from app.modules.economy.trade.services.domain.enums import RamoComercial, StatusComercial
from app.modules.economy.trade.services.domain.models import EstabelecimentoComercial
from app.modules.economy.trade.services.infrastructure.models import EstabelecimentoComercialModel

class SQLAlchemyEstabelecimentoComercialRepository(EstabelecimentoComercialRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, EstabelecimentoComercialModel] = {}

    async def save(self, item: EstabelecimentoComercial) -> EstabelecimentoComercial:
        model = EstabelecimentoComercialModel(id=item.id, cnpj=item.cnpj, razao_social=item.razao_social, tipo=item.tipo, ramo=item.ramo, porte=item.porte, regime_tributario=item.regime_tributario, cnae_principal=item.cnae_principal, data_abertura=item.data_abertura, endereco=item.endereco, numero=item.numero, bairro=item.bairro, municipio=item.municipio, provincia=item.provincia, cep=item.cep, status=item.status, inscricao_estadual=item.inscricao_estadual, inscricao_municipal=item.inscricao_municipal, nome_fantasia=item.nome_fantasia, cnaes_secundarios=item.cnaes_secundarios, data_inicio_atividades=item.data_inicio_atividades, data_encerramento=item.data_encerramento, complemento=item.complemento, coordenadas_lat=item.coordenadas_lat, coordenadas_long=item.coordenadas_long, telefone=item.telefone, celular=item.celular, email=item.email, site=item.site, redes_sociais=item.redes_sociais, horario_funcionamento=item.horario_funcionamento, dias_funcionamento=item.dias_funcionamento, area_m2=item.area_m2, numero_funcionarios=item.numero_funcionarios, faturamento_medio_mensal=item.faturamento_medio_mensal, matriz_id=item.matriz_id, franquia_id=item.franquia_id, grupo_economico_id=item.grupo_economico_id, proprietario_id=item.proprietario_id, proprietario_tipo=item.proprietario_tipo, alvara_id=item.alvara_id, licenca_sanitaria_id=item.licenca_sanitaria_id, licenca_ambiental_id=item.licenca_ambiental_id, certificacoes=item.certificacoes, created_at=item.created_at, updated_at=item.updated_at, audit_log=list(item.audit_log), observacoes=item.observacoes)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> EstabelecimentoComercial | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> EstabelecimentoComercial | None:
        lookup = cnpj.strip()
        for model in self._items.values():
            if model.cnpj == lookup:
                return self._to_domain(model)
        return None

    async def list(self, *, status: StatusComercial | None=None, ramo: RamoComercial | None=None, municipio: str | None=None) -> list[EstabelecimentoComercial]:
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
    def _to_domain(model: EstabelecimentoComercialModel) -> EstabelecimentoComercial:
        return EstabelecimentoComercial(id=model.id, cnpj=model.cnpj, razao_social=model.razao_social, tipo=model.tipo, ramo=model.ramo, porte=model.porte, regime_tributario=model.regime_tributario, cnae_principal=model.cnae_principal, data_abertura=model.data_abertura, endereco=model.endereco, numero=model.numero, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, cep=model.cep, status=model.status, inscricao_estadual=model.inscricao_estadual, inscricao_municipal=model.inscricao_municipal, nome_fantasia=model.nome_fantasia, cnaes_secundarios=model.cnaes_secundarios, data_inicio_atividades=model.data_inicio_atividades, data_encerramento=model.data_encerramento, complemento=model.complemento, coordenadas_lat=model.coordenadas_lat, coordenadas_long=model.coordenadas_long, telefone=model.telefone, celular=model.celular, email=model.email, site=model.site, redes_sociais=model.redes_sociais, horario_funcionamento=model.horario_funcionamento, dias_funcionamento=model.dias_funcionamento, area_m2=model.area_m2, numero_funcionarios=model.numero_funcionarios, faturamento_medio_mensal=model.faturamento_medio_mensal, matriz_id=model.matriz_id, franquia_id=model.franquia_id, grupo_economico_id=model.grupo_economico_id, proprietario_id=model.proprietario_id, proprietario_tipo=model.proprietario_tipo, alvara_id=model.alvara_id, licenca_sanitaria_id=model.licenca_sanitaria_id, licenca_ambiental_id=model.licenca_ambiental_id, certificacoes=model.certificacoes, created_at=model.created_at, updated_at=model.updated_at, audit_log=list(model.audit_log), observacoes=model.observacoes)