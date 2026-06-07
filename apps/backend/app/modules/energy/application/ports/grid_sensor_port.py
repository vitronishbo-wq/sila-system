from abc import ABC, abstractmethod


class GridSensorPort(ABC):
    @abstractmethod
    async def ingest_telemetry(self, sensor_id: str, load_kw: float, status: str):
        """Ponto de entrada para dados de IoT em tempo real."""
        raise NotImplementedError

    @abstractmethod
    async def trigger_load_shedding(self, region_id: str):
        """Acao critica: corte de carga preventivo em caso de sobrecarga."""
        raise NotImplementedError
