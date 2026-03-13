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
from apps.backend.app.modules.tourism.application.ports.operador_turistico_repository_port import OperadorTuristicoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.agencia_viagens_repository_port import AgenciaViagensRepositoryPort
from apps.backend.app.modules.tourism.application.ports.guia_turismo_repository_port import GuiaTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.condutor_visitantes_repository_port import CondutorVisitantesRepositoryPort
from apps.backend.app.modules.tourism.application.ports.hotel_repository_port import HotelRepositoryPort
from apps.backend.app.modules.tourism.application.ports.pousada_repository_port import PousadaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.resort_repository_port import ResortRepositoryPort
from apps.backend.app.modules.tourism.application.ports.atracao_turistica_repository_port import AtracaoTuristicaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.ponto_turistico_repository_port import PontoTuristicoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.evento_turistico_repository_port import EventoTuristicoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.pacote_turistico_repository_port import PacoteTuristicoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.roteiro_repository_port import RoteiroRepositoryPort
from apps.backend.app.modules.tourism.application.ports.reserva_hotel_repository_port import ReservaHotelRepositoryPort
from apps.backend.app.modules.tourism.application.ports.reserva_pacote_repository_port import ReservaPacoteRepositoryPort
from apps.backend.app.modules.tourism.application.ports.avaliacao_repository_port import AvaliacaoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.reclamacao_turismo_repository_port import ReclamacaoTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.cadastro_turista_repository_port import CadastroTuristaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.visitante_repository_port import VisitanteRepositoryPort
from apps.backend.app.modules.tourism.application.ports.fluxo_turistico_repository_port import FluxoTuristicoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.ocupacao_hoteleira_repository_port import OcupacaoHoteleiraRepositoryPort
from apps.backend.app.modules.tourism.application.ports.tarifa_hotel_repository_port import TarifaHotelRepositoryPort
from apps.backend.app.modules.tourism.application.ports.temporada_repository_port import TemporadaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.promocao_turistica_repository_port import PromocaoTuristicaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.licenca_turismo_repository_port import LicencaTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.cadastur_repository_port import CadasturRepositoryPort
from apps.backend.app.modules.tourism.application.ports.registro_guia_repository_port import RegistroGuiaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.credencial_repository_port import CredencialRepositoryPort
from apps.backend.app.modules.tourism.application.ports.fiscalizacao_turismo_repository_port import FiscalizacaoTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.auto_infracao_turismo_repository_port import AutoInfracaoTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.multa_turismo_repository_port import MultaTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.classificacao_hoteleira_repository_port import ClassificacaoHoteleiraRepositoryPort
from apps.backend.app.modules.tourism.application.ports.certificacao_turistica_repository_port import CertificacaoTuristicaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.estatistica_turismo_repository_port import EstatisticaTurismoRepositoryPort
from apps.backend.app.modules.tourism.application.ports.chegada_turistas_repository_port import ChegadaTuristasRepositoryPort
from apps.backend.app.modules.tourism.application.ports.receita_turistica_repository_port import ReceitaTuristicaRepositoryPort
from apps.backend.app.modules.tourism.application.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.tourism.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.tourism.application.ports.transportes_logistica_service_port import TransportesLogisticaServicePort
from apps.backend.app.modules.tourism.application.ports.ambiente_service_port import AmbienteServicePort
from apps.backend.app.modules.tourism.application.ports.cultura_service_port import CulturaServicePort
from apps.backend.app.modules.tourism.application.ports.comercio_servicos_service_port import ComercioServicosServicePort
from apps.backend.app.modules.tourism.application.ports.geosampa_service_port import GeosampaServicePort
__all__ = ['BaseRepositoryPort', 'BaseIntegrationServicePort', 'OperadorTuristicoRepositoryPort', 'AgenciaViagensRepositoryPort', 'GuiaTurismoRepositoryPort', 'CondutorVisitantesRepositoryPort', 'HotelRepositoryPort', 'PousadaRepositoryPort', 'ResortRepositoryPort', 'AtracaoTuristicaRepositoryPort', 'PontoTuristicoRepositoryPort', 'EventoTuristicoRepositoryPort', 'PacoteTuristicoRepositoryPort', 'RoteiroRepositoryPort', 'ReservaHotelRepositoryPort', 'ReservaPacoteRepositoryPort', 'AvaliacaoRepositoryPort', 'ReclamacaoTurismoRepositoryPort', 'CadastroTuristaRepositoryPort', 'VisitanteRepositoryPort', 'FluxoTuristicoRepositoryPort', 'OcupacaoHoteleiraRepositoryPort', 'TarifaHotelRepositoryPort', 'TemporadaRepositoryPort', 'PromocaoTuristicaRepositoryPort', 'LicencaTurismoRepositoryPort', 'CadasturRepositoryPort', 'RegistroGuiaRepositoryPort', 'CredencialRepositoryPort', 'FiscalizacaoTurismoRepositoryPort', 'AutoInfracaoTurismoRepositoryPort', 'MultaTurismoRepositoryPort', 'ClassificacaoHoteleiraRepositoryPort', 'CertificacaoTuristicaRepositoryPort', 'EstatisticaTurismoRepositoryPort', 'ChegadaTuristasRepositoryPort', 'ReceitaTuristicaRepositoryPort', 'CitizenServicePort', 'RequestServicePort', 'TransportesLogisticaServicePort', 'AmbienteServicePort', 'CulturaServicePort', 'ComercioServicosServicePort', 'GeosampaServicePort']
