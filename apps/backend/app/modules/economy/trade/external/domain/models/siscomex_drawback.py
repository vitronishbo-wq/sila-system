from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa
from apps.backend.app.modules.economy.trade.external.domain.models.habilitacao_base import HabilitacaoBase

@dataclass
class SiscomexDrawback(HabilitacaoBase):

    @classmethod
    def solicitar(cls, *, tipo_pessoa: TipoPessoa, razao_social: str, cnpj_cpf: str, numero_processo: str, data_solicitacao: date) -> 'SiscomexDrawback':
        return super().solicitar(tipo_operador=TipoOperador.EXPORTADOR_IMPORTADOR, tipo_pessoa=tipo_pessoa, razao_social=razao_social, cnpj_cpf=cnpj_cpf, numero_processo=numero_processo, data_solicitacao=data_solicitacao)

    def aprovar(self, *, numero_radar: str, data_analise: date, data_validade: date) -> None:
        super().aprovar(numero_radar=numero_radar, data_analise=data_analise, data_validade=data_validade)
        self.status = StatusHabilitacao.HABILITADO