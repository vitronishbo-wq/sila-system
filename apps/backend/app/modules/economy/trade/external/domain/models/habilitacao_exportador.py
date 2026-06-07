from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from apps.backend.app.modules.economy.trade.external.domain.enums import TipoOperador, TipoPessoa
from apps.backend.app.modules.economy.trade.external.domain.models.habilitacao_base import (
    HabilitacaoBase,
)


@dataclass
class HabilitacaoExportador(HabilitacaoBase):
    @classmethod
    def solicitar(
        cls,
        *,
        tipo_pessoa: TipoPessoa,
        razao_social: str,
        cnpj_cpf: str,
        numero_processo: str,
        data_solicitacao: date,
    ) -> HabilitacaoExportador:
        return super().solicitar(
            tipo_operador=TipoOperador.EXPORTADOR,
            tipo_pessoa=tipo_pessoa,
            razao_social=razao_social,
            cnpj_cpf=cnpj_cpf,
            numero_processo=numero_processo,
            data_solicitacao=data_solicitacao,
        )
