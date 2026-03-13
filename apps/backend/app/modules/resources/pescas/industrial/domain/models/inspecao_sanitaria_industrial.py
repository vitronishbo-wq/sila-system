from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.resources.pescas.industrial.domain.enums import StatusInspecao, TipoSeloInspecao

@dataclass
class InspecaoSanitariaIndustrial:
    id: UUID
    codigo_inspecao: str
    unidade_processamento_id: UUID
    data_agendada: date
    selo_inspecao: TipoSeloInspecao
    status: StatusInspecao
    fiscal_id: UUID | None = None
    lote_producao_id: UUID | None = None
    data_realizacao: date | None = None
    pontuacao: int | None = None
    inconformidades: list[str] | None = None
    observacoes: str | None = None

    @classmethod
    def agendar(cls, *, codigo_inspecao: str, unidade_processamento_id: UUID, data_agendada: date, selo_inspecao: TipoSeloInspecao, fiscal_id: UUID | None=None, lote_producao_id: UUID | None=None, observacoes: str | None=None) -> 'InspecaoSanitariaIndustrial':
        return cls(id=uuid4(), codigo_inspecao=codigo_inspecao.strip(), unidade_processamento_id=unidade_processamento_id, data_agendada=data_agendada, selo_inspecao=selo_inspecao, status=StatusInspecao.AGENDADA, fiscal_id=fiscal_id, lote_producao_id=lote_producao_id, observacoes=observacoes.strip() if observacoes else None)

    def iniciar(self) -> None:
        if self.status != StatusInspecao.AGENDADA:
            raise ValueError('Inspecao precisa estar agendada')
        self.status = StatusInspecao.EM_ANDAMENTO

    def concluir(self, *, pontuacao: int, aprovada: bool, inconformidades: list[str] | None=None, observacoes: str | None=None) -> None:
        if pontuacao < 0 or pontuacao > 100:
            raise ValueError('Pontuacao deve estar entre 0 e 100')
        self.pontuacao = pontuacao
        self.inconformidades = [item.strip() for item in inconformidades or [] if item.strip()] or None
        self.status = StatusInspecao.APROVADA if aprovada and (not self.inconformidades) else StatusInspecao.REPROVADA
        self.data_realizacao = date.today()
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def atualizar_status(self, status: StatusInspecao, observacoes: str | None=None) -> None:
        self.status = status
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
        if status in {StatusInspecao.APROVADA, StatusInspecao.REPROVADA, StatusInspecao.INTERDITADA}:
            self.data_realizacao = self.data_realizacao or date.today()