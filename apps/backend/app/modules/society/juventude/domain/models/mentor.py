from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusMentoria, TipoMentoria

@dataclass
class Mentor:
    id: UUID
    codigo_mentor: str
    nome: str
    tipo_mentoria: TipoMentoria
    area_interesse: AreaInteresse
    data_cadastro: date
    email: str | None = None
    telefone: str | None = None
    jovem_ids: list[UUID] | None = None
    status: StatusMentoria = StatusMentoria.ATIVA
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, codigo_mentor: str, nome: str, tipo_mentoria: TipoMentoria, area_interesse: AreaInteresse, email: str | None=None, telefone: str | None=None, observacoes: str | None=None) -> 'Mentor':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do mentor deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), codigo_mentor=codigo_mentor.strip(), nome=nome_normalizado, tipo_mentoria=tipo_mentoria, area_interesse=area_interesse, data_cadastro=date.today(), email=email.strip().lower() if email else None, telefone=telefone.strip() if telefone else None, observacoes=observacoes.strip() if observacoes else None, status=StatusMentoria.ATIVA, ativo=True)

    def atribuir_jovem(self, jovem_id: UUID) -> None:
        if self.jovem_ids is None:
            self.jovem_ids = []
        if jovem_id not in self.jovem_ids:
            self.jovem_ids.append(jovem_id)

    def atualizar_status(self, status: StatusMentoria) -> None:
        self.status = status
        self.ativo = status not in {StatusMentoria.CANCELADA, StatusMentoria.CONCLUIDA}