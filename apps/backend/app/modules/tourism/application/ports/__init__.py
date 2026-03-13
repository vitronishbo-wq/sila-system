from __future__ import annotations
from typing import Any

class BaseRepositoryPort:

    async def save(self, entity: Any) -> Any:
        raise NotImplementedError

    async def get_by_id(self, id: Any) -> Any:
        raise NotImplementedError

    async def list(self, **filters: Any) -> list[Any]:
        raise NotImplementedError

class BaseIntegrationServicePort:

    async def request(self, **payload: Any) -> Any:
        raise NotImplementedError
from app.modules.tourism.application.ports.operador_turistico_repository_port import OperadorTuristicoRepositoryPort
from app.modules.tourism.application.ports.agencia_viagens_repository_port import AgenciaViagensRepositoryPort
from app.modules.tourism.application.ports.guia_turismo_repository_port import GuiaTurismoRepositoryPort
from app.modules.tourism.application.ports.condutor_visitantes_repository_port import CondutorVisitantesRepositoryPort
from app.modules.tourism.application.ports.hotel_repository_port import HotelRepositoryPort
from app.modules.tourism.application.ports.pousada_repository_port import PousadaRepositoryPort
from app.modules.tourism.application.ports.resort_repository_port import ResortRepositoryPort
from app.modules.tourism.application.ports.atracao_turistica_repository_port import AtracaoTuristicaRepositoryPort
from app.modules.tourism.application.ports.ponto_turistico_repository_port import PontoTuristicoRepositoryPort
from app.modules.tourism.application.ports.evento_turistico_repository_port import EventoTuristicoRepositoryPort
from app.modules.tourism.application.ports.pacote_turistico_repository_port import PacoteTuristicoRepositoryPort
from app.modules.tourism.application.ports.roteiro_repository_port import RoteiroRepositoryPort
from app.modules.tourism.application.ports.reserva_hotel_repository_port import ReservaHotelRepositoryPort
from app.modules.tourism.application.ports.reserva_pacote_repository_port import ReservaPacoteRepositoryPort
from app.modules.tourism.application.ports.avaliacao_repository_port import AvaliacaoRepositoryPort
from app.modules.tourism.application.ports.reclamacao_turismo_repository_port import ReclamacaoTurismoRepositoryPort
from app.modules.tourism.application.ports.cadastro_turista_repository_port import CadastroTuristaRepositoryPort
from app.modules.tourism.application.ports.visitante_repository_port import VisitanteRepositoryPort
from app.modules.tourism.application.ports.fluxo_turistico_repository_port import FluxoTuristicoRepositoryPort
from app.modules.tourism.application.ports.ocupacao_hoteleira_repository_port import OcupacaoHoteleiraRepositoryPort
from app.modules.tourism.application.ports.tarifa_hotel_repository_port import TarifaHotelRepositoryPort
from app.modules.tourism.application.ports.temporada_repository_port import TemporadaRepositoryPort
from app.modules.tourism.application.ports.promocao_turistica_repository_port import PromocaoTuristicaRepositoryPort
from app.modules.tourism.application.ports.licenca_turismo_repository_port import LicencaTurismoRepositoryPort
from app.modules.tourism.application.ports.cadastur_repository_port import CadasturRepositoryPort
from app.modules.tourism.application.ports.registro_guia_repository_port import RegistroGuiaRepositoryPort
from app.modules.tourism.application.ports.credencial_repository_port import CredencialRepositoryPort
from app.modules.tourism.application.ports.fiscalizacao_turismo_repository_port import FiscalizacaoTurismoRepositoryPort
from app.modules.tourism.application.ports.auto_infracao_turismo_repository_port import AutoInfracaoTurismoRepositoryPort
from app.modules.tourism.application.ports.multa_turismo_repository_port import MultaTurismoRepositoryPort
from app.modules.tourism.application.ports.classificacao_hoteleira_repository_port import ClassificacaoHoteleiraRepositoryPort
from app.modules.tourism.application.ports.certificacao_turistica_repository_port import CertificacaoTuristicaRepositoryPort
from app.modules.tourism.application.ports.estatistica_turismo_repository_port import EstatisticaTurismoRepositoryPort
from app.modules.tourism.application.ports.chegada_turistas_repository_port import ChegadaTuristasRepositoryPort
from app.modules.tourism.application.ports.receita_turistica_repository_port import ReceitaTuristicaRepositoryPort
from app.modules.tourism.application.ports.citizen_service_port import CitizenServicePort
from app.modules.tourism.application.ports.request_service_port import RequestServicePort
from app.modules.tourism.application.ports.transportes_logistica_service_port import TransportesLogisticaServicePort
from app.modules.tourism.application.ports.ambiente_service_port import AmbienteServicePort
from app.modules.tourism.application.ports.cultura_service_port import CulturaServicePort
from app.modules.tourism.application.ports.comercio_servicos_service_port import ComercioServicosServicePort
from app.modules.tourism.application.ports.geosampa_service_port import GeosampaServicePort
__all__ = ['BaseRepositoryPort', 'BaseIntegrationServicePort', 'OperadorTuristicoRepositoryPort', 'AgenciaViagensRepositoryPort', 'GuiaTurismoRepositoryPort', 'CondutorVisitantesRepositoryPort', 'HotelRepositoryPort', 'PousadaRepositoryPort', 'ResortRepositoryPort', 'AtracaoTuristicaRepositoryPort', 'PontoTuristicoRepositoryPort', 'EventoTuristicoRepositoryPort', 'PacoteTuristicoRepositoryPort', 'RoteiroRepositoryPort', 'ReservaHotelRepositoryPort', 'ReservaPacoteRepositoryPort', 'AvaliacaoRepositoryPort', 'ReclamacaoTurismoRepositoryPort', 'CadastroTuristaRepositoryPort', 'VisitanteRepositoryPort', 'FluxoTuristicoRepositoryPort', 'OcupacaoHoteleiraRepositoryPort', 'TarifaHotelRepositoryPort', 'TemporadaRepositoryPort', 'PromocaoTuristicaRepositoryPort', 'LicencaTurismoRepositoryPort', 'CadasturRepositoryPort', 'RegistroGuiaRepositoryPort', 'CredencialRepositoryPort', 'FiscalizacaoTurismoRepositoryPort', 'AutoInfracaoTurismoRepositoryPort', 'MultaTurismoRepositoryPort', 'ClassificacaoHoteleiraRepositoryPort', 'CertificacaoTuristicaRepositoryPort', 'EstatisticaTurismoRepositoryPort', 'ChegadaTuristasRepositoryPort', 'ReceitaTuristicaRepositoryPort', 'CitizenServicePort', 'RequestServicePort', 'TransportesLogisticaServicePort', 'AmbienteServicePort', 'CulturaServicePort', 'ComercioServicosServicePort', 'GeosampaServicePort']
