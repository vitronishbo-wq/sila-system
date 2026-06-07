from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.public_security.domain.enums import (
    StatusUnidadePolicial,
    TipoUnidadePolicial,
)


@dataclass
class UnidadePolicial:
    id: UUID
    codigo_unidade: str
    nome: str
    tipo: TipoUnidadePolicial
    municipio: str
    provincia: str
    endereco: str
    comandante: str
    data_ativacao: date
    status: StatusUnidadePolicial = StatusUnidadePolicial.ATIVA
    telefone: str | None = None
    email: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(
        cls,
        *,
        codigo_unidade: str,
        nome: str,
        tipo: TipoUnidadePolicial,
        municipio: str,
        provincia: str,
        endereco: str,
        comandante: str,
        telefone: str | None = None,
        email: str | None = None,
        observacoes: str | None = None,
    ) -> UnidadePolicial:
        if len(nome.strip()) < 3:
            raise ValueError("Nome da unidade deve ter pelo menos 3 caracteres")
        if len(comandante.strip()) < 3:
            raise ValueError("Comandante deve ter pelo menos 3 caracteres")
        return cls(
            id=uuid4(),
            codigo_unidade=codigo_unidade.strip(),
            nome=nome.strip(),
            tipo=tipo,
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            endereco=endereco.strip(),
            comandante=comandante.strip(),
            data_ativacao=date.today(),
            status=StatusUnidadePolicial.ATIVA,
            telefone=telefone.strip() if telefone else None,
            email=email.strip().lower() if email else None,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusUnidadePolicial, motivo: str | None = None) -> None:
        self.status = status
        self.ativo = status not in {StatusUnidadePolicial.DESATIVADA}
        if motivo:
            self.observacoes = motivo.strip()
