"""Adapters do modulo turismo."""
from apps.backend.app.modules.tourism.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.transportes_logistica_service_adapter import TransportesLogisticaServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.ambiente_service_adapter import AmbienteServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.cultura_service_adapter import CulturaServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.comercio_servicos_service_adapter import ComercioServicosServiceAdapter
from apps.backend.app.modules.tourism.infrastructure.adapters.geosampa_service_adapter import GeosampaServiceAdapter
__all__ = ['CitizenServiceAdapter', 'RequestServiceAdapter', 'TransportesLogisticaServiceAdapter', 'AmbienteServiceAdapter', 'CulturaServiceAdapter', 'ComercioServicosServiceAdapter', 'GeosampaServiceAdapter']
