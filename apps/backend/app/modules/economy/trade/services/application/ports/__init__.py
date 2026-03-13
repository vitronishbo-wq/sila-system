from apps.backend.app.modules.economy.trade.services.application.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.comercio_externo_service_port import ComercioExternoServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.defesa_consumidor_service_port import DefesaConsumidorServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.estabelecimento_comercial_repository_port import EstabelecimentoComercialRepositoryPort
from apps.backend.app.modules.economy.trade.services.application.ports.financas_impostos_service_port import FinancasImpostosServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.geosampa_service_port import GeosampaServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.industria_service_port import IndustriaServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.transportes_logistica_service_port import TransportesLogisticaServicePort
from apps.backend.app.modules.economy.trade.services.application.ports.urbanismo_service_port import UrbanismoServicePort
ComercioInternacionalServicePort = ComercioExternoServicePort
TributacaoFiscalServicePort = FinancasImpostosServicePort
__all__ = ['EstabelecimentoComercialRepositoryPort', 'CitizenServicePort', 'RequestServicePort', 'IndustriaServicePort', 'TransportesLogisticaServicePort', 'ComercioExternoServicePort', 'ComercioInternacionalServicePort', 'FinancasImpostosServicePort', 'TributacaoFiscalServicePort', 'DefesaConsumidorServicePort', 'UrbanismoServicePort', 'GeosampaServicePort']