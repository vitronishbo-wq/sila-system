from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import StatusFormacao

@dataclass
class FormacaoJuvenil:
    id: UUID
    codigo_formacao: str
    jovem_id: UUID
    nome_curso: str
    instituicao: str
    carga_horaria: int
    data_inicio: date
    data_cadastro: date
    programa_id: UUID | None = None
    data_fim: date | None = None
    certificado_emitido: bool = False
    status: StatusFormacao = StatusFormacao.INSCRITO
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_formacao: str, jovem_id: UUID, nome_curso: str, instituicao: str, carga_horaria: int, data_inicio: date, programa_id: UUID | None=None, data_fim: date | None=None, observacoes: str | None=None) -> 'FormacaoJuvenil':
        if len(nome_curso.strip()) < 3:
            raise ValueError('Nome do curso deve ter pelo menos 3 caracteres')
        if len(instituicao.strip()) < 3:
            raise ValueError('Instituicao deve ter pelo menos 3 caracteres')
        if carga_horaria <= 0:
            raise ValueError('Carga horaria deve ser maior que zero')
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError('Data fim da formacao deve ser maior ou igual a data inicio')
        return cls(id=uuid4(), codigo_formacao=codigo_formacao.strip(), jovem_id=jovem_id, nome_curso=nome_curso.strip(), instituicao=instituicao.strip(), carga_horaria=carga_horaria, data_inicio=data_inicio, programa_id=programa_id, data_fim=data_fim, data_cadastro=date.today(), status=StatusFormacao.INSCRITO, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusFormacao, certificado_emitido: bool | None=None) -> None:
        self.status = status
        if certificado_emitido is not None:
            self.certificado_emitido = certificado_emitido
        self.ativo = status not in {StatusFormacao.CONCLUIDA, StatusFormacao.CANCELADA}