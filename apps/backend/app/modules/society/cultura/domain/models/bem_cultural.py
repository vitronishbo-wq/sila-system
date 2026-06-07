from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio


@dataclass
class BemCultural:
    id: UUID
    registro_ipat: str
    nome: str
    tipo: TipoPatrimonio
    descricao: str
    localizacao: str
    municipio: str
    provincia: str
    data_cadastro: date
    status_tombamento: StatusTombamento = StatusTombamento.PROPOSTO
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    tombamento_id: UUID | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        registro: str,
        nome: str,
        tipo: TipoPatrimonio,
        descricao: str,
        localizacao: str,
        municipio: str,
        provincia: str,
        coordenadas_lat: Decimal | None = None,
        coordenadas_long: Decimal | None = None,
        observacoes: str | None = None,
    ) -> BemCultural:
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError("Nome do bem cultural deve ter pelo menos 3 caracteres")
        if not descricao.strip():
            raise ValueError("Descricao do bem cultural e obrigatoria")
        return cls(
            id=uuid4(),
            registro_ipat=registro.strip(),
            nome=nome_normalizado,
            tipo=tipo,
            descricao=descricao.strip(),
            localizacao=localizacao.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_cadastro=date.today(),
            coordenadas_lat=coordenadas_lat,
            coordenadas_long=coordenadas_long,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        nome: str | None = None,
        tipo: TipoPatrimonio | None = None,
        descricao: str | None = None,
        localizacao: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        coordenadas_lat: Decimal | None = None,
        coordenadas_long: Decimal | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError("Nome do bem cultural deve ter pelo menos 3 caracteres")
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if descricao is not None:
            descricao_normalizada = descricao.strip()
            if not descricao_normalizada:
                raise ValueError("Descricao do bem cultural e obrigatoria")
            self.descricao = descricao_normalizada
        if localizacao is not None:
            self.localizacao = localizacao.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if coordenadas_lat is not None:
            self.coordenadas_lat = coordenadas_lat
        if coordenadas_long is not None:
            self.coordenadas_long = coordenadas_long
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def tombar(self, tombamento_id: UUID) -> None:
        self.tombamento_id = tombamento_id
        self.status_tombamento = StatusTombamento.TOMBADO
