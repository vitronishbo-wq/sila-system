from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.society.desporto.domain.enums import (
    ModalidadeDesportiva,
    StatusCompeticao,
    TipoCompeticao,
)


@dataclass
class Competicao:
    id: UUID
    codigo_competicao: str
    nome: str
    tipo: TipoCompeticao
    modalidade: ModalidadeDesportiva
    data_inicio: date
    data_fim: date
    municipio: str
    provincia: str
    organizador_id: UUID
    data_cadastro: date
    status: StatusCompeticao = StatusCompeticao.PLANEADA
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    premiacao_total: Decimal | None = None
    inscricoes_abertas: bool = False
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        codigo_competicao: str,
        nome: str,
        tipo: TipoCompeticao,
        modalidade: ModalidadeDesportiva,
        data_inicio: date,
        data_fim: date,
        municipio: str,
        provincia: str,
        organizador_id: UUID,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        premiacao_total: Decimal | None = None,
        observacoes: str | None = None,
    ) -> Competicao:
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError("Nome da competicao deve ter pelo menos 3 caracteres")
        if data_fim < data_inicio:
            raise ValueError("Data fim nao pode ser anterior a data inicio")
        if premiacao_total is not None and premiacao_total < 0:
            raise ValueError("Premiacao total nao pode ser negativa")
        return cls(
            id=uuid4(),
            codigo_competicao=codigo_competicao.strip(),
            nome=nome_normalizado,
            tipo=tipo,
            modalidade=modalidade,
            data_inicio=data_inicio,
            data_fim=data_fim,
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            organizador_id=organizador_id,
            data_cadastro=date.today(),
            codigo_obra_instalacao=codigo_obra_instalacao.strip()
            if codigo_obra_instalacao
            else None,
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
            premiacao_total=premiacao_total,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        nome: str | None = None,
        tipo: TipoCompeticao | None = None,
        modalidade: ModalidadeDesportiva | None = None,
        data_inicio: date | None = None,
        data_fim: date | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        codigo_obra_instalacao: str | None = None,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        premiacao_total: Decimal | None = None,
        inscricoes_abertas: bool | None = None,
        status: StatusCompeticao | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        novo_inicio = data_inicio or self.data_inicio
        novo_fim = data_fim or self.data_fim
        if novo_fim < novo_inicio:
            raise ValueError("Data fim nao pode ser anterior a data inicio")
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError("Nome da competicao deve ter pelo menos 3 caracteres")
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if modalidade is not None:
            self.modalidade = modalidade
        if data_inicio is not None:
            self.data_inicio = data_inicio
        if data_fim is not None:
            self.data_fim = data_fim
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if codigo_obra_instalacao is not None:
            self.codigo_obra_instalacao = (
                codigo_obra_instalacao.strip() if codigo_obra_instalacao else None
            )
        if atracao_turistica_id is not None:
            self.atracao_turistica_id = atracao_turistica_id
        if instituicao_educacional_id is not None:
            self.instituicao_educacional_id = instituicao_educacional_id
        if premiacao_total is not None:
            if premiacao_total < 0:
                raise ValueError("Premiacao total nao pode ser negativa")
            self.premiacao_total = premiacao_total
        if inscricoes_abertas is not None:
            self.inscricoes_abertas = inscricoes_abertas
        if status is not None:
            self.status = status
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
