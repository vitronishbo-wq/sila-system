from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital


@dataclass
class Edital:
    id: UUID
    numero_edital: str
    titulo: str
    objeto: str
    licitacao_id: UUID
    status: StatusEdital
    data_publicacao: date
    data_abertura: date
    data_encerramento: date
    data_cadastro: date
    versao: int = 1
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def publicar(
        cls,
        *,
        numero_edital: str,
        titulo: str,
        objeto: str,
        licitacao_id: UUID,
        data_publicacao: date,
        data_abertura: date,
        data_encerramento: date,
    ) -> Edital:
        if not numero_edital.strip():
            raise ValueError("Numero do edital e obrigatorio")
        if not titulo.strip():
            raise ValueError("Titulo do edital e obrigatorio")
        if not objeto.strip():
            raise ValueError("Objeto do edital e obrigatorio")
        if data_abertura < data_publicacao:
            raise ValueError("Data de abertura nao pode ser menor que data de publicacao")
        if data_encerramento <= data_abertura:
            raise ValueError("Data de encerramento deve ser maior que abertura")
        return cls(
            id=uuid4(),
            numero_edital=numero_edital.strip(),
            titulo=titulo.strip(),
            objeto=objeto.strip(),
            licitacao_id=licitacao_id,
            status=StatusEdital.PUBLICADO,
            data_publicacao=data_publicacao,
            data_abertura=data_abertura,
            data_encerramento=data_encerramento,
            data_cadastro=date.today(),
            versao=1,
        )

    def impugnar(self, motivo: str) -> None:
        if self.status not in {StatusEdital.PUBLICADO, StatusEdital.RETIFICADO}:
            raise ValueError("Edital nao pode ser impugnado neste status")
        if not motivo.strip():
            raise ValueError("Motivo da impugnacao e obrigatorio")
        self.status = StatusEdital.IMPUGNADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def retificar(self, descricao: str) -> None:
        if self.status not in {
            StatusEdital.PUBLICADO,
            StatusEdital.IMPUGNADO,
            StatusEdital.RETIFICADO,
        }:
            raise ValueError("Edital nao pode ser retificado neste status")
        if not descricao.strip():
            raise ValueError("Descricao da retificacao e obrigatoria")
        self.status = StatusEdital.RETIFICADO
        self.versao += 1
        self.observacoes = descricao.strip()
        self.data_atualizacao = date.today()

    def suspender(self, motivo: str) -> None:
        if self.status not in {
            StatusEdital.PUBLICADO,
            StatusEdital.IMPUGNADO,
            StatusEdital.RETIFICADO,
        }:
            raise ValueError("Edital nao pode ser suspenso neste status")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusEdital.SUSPENSO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def revogar(self, motivo: str) -> None:
        if self.status in {StatusEdital.REVOGADO, StatusEdital.ENCERRADO}:
            raise ValueError("Edital nao pode ser revogado neste status")
        if not motivo.strip():
            raise ValueError("Motivo da revogacao e obrigatorio")
        self.status = StatusEdital.REVOGADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def encerrar(self, *, data_encerramento: date | None = None) -> None:
        if self.status in {StatusEdital.REVOGADO, StatusEdital.ENCERRADO}:
            raise ValueError("Edital nao pode ser encerrado neste status")
        data_ref = data_encerramento or date.today()
        if data_ref < self.data_abertura:
            raise ValueError("Data de encerramento nao pode ser menor que abertura")
        self.status = StatusEdital.ENCERRADO
        self.data_encerramento = data_ref
        self.data_atualizacao = date.today()
