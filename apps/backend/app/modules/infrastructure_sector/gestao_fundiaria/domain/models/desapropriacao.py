from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao, TipoDesapropriacao

@dataclass
class Desapropriacao:
    id: UUID
    numero_processo: str
    imovel_inscricao: str
    tipo: TipoDesapropriacao
    ente_publico: str
    finalidade: str
    valor_indenizacao: Decimal
    data_inicio: date
    status: StatusDesapropriacao = StatusDesapropriacao.INSTAURADA
    ativo: bool = True
    data_decreto: date | None = None
    data_pagamento: date | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def instaurar(cls, *, numero_processo: str, imovel_inscricao: str, tipo: TipoDesapropriacao, ente_publico: str, finalidade: str, valor_indenizacao: Decimal) -> 'Desapropriacao':
        if not numero_processo.strip():
            raise ValueError('Numero do processo e obrigatorio')
        if not imovel_inscricao.strip():
            raise ValueError('Inscricao do imovel e obrigatoria')
        if not ente_publico.strip():
            raise ValueError('Ente publico e obrigatorio')
        if not finalidade.strip():
            raise ValueError('Finalidade da desapropriacao e obrigatoria')
        if valor_indenizacao <= Decimal('0'):
            raise ValueError('Valor da indenizacao deve ser maior que zero')
        return cls(id=uuid4(), numero_processo=numero_processo.strip(), imovel_inscricao=imovel_inscricao.strip(), tipo=tipo, ente_publico=ente_publico.strip(), finalidade=finalidade.strip(), valor_indenizacao=valor_indenizacao.quantize(Decimal('0.01')), data_inicio=date.today(), status=StatusDesapropriacao.INSTAURADA, ativo=True)

    def decretar(self, data_decreto: date) -> None:
        if self.status in (StatusDesapropriacao.CANCELADA, StatusDesapropriacao.ENCERRADA):
            raise ValueError('Nao e possivel decretar processo encerrado/cancelado')
        if data_decreto < self.data_inicio:
            raise ValueError('Data do decreto nao pode ser anterior ao inicio do processo')
        self.status = StatusDesapropriacao.DECRETADA
        self.data_decreto = data_decreto
        self.data_atualizacao = date.today()

    def registrar_pagamento(self, data_pagamento: date | None=None) -> None:
        if self.status not in (StatusDesapropriacao.DECRETADA, StatusDesapropriacao.EM_AVALIACAO):
            raise ValueError('Pagamento exige processo decretado ou em avaliacao')
        pagamento = data_pagamento or date.today()
        if self.data_decreto and pagamento < self.data_decreto:
            raise ValueError('Data de pagamento nao pode ser anterior ao decreto')
        self.status = StatusDesapropriacao.INDENIZADA
        self.data_pagamento = pagamento
        self.data_atualizacao = date.today()

    def encerrar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo de encerramento e obrigatorio')
        if self.status == StatusDesapropriacao.CANCELADA:
            raise ValueError('Processo cancelado nao pode ser encerrado')
        self.status = StatusDesapropriacao.ENCERRADA
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def cancelar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo de cancelamento e obrigatorio')
        if self.status == StatusDesapropriacao.INDENIZADA:
            raise ValueError('Processo indenizado nao pode ser cancelado')
        self.status = StatusDesapropriacao.CANCELADA
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()