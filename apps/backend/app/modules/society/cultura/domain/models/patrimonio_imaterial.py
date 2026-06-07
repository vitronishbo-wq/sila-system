from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.cultura.domain.enums import (
    CategoriaPatrimonioImaterial,
    StatusPatrimonioImaterial,
)


@dataclass
class PatrimonioImaterial:
    id: UUID
    registro_pni: str
    nome: str
    categoria: CategoriaPatrimonioImaterial
    descricao: str
    comunidade: str
    municipio: str
    provincia: str
    data_registro: date
    status: StatusPatrimonioImaterial = StatusPatrimonioImaterial.PROPOSTO
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    plano_salvaguarda: str | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        registro_pni: str,
        nome: str,
        categoria: CategoriaPatrimonioImaterial,
        descricao: str,
        comunidade: str,
        municipio: str,
        provincia: str,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        plano_salvaguarda: str | None = None,
        observacoes: str | None = None,
    ) -> PatrimonioImaterial:
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError("Nome do patrimonio imaterial deve ter pelo menos 3 caracteres")
        descricao_normalizada = descricao.strip()
        if len(descricao_normalizada) < 10:
            raise ValueError("Descricao do patrimonio imaterial deve ter pelo menos 10 caracteres")
        return cls(
            id=uuid4(),
            registro_pni=registro_pni.strip(),
            nome=nome_normalizado,
            categoria=categoria,
            descricao=descricao_normalizada,
            comunidade=comunidade.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_registro=date.today(),
            atracao_turistica_id=atracao_turistica_id,
            instituicao_educacional_id=instituicao_educacional_id,
            plano_salvaguarda=plano_salvaguarda.strip() if plano_salvaguarda else None,
            observacoes=observacoes.strip() if observacoes else None,
        )

    def atualizar(
        self,
        *,
        nome: str | None = None,
        categoria: CategoriaPatrimonioImaterial | None = None,
        descricao: str | None = None,
        comunidade: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        atracao_turistica_id: UUID | None = None,
        instituicao_educacional_id: UUID | None = None,
        plano_salvaguarda: str | None = None,
        status: StatusPatrimonioImaterial | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError("Nome do patrimonio imaterial deve ter pelo menos 3 caracteres")
            self.nome = nome_normalizado
        if categoria is not None:
            self.categoria = categoria
        if descricao is not None:
            descricao_normalizada = descricao.strip()
            if len(descricao_normalizada) < 10:
                raise ValueError(
                    "Descricao do patrimonio imaterial deve ter pelo menos 10 caracteres"
                )
            self.descricao = descricao_normalizada
        if comunidade is not None:
            self.comunidade = comunidade.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if atracao_turistica_id is not None:
            self.atracao_turistica_id = atracao_turistica_id
        if instituicao_educacional_id is not None:
            self.instituicao_educacional_id = instituicao_educacional_id
        if plano_salvaguarda is not None:
            self.plano_salvaguarda = plano_salvaguarda.strip() if plano_salvaguarda else None
        if status is not None:
            self.status = status
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None
