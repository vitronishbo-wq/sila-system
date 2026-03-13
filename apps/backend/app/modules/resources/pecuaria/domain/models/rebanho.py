from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.resources.pecuaria.domain.enums import StatusRebanho, TipoAnimal

@dataclass
class Rebanho:
    id: UUID
    codigo_rebanho: str
    propriedade_id: UUID
    tipo_animal: TipoAnimal
    descricao: str
    quantidade_animais: int
    data_cadastro: date
    status: StatusRebanho

    @classmethod
    def criar(cls, *, propriedade_id: UUID, tipo_animal: TipoAnimal, descricao: str, quantidade_animais: int=0) -> 'Rebanho':
        if quantidade_animais < 0:
            raise ValueError('Quantidade de animais nao pode ser negativa')
        return cls(id=uuid4(), codigo_rebanho='', propriedade_id=propriedade_id, tipo_animal=tipo_animal, descricao=descricao, quantidade_animais=quantidade_animais, data_cadastro=date.today(), status=StatusRebanho.ATIVO)

    def registrar_entrada(self, quantidade: int=1) -> None:
        if quantidade <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        self.quantidade_animais += quantidade

    def registrar_saida(self, quantidade: int=1) -> None:
        if quantidade <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        if quantidade > self.quantidade_animais:
            raise ValueError('Quantidade de saida maior que estoque do rebanho')
        self.quantidade_animais -= quantidade