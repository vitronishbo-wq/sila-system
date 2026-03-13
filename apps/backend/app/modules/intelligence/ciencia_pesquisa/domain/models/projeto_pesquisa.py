from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, StatusProjetoPesquisa

@dataclass
class ProjetoPesquisa:
    id: UUID
    codigo_projeto: str
    titulo: str
    resumo: str
    instituicao_id: UUID
    coordenador_id: UUID
    equipe_pesquisadores_ids: list[UUID]
    area_conhecimento: AreaConhecimento
    data_inicio: date
    data_fim_prevista: date | None = None
    data_fim_real: date | None = None
    status: StatusProjetoPesquisa = StatusProjetoPesquisa.SUBMETIDO
    palavras_chave: list[str] | None = None
    orcamento_previsto: float | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, codigo_projeto: str, titulo: str, resumo: str, instituicao_id: UUID, coordenador_id: UUID, equipe_pesquisadores_ids: list[UUID] | None=None, area_conhecimento: AreaConhecimento=AreaConhecimento.MULTIDISCIPLINAR, data_inicio: date | None=None, data_fim_prevista: date | None=None, palavras_chave: list[str] | None=None, orcamento_previsto: float | None=None) -> 'ProjetoPesquisa':
        titulo_normalizado = titulo.strip()
        if len(titulo_normalizado) < 5:
            raise ValueError('Titulo do projeto deve ter pelo menos 5 caracteres')
        resumo_normalizado = resumo.strip()
        if len(resumo_normalizado) < 10:
            raise ValueError('Resumo do projeto deve ter pelo menos 10 caracteres')
        inicio = data_inicio or date.today()
        if data_fim_prevista is not None and data_fim_prevista < inicio:
            raise ValueError('Data fim prevista nao pode ser anterior ao inicio')
        equipe = list(dict.fromkeys(equipe_pesquisadores_ids or []))
        if coordenador_id not in equipe:
            equipe.append(coordenador_id)
        return cls(id=uuid4(), codigo_projeto=codigo_projeto.strip(), titulo=titulo_normalizado, resumo=resumo_normalizado, instituicao_id=instituicao_id, coordenador_id=coordenador_id, equipe_pesquisadores_ids=equipe, area_conhecimento=area_conhecimento, data_inicio=inicio, data_fim_prevista=data_fim_prevista, data_fim_real=None, status=StatusProjetoPesquisa.SUBMETIDO, palavras_chave=[item.strip() for item in palavras_chave or [] if item.strip()], orcamento_previsto=orcamento_previsto, ativo=True)

    def aprovar(self) -> None:
        if self.status not in {StatusProjetoPesquisa.SUBMETIDO, StatusProjetoPesquisa.RASCUNHO}:
            raise ValueError('Projeto precisa estar submetido para aprovacao')
        self.status = StatusProjetoPesquisa.APROVADO
        self.ativo = True

    def iniciar_execucao(self) -> None:
        if self.status not in {StatusProjetoPesquisa.APROVADO, StatusProjetoPesquisa.SUBMETIDO}:
            raise ValueError('Projeto precisa estar aprovado/submetido para iniciar')
        self.status = StatusProjetoPesquisa.EM_EXECUCAO
        self.ativo = True

    def vincular_pesquisadores(self, pesquisador_ids: list[UUID]) -> None:
        for pesquisador_id in pesquisador_ids:
            if pesquisador_id not in self.equipe_pesquisadores_ids:
                self.equipe_pesquisadores_ids.append(pesquisador_id)
        if self.coordenador_id not in self.equipe_pesquisadores_ids:
            self.equipe_pesquisadores_ids.append(self.coordenador_id)

    def suspender(self) -> None:
        if self.status == StatusProjetoPesquisa.ENCERRADO:
            raise ValueError('Projeto encerrado nao pode ser suspenso')
        self.status = StatusProjetoPesquisa.SUSPENSO
        self.ativo = False

    def encerrar(self, *, data_fim_real: date | None=None) -> None:
        fim = data_fim_real or date.today()
        if fim < self.data_inicio:
            raise ValueError('Data de encerramento nao pode ser anterior ao inicio')
        self.data_fim_real = fim
        self.status = StatusProjetoPesquisa.ENCERRADO
        self.ativo = False