from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoEventoCultural

@dataclass
class EventoCultural:
    id: UUID
    codigo_evento: str
    nome: str
    tipo: TipoEventoCultural
    descricao: str
    data_inicio: date
    data_fim: date
    local: str
    municipio: str
    provincia: str
    realizador_id: UUID
    data_cadastro: date
    status: StatusEventoCultural = StatusEventoCultural.RASCUNHO
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    entrada_gratuita: bool = True
    valor_ingresso: Decimal | None = None
    publico_estimado: int | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo_evento: str, nome: str, tipo: TipoEventoCultural, descricao: str, data_inicio: date, data_fim: date, local: str, municipio: str, provincia: str, realizador_id: UUID, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, entrada_gratuita: bool=True, valor_ingresso: Decimal | None=None, publico_estimado: int | None=None, observacoes: str | None=None) -> 'EventoCultural':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do evento deve ter pelo menos 3 caracteres')
        if data_fim < data_inicio:
            raise ValueError('Data fim nao pode ser anterior a data inicio')
        if publico_estimado is not None and publico_estimado < 0:
            raise ValueError('Publico estimado nao pode ser negativo')
        if valor_ingresso is not None and valor_ingresso < 0:
            raise ValueError('Valor do ingresso nao pode ser negativo')
        if not entrada_gratuita and valor_ingresso is None:
            raise ValueError('Valor do ingresso e obrigatorio para evento pago')
        return cls(id=uuid4(), codigo_evento=codigo_evento.strip(), nome=nome_normalizado, tipo=tipo, descricao=descricao.strip(), data_inicio=data_inicio, data_fim=data_fim, local=local.strip(), municipio=municipio.strip(), provincia=provincia.strip(), realizador_id=realizador_id, data_cadastro=date.today(), atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id, entrada_gratuita=entrada_gratuita, valor_ingresso=valor_ingresso, publico_estimado=publico_estimado, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, tipo: TipoEventoCultural | None=None, descricao: str | None=None, data_inicio: date | None=None, data_fim: date | None=None, local: str | None=None, municipio: str | None=None, provincia: str | None=None, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, entrada_gratuita: bool | None=None, valor_ingresso: Decimal | None=None, publico_estimado: int | None=None, status: StatusEventoCultural | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        novo_inicio = data_inicio or self.data_inicio
        novo_fim = data_fim or self.data_fim
        if novo_fim < novo_inicio:
            raise ValueError('Data fim nao pode ser anterior a data inicio')
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do evento deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if descricao is not None:
            self.descricao = descricao.strip()
        if data_inicio is not None:
            self.data_inicio = data_inicio
        if data_fim is not None:
            self.data_fim = data_fim
        if local is not None:
            self.local = local.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if atracao_turistica_id is not None:
            self.atracao_turistica_id = atracao_turistica_id
        if instituicao_educacional_id is not None:
            self.instituicao_educacional_id = instituicao_educacional_id
        if entrada_gratuita is not None:
            self.entrada_gratuita = entrada_gratuita
        if valor_ingresso is not None:
            if valor_ingresso < 0:
                raise ValueError('Valor do ingresso nao pode ser negativo')
            self.valor_ingresso = valor_ingresso
        if publico_estimado is not None:
            if publico_estimado < 0:
                raise ValueError('Publico estimado nao pode ser negativo')
            self.publico_estimado = publico_estimado
        if status is not None:
            self.status = status
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
        if self.entrada_gratuita:
            self.valor_ingresso = None
        elif self.valor_ingresso is None:
            raise ValueError('Valor do ingresso e obrigatorio para evento pago')