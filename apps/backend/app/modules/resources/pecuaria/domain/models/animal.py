from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal


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
    nome: str | None = None
    peso_nascimento: Decimal | None = None
    peso_atual: Decimal | None = None
    rebanho_id: UUID | None = None
    mae_id: UUID | None = None
    pai_id: UUID | None = None
    data_saida: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        brinco: str,
        tipo: TipoAnimal,
        raca_id: UUID,
        sexo: Sexo,
        data_nascimento: date,
        proprietario_id: UUID,
        propriedade_id: UUID,
        rebanho_id: UUID | None = None,
    ) -> Animal:
        return cls(
            id=uuid4(),
            brinco=brinco,
            tipo=tipo,
            raca_id=raca_id,
            sexo=sexo,
            data_nascimento=data_nascimento,
            status=StatusAnimal.ATIVO,
            proprietario_id=proprietario_id,
            propriedade_id=propriedade_id,
            rebanho_id=rebanho_id,
            data_entrada=date.today(),
        )

    def atualizar_peso(self, peso: Decimal) -> None:
        self.peso_atual = peso

    def registrar_saida(self, data: date, status: StatusAnimal) -> None:
        if status == StatusAnimal.ATIVO:
            raise ValueError("Status de saida nao pode ser ativo")
        self.status = status
        self.data_saida = data
