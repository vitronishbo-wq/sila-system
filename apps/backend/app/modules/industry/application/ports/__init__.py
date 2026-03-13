from apps.backend.app.modules.industry.application.ports.aguas_saneamento_service_port import AguasSaneamentoServicePort
from apps.backend.app.modules.industry.application.ports.ambiente_service_port import AmbienteServicePort
from apps.backend.app.modules.industry.application.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.industry.application.ports.comercio_externo_service_port import ComercioExternoServicePort
from apps.backend.app.modules.industry.application.ports.energia_service_port import EnergiaServicePort
from apps.backend.app.modules.industry.application.ports.estabelecimento_industrial_repository_port import EstabelecimentoIndustrialRepositoryPort
from apps.backend.app.modules.industry.application.ports.financas_impostos_service_port import FinancasImpostosServicePort
from apps.backend.app.modules.industry.application.ports.geosampa_service_port import GeosampaServicePort
from apps.backend.app.modules.industry.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort
from apps.backend.app.modules.industry.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.industry.application.ports.transportes_logistica_service_port import TransportesLogisticaServicePort
from apps.backend.app.modules.industry.application.ports.urbanismo_service_port import UrbanismoServicePort
ComercioInternacionalServicePort = ComercioExternoServicePort
TributacaoFiscalServicePort = FinancasImpostosServicePort
__all__ = ['EstabelecimentoIndustrialRepositoryPort', 'CitizenServicePort', 'RequestServicePort', 'AmbienteServicePort', 'EnergiaServicePort', 'AguasSaneamentoServicePort', 'TransportesLogisticaServicePort', 'ComercioExternoServicePort', 'ComercioInternacionalServicePort', 'FinancasImpostosServicePort', 'TributacaoFiscalServicePort', 'GestaoFundiariaServicePort', 'UrbanismoServicePort', 'GeosampaServicePort']
