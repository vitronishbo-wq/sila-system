from __future__ import annotations
from dataclasses import dataclass
from app.modules.economy.trade.external.domain.enums import TipoOperador, TipoPessoa
from app.modules.economy.trade.external.domain.models.operador_logistico_base import OperadorLogisticoBase

@dataclass
class Drawback(OperadorLogisticoBase):

    @classmethod
    def cadastrar(cls, *, razao_social: str, cnpj_cpf: str, tipo_pessoa: TipoPessoa, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str) -> 'Drawback':
        return super().cadastrar(tipo_operador=TipoOperador.EXPORTADOR_IMPORTADOR, razao_social=razao_social, cnpj_cpf=cnpj_cpf, tipo_pessoa=tipo_pessoa, endereco=endereco, numero=numero, bairro=bairro, municipio=municipio, provincia=provincia, cep=cep)