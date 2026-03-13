from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.cultura.domain.enums import FaseEditalCultural, TipoEditalCultural

@dataclass
class Edital:
    id: UUID
    numero: str
    titulo: str
    tipo: TipoEditalCultural
    orgao_responsavel_id: UUID
    valor_total: Decimal
    valor_disponivel: Decimal
    data_publicacao: datetime
    data_inicio_inscricoes: datetime
    data_fim_inscricoes: datetime
    vagas: int
    descricao: str
    fase: FaseEditalCultural
    criterios: list[str] = field(default_factory=list)
    documentos_necessarios: list[str] = field(default_factory=list)
    inscricoes: list[UUID] = field(default_factory=list)
    projetos_selecionados: list[UUID] = field(default_factory=list)
    ativo: bool = True

    @classmethod
    def publicar(cls, *, numero: str, titulo: str, tipo: TipoEditalCultural, orgao_responsavel_id: UUID, valor_total: Decimal, data_publicacao: datetime, data_inicio_inscricoes: datetime, data_fim_inscricoes: datetime, vagas: int, descricao: str, criterios: list[str], documentos_necessarios: list[str]) -> 'Edital':
        if valor_total <= 0:
            raise ValueError('Valor total deve ser positivo')
        if vagas <= 0:
            raise ValueError('Vagas deve ser positivo')
        if data_fim_inscricoes <= data_inicio_inscricoes:
            raise ValueError('Data fim das inscricoes deve ser maior que data inicio')
        return cls(id=uuid4(), numero=numero.strip(), titulo=titulo.strip(), tipo=tipo, orgao_responsavel_id=orgao_responsavel_id, valor_total=valor_total, valor_disponivel=valor_total, data_publicacao=data_publicacao, data_inicio_inscricoes=data_inicio_inscricoes, data_fim_inscricoes=data_fim_inscricoes, vagas=vagas, descricao=descricao.strip(), fase=FaseEditalCultural.PUBLICADO, criterios=[item.strip() for item in criterios if item and item.strip()], documentos_necessarios=[item.strip() for item in documentos_necessarios if item and item.strip()])

    def abrir_inscricoes(self) -> None:
        self.fase = FaseEditalCultural.INSCRICOES_ABERTAS

    def encerrar_inscricoes(self) -> None:
        self.fase = FaseEditalCultural.INSCRICOES_ENCERRADAS

    def adicionar_inscricao(self, projeto_id: UUID) -> None:
        if self.fase != FaseEditalCultural.INSCRICOES_ABERTAS:
            raise ValueError('Inscricoes nao estao abertas para este edital')
        self.inscricoes.append(projeto_id)

    def publicar_resultado_final(self, selecionados: list[UUID]) -> None:
        if len(selecionados) > self.vagas:
            raise ValueError('Quantidade de selecionados excede vagas do edital')
        self.fase = FaseEditalCultural.RESULTADO_FINAL
        self.projetos_selecionados = list(selecionados)

    def dias_restantes_inscricao(self) -> int:
        hoje = datetime.utcnow()
        if hoje > self.data_fim_inscricoes:
            return 0
        return max(0, (self.data_fim_inscricoes - hoje).days)