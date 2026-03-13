from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import RiscoSocial, SituacaoOcupacional, TipoVulnerabilidade

@dataclass
class RiscoEvasao:
    id: UUID
    codigo_risco: str
    jovem_id: UUID
    citizen_id: UUID | None
    matricula_ativa: bool
    situacao_ocupacional: SituacaoOcupacional
    vulnerabilidades: list[TipoVulnerabilidade] | None
    pontuacao: int
    nivel_risco: RiscoSocial
    data_avaliacao: date
    fatores: list[str]
    recomendacoes: list[str]
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def avaliar(cls, *, codigo_risco: str, jovem_id: UUID, citizen_id: UUID | None, matricula_ativa: bool, situacao_ocupacional: SituacaoOcupacional, vulnerabilidades: list[TipoVulnerabilidade] | None, observacoes: str | None=None) -> 'RiscoEvasao':
        score, fatores, recomendacoes = cls._calcular_sinalizadores(matricula_ativa=matricula_ativa, situacao_ocupacional=situacao_ocupacional, vulnerabilidades=vulnerabilidades)
        return cls(id=uuid4(), codigo_risco=codigo_risco.strip(), jovem_id=jovem_id, citizen_id=citizen_id, matricula_ativa=matricula_ativa, situacao_ocupacional=situacao_ocupacional, vulnerabilidades=vulnerabilidades, pontuacao=score, nivel_risco=cls._classificar(score), data_avaliacao=date.today(), fatores=fatores, recomendacoes=recomendacoes, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    @staticmethod
    def _classificar(score: int) -> RiscoSocial:
        if score >= 75:
            return RiscoSocial.CRITICO
        if score >= 50:
            return RiscoSocial.ALTO
        if score >= 25:
            return RiscoSocial.MEDIO
        return RiscoSocial.BAIXO

    @staticmethod
    def _calcular_sinalizadores(*, matricula_ativa: bool, situacao_ocupacional: SituacaoOcupacional, vulnerabilidades: list[TipoVulnerabilidade] | None) -> tuple[int, list[str], list[str]]:
        score = 0
        fatores: list[str] = []
        recomendacoes: list[str] = []
        if not matricula_ativa:
            score += 60
            fatores.append('sem_matricula_ativa')
            recomendacoes.append('Encaminhar para regularizacao de matricula no modulo educacao')
        if situacao_ocupacional in {SituacaoOcupacional.NAO_ESTUDA_NAO_TRABALHA, SituacaoOcupacional.DESEMPREGADO, SituacaoOcupacional.PROCURA_EMPREGO}:
            score += 20
            fatores.append(f'situacao_ocupacional:{situacao_ocupacional.value}')
            recomendacoes.append('Priorizar jovem para programa de formacao e transicao para emprego')
        qtd_vulnerabilidades = len(vulnerabilidades or [])
        if qtd_vulnerabilidades > 0:
            score += min(20, qtd_vulnerabilidades * 5)
            fatores.append(f'vulnerabilidades:{qtd_vulnerabilidades}')
            recomendacoes.append('Ativar acompanhamento psicossocial e monitorar frequencia mensal')
        return (min(score, 100), fatores, recomendacoes)