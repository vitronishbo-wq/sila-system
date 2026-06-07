from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCadastroAmbiental


@dataclass
class CadastroAmbiental:
    id: UUID
    codigo_cadastro_ambiental: str
    codigo_zoneamento: str
    codigo_propriedade: str
    reserva_legal_percentual: float
    app_percentual: float
    area_protecao_ha: float
    status: StatusCadastroAmbiental
    data_registro: date
    numero_processo: str | None = None
    data_validacao: date | None = None
    pendencias: list[str] | None = None

    @classmethod
    def registrar(
        cls,
        *,
        codigo_zoneamento: str,
        codigo_propriedade: str,
        reserva_legal_percentual: float,
        app_percentual: float,
        area_protecao_ha: float,
        numero_processo: str | None = None,
    ) -> CadastroAmbiental:
        if not 0 <= reserva_legal_percentual <= 100:
            raise ValueError("Reserva legal percentual deve estar entre 0 e 100")
        if not 0 <= app_percentual <= 100:
            raise ValueError("APP percentual deve estar entre 0 e 100")
        if area_protecao_ha < 0:
            raise ValueError("Area de protecao nao pode ser negativa")
        return cls(
            id=uuid4(),
            codigo_cadastro_ambiental="",
            codigo_zoneamento=codigo_zoneamento,
            codigo_propriedade=codigo_propriedade,
            reserva_legal_percentual=round(reserva_legal_percentual, 2),
            app_percentual=round(app_percentual, 2),
            area_protecao_ha=round(area_protecao_ha, 2),
            status=StatusCadastroAmbiental.PENDENTE,
            data_registro=date.today(),
            numero_processo=numero_processo,
            pendencias=[],
        )

    def validar(self, numero_processo: str) -> None:
        if self.pendencias:
            raise ValueError("Nao e possivel validar cadastro com pendencias")
        self.status = StatusCadastroAmbiental.VALIDADO
        self.numero_processo = numero_processo
        self.data_validacao = date.today()

    def adicionar_pendencia(self, pendencia: str) -> None:
        self.pendencias = self.pendencias or []
        self.pendencias.append(pendencia)
        self.status = StatusCadastroAmbiental.COM_PENDENCIA

    def sanar_pendencias(self) -> None:
        self.pendencias = []
        self.status = StatusCadastroAmbiental.PENDENTE
