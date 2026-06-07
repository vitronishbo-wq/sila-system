from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    StatusMatriculaImovel,
    TipoRegistro,
)


@dataclass
class MatriculaImovel:
    id: UUID
    numero_matricula: str
    imovel_inscricao: str
    tipo_registro: TipoRegistro
    cartorio_nome: str
    livro: str
    folha: str
    comarca: str
    provincia: str
    data_registro: date
    status: StatusMatriculaImovel = StatusMatriculaImovel.ATIVA
    ativo: bool = True
    proprietario_documento: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        numero_matricula: str,
        imovel_inscricao: str,
        tipo_registro: TipoRegistro,
        cartorio_nome: str,
        livro: str,
        folha: str,
        comarca: str,
        provincia: str,
        proprietario_documento: str | None = None,
    ) -> MatriculaImovel:
        if not numero_matricula.strip():
            raise ValueError("Numero de matricula e obrigatorio")
        if not imovel_inscricao.strip():
            raise ValueError("Inscricao imobiliaria e obrigatoria")
        if not cartorio_nome.strip():
            raise ValueError("Nome do cartorio e obrigatorio")
        if not livro.strip() or not folha.strip():
            raise ValueError("Livro e folha sao obrigatorios")
        if not comarca.strip() or not provincia.strip():
            raise ValueError("Comarca e provincia sao obrigatorias")
        return cls(
            id=uuid4(),
            numero_matricula=numero_matricula.strip(),
            imovel_inscricao=imovel_inscricao.strip(),
            tipo_registro=tipo_registro,
            cartorio_nome=cartorio_nome.strip(),
            livro=livro.strip(),
            folha=folha.strip(),
            comarca=comarca.strip(),
            provincia=provincia.strip(),
            data_registro=date.today(),
            status=StatusMatriculaImovel.ATIVA,
            ativo=True,
            proprietario_documento=proprietario_documento.strip()
            if proprietario_documento
            else None,
        )

    def transferir(self, novo_documento: str) -> None:
        if not novo_documento.strip():
            raise ValueError("Documento do novo titular e obrigatorio")
        self.proprietario_documento = novo_documento.strip()
        self.status = StatusMatriculaImovel.TRANSFERIDA
        self.data_atualizacao = date.today()

    def cancelar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        if self.status == StatusMatriculaImovel.CANCELADA:
            raise ValueError("Matricula ja esta cancelada")
        self.status = StatusMatriculaImovel.CANCELADA
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
