from __future__ import annotations

from dataclasses import dataclass

from apps.backend.app.modules.resources.pescas.domain.models.armador import Armador


@dataclass
class ArmadorIndustrial(Armador):
    registro_industrial: str | None = None
    capacidade_total_toneladas_mes: float | None = None

    @classmethod
    def a_partir_armador(
        cls,
        *,
        armador: Armador,
        registro_industrial: str | None = None,
        capacidade_total_toneladas_mes: float | None = None,
    ) -> ArmadorIndustrial:
        return cls(
            id=armador.id,
            nome=armador.nome,
            nif=armador.nif,
            data_registro=armador.data_registro,
            ativo=armador.ativo,
            telefone=armador.telefone,
            email=armador.email,
            observacoes=armador.observacoes,
            registro_industrial=registro_industrial,
            capacidade_total_toneladas_mes=capacidade_total_toneladas_mes,
        )
