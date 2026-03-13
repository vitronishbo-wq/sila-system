from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento

@dataclass
class AbastecimentoAgua:
    id: UUID
    codigo_abastecimento: str
    infraestrutura_id: UUID
    nome_sistema: str
    provincia: str
    municipio: str
    status: StatusAbastecimento
    data_registro: date
    data_inicio_operacao: date | None = None
    data_interrupcao: date | None = None
    motivo_interrupcao: str | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, infraestrutura_id: UUID, nome_sistema: str, provincia: str, municipio: str) -> 'AbastecimentoAgua':
        if not nome_sistema.strip():
            raise ValueError('Nome do sistema de abastecimento e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia do abastecimento e obrigatoria')
        if not municipio.strip():
            raise ValueError('Municipio do abastecimento e obrigatorio')
        return cls(id=uuid4(), codigo_abastecimento='', infraestrutura_id=infraestrutura_id, nome_sistema=nome_sistema.strip(), provincia=provincia.strip(), municipio=municipio.strip(), status=StatusAbastecimento.PLANEJADO, data_registro=date.today())

    def iniciar_operacao(self, *, data_inicio_operacao: date | None=None) -> None:
        if self.status != StatusAbastecimento.PLANEJADO:
            raise ValueError('Apenas abastecimento planejado pode iniciar operacao')
        self.status = StatusAbastecimento.OPERACIONAL
        self.data_inicio_operacao = data_inicio_operacao or date.today()
        self.data_interrupcao = None
        self.motivo_interrupcao = None

    def interromper(self, motivo: str) -> None:
        if self.status != StatusAbastecimento.OPERACIONAL:
            raise ValueError('Apenas abastecimento operacional pode ser interrompido')
        if not motivo.strip():
            raise ValueError('Motivo da interrupcao e obrigatorio')
        self.status = StatusAbastecimento.INTERROMPIDO
        self.data_interrupcao = date.today()
        self.motivo_interrupcao = motivo.strip()

    def retomar(self) -> None:
        if self.status != StatusAbastecimento.INTERROMPIDO:
            raise ValueError('Apenas abastecimento interrompido pode ser retomado')
        self.status = StatusAbastecimento.OPERACIONAL
        self.data_interrupcao = None
        self.motivo_interrupcao = None

    def encerrar(self, motivo: str) -> None:
        if self.status == StatusAbastecimento.ENCERRADO:
            raise ValueError('Abastecimento ja encerrado')
        if not motivo.strip():
            raise ValueError('Motivo do encerramento e obrigatorio')
        self.status = StatusAbastecimento.ENCERRADO
        self.observacoes = motivo.strip()