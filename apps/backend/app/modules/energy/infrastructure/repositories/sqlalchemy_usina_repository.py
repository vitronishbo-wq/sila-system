from __future__ import annotations
from copy import deepcopy
from uuid import UUID
from app.modules.energy.application.ports import UsinaRepositoryPort
from app.modules.energy.domain.enums import FonteEnergia, StatusUsina
from app.modules.energy.domain.models import Usina
from app.modules.energy.infrastructure.models import UsinaModel

class SQLAlchemyUsinaRepository(UsinaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, UsinaModel] = {}
        self._index_codigo: dict[str, UUID] = {}

    async def save(self, usina: Usina) -> Usina:
        model = self._to_model(usina)
        self._items[model.id] = model
        self._index_codigo[model.codigo_aneel] = model.id
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Usina | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def get_by_codigo_aneel(self, codigo_aneel: str) -> Usina | None:
        id = self._index_codigo.get(codigo_aneel.strip().upper())
        if not id:
            return None
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusUsina | None=None, fonte: FonteEnergia | None=None, provincia: str | None=None) -> list[Usina]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if fonte:
            values = [item for item in values if item.fonte == fonte]
        if provincia:
            uf = provincia.strip().lower()
            values = [item for item in values if item.provincia.lower() == uf]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    @staticmethod
    def _to_model(usina: Usina) -> UsinaModel:
        return UsinaModel(id=usina.id, codigo_aneel=usina.codigo_aneel, nome=usina.nome, fonte=usina.fonte, tipo=usina.tipo, status=usina.status, potencia_instalada_mw=usina.potencia_instalada_mw, proprietario_id=usina.proprietario_id, proprietario_tipo=usina.proprietario_tipo, municipio=usina.municipio, provincia=usina.provincia, potencia_fiscalizada_mw=usina.potencia_fiscalizada_mw, garantia_fisica_mw=usina.garantia_fisica_mw, energia_assegurada_mwm=usina.energia_assegurada_mwm, operador_id=usina.operador_id, concessionaria_id=usina.concessionaria_id, outorga_id=usina.outorga_id, licenca_operacao_id=usina.licenca_operacao_id, data_autorizacao=usina.data_autorizacao, data_inicio_construcao=usina.data_inicio_construcao, data_entrada_operacao=usina.data_entrada_operacao, data_validade_outorga=usina.data_validade_outorga, observacoes=usina.observacoes)

    @staticmethod
    def _to_domain(model: UsinaModel) -> Usina:
        return Usina(id=model.id, codigo_aneel=model.codigo_aneel, nome=model.nome, fonte=model.fonte, tipo=model.tipo, status=model.status, potencia_instalada_mw=model.potencia_instalada_mw, proprietario_id=model.proprietario_id, proprietario_tipo=model.proprietario_tipo, municipio=model.municipio, provincia=model.provincia, potencia_fiscalizada_mw=model.potencia_fiscalizada_mw, garantia_fisica_mw=model.garantia_fisica_mw, energia_assegurada_mwm=model.energia_assegurada_mwm, operador_id=model.operador_id, concessionaria_id=model.concessionaria_id, outorga_id=model.outorga_id, licenca_operacao_id=model.licenca_operacao_id, data_autorizacao=model.data_autorizacao, data_inicio_construcao=model.data_inicio_construcao, data_entrada_operacao=model.data_entrada_operacao, data_validade_outorga=model.data_validade_outorga, bacia_hidrografica=None, rio=None, area_reservatorio_km2=None, volume_reservatorio_hm3=None, area_ocupada_ha=None, numero_aerogeradores=None, altura_torre_m=None, diametro_rotor_m=None, potencia_por_aerogerador_mw=None, numero_paineis=None, area_paineis_m2=None, tecnologia=None, combustivel=None, consumo_combustivel=None, unidade_consumo=None, rendimento=None, coordenadas_lat=None, coordenadas_long=None, observacoes=deepcopy(model.observacoes))
