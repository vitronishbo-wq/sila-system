from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from app.modules.intelligence.defesa_consumidor.domain.enums import CategoriaReclamacao, Prioridade, StatusReclamacao

@dataclass
class Reclamacao:
    id: Optional[int]
    protocolo: str
    consumidor_id: int
    estabelecimento_id: int
    produto_servico: str
    descricao: str
    categoria: CategoriaReclamacao
    status: StatusReclamacao = StatusReclamacao.ABERTA
    prioridade: Prioridade = Prioridade.MEDIA
    valor_reclamado: Optional[float] = None
    data_abertura: datetime = field(default_factory=datetime.utcnow)
    data_resolucao: Optional[datetime] = None
    resolvido: bool = False
    descricao_resposta: Optional[str] = None

    def finalizar(self, resolvido: bool=True, descricao_resposta: Optional[str]=None) -> None:
        if self.resolvido:
            raise ValueError('Reclamacao ja esta finalizada')
        self.resolvido = resolvido
        self.status = StatusReclamacao.ENCERRADA
        self.data_resolucao = datetime.utcnow()
        self.descricao_resposta = descricao_resposta

    def escalar_prioridade(self) -> None:
        if self.resolvido:
            raise ValueError('Nao e possivel escalar reclamacao finalizada')
        ordem = [Prioridade.BAIXA, Prioridade.MEDIA, Prioridade.ALTA, Prioridade.CRITICA]
        idx = ordem.index(self.prioridade)
        if idx < len(ordem) - 1:
            self.prioridade = ordem[idx + 1]

    @property
    def dias_aberto(self) -> int:
        fim = self.data_resolucao or datetime.utcnow()
        return (fim - self.data_abertura).days