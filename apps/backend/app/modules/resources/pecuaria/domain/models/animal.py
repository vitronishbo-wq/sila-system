from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal

@dataclass
class Animal:
    id: UUID
    brinco: str
    tipo: TipoAnimal
    raca_id: UUID
    sexo: Sexo
    data_nascimento: date
    status: StatusAnimal
    proprietario_id: UUID
    propriedade_id: UUID
    data_entrada: date
    nome: Optional[str] = None
    peso_nascimento: Optional[Decimal] = None
    peso_atual: Optional[Decimal] = None
    rebanho_id: Optional[UUID] = None
    mae_id: Optional[UUID] = None
    pai_id: Optional[UUID] = None
    data_saida: Optional[date] = None
    observacoes: Optional[str] = None

    @classmethod
    def cadastrar(cls, *, brinco: str, tipo: TipoAnimal, raca_id: UUID, sexo: Sexo, data_nascimento: date, proprietario_id: UUID, propriedade_id: UUID, rebanho_id: Optional[UUID]=None) -> 'Animal':
        return cls(id=uuid4(), brinco=brinco, tipo=tipo, raca_id=raca_id, sexo=sexo, data_nascimento=data_nascimento, status=StatusAnimal.ATIVO, proprietario_id=proprietario_id, propriedade_id=propriedade_id, rebanho_id=rebanho_id, data_entrada=date.today())

    def atualizar_peso(self, peso: Decimal) -> None:
        self.peso_atual = peso

    def registrar_saida(self, data: date, status: StatusAnimal) -> None:
        if status == StatusAnimal.ATIVO:
            raise ValueError('Status de saida nao pode ser ativo')
        self.status = status
        self.data_saida = data