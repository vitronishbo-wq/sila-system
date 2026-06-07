from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoOperacao


@dataclass
class Operacao:
    id: UUID
    codigo_operacao: str
    codigo_safra: str
    tipo: TipoOperacao
    descricao: str
    data_operacao: datetime
    codigo_insumo: str | None = None
    quantidade_insumo: float | None = None

    @classmethod
    def registrar(
        cls,
        *,
        codigo_safra: str,
        tipo: TipoOperacao,
        descricao: str,
        codigo_insumo: str | None = None,
        quantidade_insumo: float | None = None,
    ) -> Operacao:
        if codigo_insumo and (quantidade_insumo is None or quantidade_insumo <= 0):
            raise ValueError("Quantidade de insumo deve ser maior que zero quando houver insumo")
        if quantidade_insumo is not None and quantidade_insumo <= 0:
            raise ValueError("Quantidade de insumo deve ser maior que zero")
        return cls(
            id=uuid4(),
            codigo_operacao="",
            codigo_safra=codigo_safra,
            tipo=tipo,
            descricao=descricao,
            data_operacao=datetime.utcnow(),
            codigo_insumo=codigo_insumo,
            quantidade_insumo=round(quantidade_insumo, 3)
            if quantidade_insumo is not None
            else None,
        )
