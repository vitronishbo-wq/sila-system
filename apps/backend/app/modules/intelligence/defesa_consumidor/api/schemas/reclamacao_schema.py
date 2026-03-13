from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class CategoriaEnum(str, Enum):
    PRODUTO_DEFECTUOSO = 'produto_defectuoso'
    SERVICO_NAO_PRESTADO = 'servico_nao_prestado'
    PROPAGANDA_ENGANOSA = 'propaganda_enganosa'
    COBRANCA_INDEVIDA = 'cobranca_indevida'
    ATENDIMENTO_INADEQUADO = 'atendimento_inadequado'
    RECUSA_VENDA = 'recusa_venda'
    OUTROS = 'outros'

class StatusEnum(str, Enum):
    ABERTA = 'aberta'
    EM_ANALISE = 'em_analise'
    EM_MEDIACAO = 'em_mediacao'
    AGUARDANDO_CONSUMIDOR = 'aguardando_consumidor'
    AGUARDANDO_ESTABELECIMENTO = 'aguardando_estabelecimento'
    ENCERRADA = 'encerrada'
    CANCELADA = 'cancelada'

class PrioridadeEnum(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'
    CRITICA = 'critica'

class ReclamacaoCreate(BaseModel):
    consumidor_id: int = Field(..., gt=0)
    estabelecimento_id: int = Field(..., gt=0)
    produto_servico: str = Field(..., min_length=3, max_length=200)
    descricao: str = Field(..., min_length=10, max_length=5000)
    categoria: CategoriaEnum
    valor_reclamado: Optional[float] = Field(default=None, ge=0)
    prioridade: PrioridadeEnum = PrioridadeEnum.MEDIA

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, value: str) -> str:
        if len(value.strip()) < 10:
            raise ValueError('Descricao deve ter pelo menos 10 caracteres')
        return value

class ReclamacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    protocolo: str
    consumidor_id: int
    estabelecimento_id: int
    produto_servico: str
    descricao: str
    categoria: str
    status: str
    prioridade: str
    valor_reclamado: Optional[float] = None
    data_abertura: datetime
    data_resolucao: Optional[datetime] = None
    resolvido: bool
    descricao_resposta: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime

class ReclamacaoListaResponse(BaseModel):
    reclamacoes: list[ReclamacaoResponse]
    total: int
    pagina: int = 1
    tamanho_pagina: int = 20
    total_paginas: int = 0

    @model_validator(mode='after')
    def calcular_total_paginas(self) -> 'ReclamacaoListaResponse':
        if self.tamanho_pagina > 0:
            self.total_paginas = (self.total + self.tamanho_pagina - 1) // self.tamanho_pagina
        return self