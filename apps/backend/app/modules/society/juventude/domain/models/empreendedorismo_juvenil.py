from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEmpreendimento

@dataclass
class EmpreendedorismoJuvenil:
    id: UUID
    codigo_empreendimento: str
    jovem_id: UUID
    nome_negocio: str
    area_interesse: AreaInteresse
    data_cadastro: date
    status: StatusEmpreendimento = StatusEmpreendimento.IDEIA
    receita_mensal: Decimal | None = None
    valor_credito: Decimal | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_empreendimento: str, jovem_id: UUID, nome_negocio: str, area_interesse: AreaInteresse, receita_mensal: Decimal | None=None, valor_credito: Decimal | None=None, observacoes: str | None=None) -> 'EmpreendedorismoJuvenil':
        if len(nome_negocio.strip()) < 3:
            raise ValueError('Nome do negocio deve ter pelo menos 3 caracteres')
        if receita_mensal is not None and receita_mensal < 0:
            raise ValueError('Receita mensal nao pode ser negativa')
        if valor_credito is not None and valor_credito < 0:
            raise ValueError('Valor de credito nao pode ser negativo')
        return cls(id=uuid4(), codigo_empreendimento=codigo_empreendimento.strip(), jovem_id=jovem_id, nome_negocio=nome_negocio.strip(), area_interesse=area_interesse, data_cadastro=date.today(), receita_mensal=receita_mensal, valor_credito=valor_credito, observacoes=observacoes.strip() if observacoes else None, status=StatusEmpreendimento.IDEIA, ativo=True)

    def atualizar_status(self, status: StatusEmpreendimento) -> None:
        self.status = status
        self.ativo = status != StatusEmpreendimento.ENCERRADO