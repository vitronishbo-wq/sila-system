from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusEstoque


@dataclass
class Estoque:
    id: UUID
    codigo_estoque: str
    codigo_insumo: str
    quantidade_atual: float
    quantidade_minima: float
    status: StatusEstoque
    data_atualizacao: datetime

    @classmethod
    def criar(
        cls, *, codigo_insumo: str, quantidade_atual: float, quantidade_minima: float
    ) -> Estoque:
        if quantidade_minima < 0:
            raise ValueError("Quantidade minima nao pode ser negativa")
        if quantidade_atual < 0:
            raise ValueError("Quantidade atual nao pode ser negativa")
        status = cls._calcular_status(quantidade_atual, quantidade_minima)
        return cls(
            id=uuid4(),
            codigo_estoque="",
            codigo_insumo=codigo_insumo,
            quantidade_atual=round(quantidade_atual, 3),
            quantidade_minima=round(quantidade_minima, 3),
            status=status,
            data_atualizacao=datetime.utcnow(),
        )

    def atualizar_quantidade(self, quantidade_atual: float) -> None:
        if quantidade_atual < 0:
            raise ValueError("Quantidade atual nao pode ser negativa")
        self.quantidade_atual = round(quantidade_atual, 3)
        self.status = self._calcular_status(self.quantidade_atual, self.quantidade_minima)
        self.data_atualizacao = datetime.utcnow()

    @staticmethod
    def _calcular_status(quantidade_atual: float, quantidade_minima: float) -> StatusEstoque:
        if quantidade_atual <= 0:
            return StatusEstoque.ZERADO
        if quantidade_atual <= quantidade_minima:
            return StatusEstoque.BAIXO
        return StatusEstoque.NORMAL
