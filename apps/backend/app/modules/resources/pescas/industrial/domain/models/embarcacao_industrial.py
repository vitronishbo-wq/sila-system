from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.embarcacao import Embarcacao

@dataclass
class EmbarcacaoIndustrial(Embarcacao):
    capacidade_carga_congelada_ton: Decimal | None = None
    possui_sistema_reefer: bool = False
    homologada_exportacao: bool = False

    @classmethod
    def a_partir_embarcacao(cls, *, embarcacao: Embarcacao, capacidade_carga_congelada_ton: Decimal | None=None, possui_sistema_reefer: bool=False, homologada_exportacao: bool=False) -> 'EmbarcacaoIndustrial':
        return cls(id=embarcacao.id, nome=embarcacao.nome, numero_inscricao=embarcacao.numero_inscricao, tipo=embarcacao.tipo, modalidades=list(embarcacao.modalidades), comprimento=embarcacao.comprimento, arqueacao_bruta=embarcacao.arqueacao_bruta, tripulacao_minima=embarcacao.tripulacao_minima, porto_registro=embarcacao.porto_registro, ano_construcao=embarcacao.ano_construcao, material_casco=embarcacao.material_casco, proprietario_id=embarcacao.proprietario_id, potencia_motor=embarcacao.potencia_motor, capacidade_porao=embarcacao.capacidade_porao, armador_id=embarcacao.armador_id, licenca_id=embarcacao.licenca_id, equipamentos_seguranca=list(embarcacao.equipamentos_seguranca), sistema_rastreio=embarcacao.sistema_rastreio, data_inspecao=embarcacao.data_inspecao, data_validade_doc=embarcacao.data_validade_doc, observacoes=embarcacao.observacoes, capacidade_carga_congelada_ton=capacidade_carga_congelada_ton, possui_sistema_reefer=possui_sistema_reefer, homologada_exportacao=homologada_exportacao)