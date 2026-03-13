from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Proprietario:
    id: UUID
    codigo_proprietario: str
    nome: str
    documento: str
    telefone: str | None
    email: str | None
    data_cadastro: date
    ativo: bool = True

    @classmethod
    def criar(cls, *, nome: str, documento: str, telefone: str | None=None, email: str | None=None) -> 'Proprietario':
        if len(documento.strip()) < 5:
            raise ValueError('Documento invalido')
        return cls(id=uuid4(), codigo_proprietario='', nome=nome.strip(), documento=documento.strip(), telefone=telefone, email=email, data_cadastro=date.today(), ativo=True)