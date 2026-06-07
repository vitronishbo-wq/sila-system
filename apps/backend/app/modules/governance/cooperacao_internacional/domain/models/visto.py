from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from uuid import UUID, uuid4

from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import (
    CategoriaVisto,
    StatusVisto,
    TipoVisto,
)


@dataclass
class Visto:
    tipo: TipoVisto
    categoria: CategoriaVisto
    solicitante_cpf: str
    solicitante_nome: str
    solicitante_passaporte: str
    pais_origem_id: UUID
    pais_destino_id: UUID
    data_entrada_prevista: date
    data_saida_prevista: date
    objetivo_viagem: str
    consulato_emissor_id: UUID
    id: UUID = field(default_factory=uuid4)
    numero_processo: str = ""
    status: StatusVisto = StatusVisto.SOLICITADO
    data_solicitacao: datetime = field(default_factory=datetime.utcnow)
    data_emissao: date | None = None
    data_validade: date | None = None
    numero_visto: str | None = None
    historico_analise: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.numero_processo = self.numero_processo or self._gerar_numero_processo()
        if self.data_saida_prevista <= self.data_entrada_prevista:
            raise ValueError("Data de saida deve ser maior que data de entrada")

    def _gerar_numero_processo(self) -> str:
        return f"VIST{datetime.utcnow().year}{uuid4().hex[:10].upper()}"

    def analisar(self, *, analista: str, resultado: str, justificativa: str | None = None) -> None:
        self.status = StatusVisto.EM_ANALISE
        self.historico_analise.append(
            {
                "data": datetime.utcnow().isoformat(),
                "analista": analista,
                "resultado": resultado,
                "justificativa": justificativa,
            }
        )

    def aprovar(self, *, autoridade: str, validade_dias: int = 90) -> None:
        if validade_dias <= 0:
            raise ValueError("Validade deve ser positiva")
        self.status = StatusVisto.APROVADO
        self.data_emissao = date.today()
        self.data_validade = date.today() + timedelta(days=validade_dias)
        self.numero_visto = f"V{datetime.utcnow().strftime('%Y%m%d')}{uuid4().hex[:6].upper()}"
        self.historico_analise.append(
            {"data": datetime.utcnow().isoformat(), "analista": autoridade, "resultado": "APROVADO"}
        )

    def emitir(self) -> None:
        if self.status != StatusVisto.APROVADO:
            raise ValueError("Somente vistos aprovados podem ser emitidos")
        self.status = StatusVisto.EMITIDO

    def negar(self, *, motivo: str) -> None:
        self.status = StatusVisto.NEGADO
        self.historico_analise.append(
            {"data": datetime.utcnow().isoformat(), "resultado": "NEGADO", "justificativa": motivo}
        )

    def esta_valido(self) -> bool:
        return self.status == StatusVisto.EMITIDO and bool(
            self.data_validade and date.today() <= self.data_validade
        )
