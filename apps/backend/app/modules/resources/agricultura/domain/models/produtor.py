from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor


@dataclass
class Produtor:
    id: UUID
    cadastro_produtor: str
    tipo: TipoProdutor
    status: StatusProdutor
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    citizen_id: UUID | None = None
    empresa_id: UUID | None = None
    familiar: bool = False
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        nome: str,
        documento: str,
        documento_tipo: str,
        tipo: TipoProdutor,
        citizen_id: UUID | None = None,
        empresa_id: UUID | None = None,
        telefone: str | None = None,
        email: str | None = None,
        endereco: str | None = None,
        observacoes: str | None = None,
    ) -> Produtor:
        return cls(
            id=uuid4(),
            cadastro_produtor="",
            tipo=tipo,
            status=StatusProdutor.PENDENTE,
            nome=nome,
            documento=documento,
            documento_tipo=documento_tipo,
            data_cadastro=date.today(),
            telefone=telefone,
            email=email,
            endereco=endereco,
            citizen_id=citizen_id,
            empresa_id=empresa_id,
            familiar=tipo == TipoProdutor.FAMILIAR,
            observacoes=observacoes,
        )

    def ativar(self) -> None:
        if self.status != StatusProdutor.PENDENTE:
            raise ValueError("Apenas produtores pendentes podem ser ativados")
        self.status = StatusProdutor.ATIVO

    def suspender(self, motivo: str) -> None:
        if self.status != StatusProdutor.ATIVO:
            raise ValueError("Apenas produtores ativos podem ser suspensos")
        self.status = StatusProdutor.SUSPENSO
        self.observacoes = motivo
