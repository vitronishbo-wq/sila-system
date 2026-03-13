"""Adapters do modulo turismo."""
from app.modules.tourism.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from app.modules.tourism.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from app.modules.tourism.infrastructure.adapters.transportes_logistica_service_adapter import TransportesLogisticaServiceAdapter
from app.modules.tourism.infrastructure.adapters.ambiente_service_adapter import AmbienteServiceAdapter
from app.modules.tourism.infrastructure.adapters.cultura_service_adapter import CulturaServiceAdapter
from app.modules.tourism.infrastructure.adapters.comercio_servicos_service_adapter import ComercioServicosServiceAdapter
from app.modules.tourism.infrastructure.adapters.geosampa_service_adapter import GeosampaServiceAdapter
__all__ = ['CitizenServiceAdapter', 'RequestServiceAdapter', 'TransportesLogisticaServiceAdapter', 'AmbienteServiceAdapter', 'CulturaServiceAdapter', 'ComercioServicosServiceAdapter', 'GeosampaServiceAdapter']
