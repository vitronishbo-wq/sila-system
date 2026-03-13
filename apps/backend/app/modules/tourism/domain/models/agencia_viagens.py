from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class AgenciaViagens:
    id: UUID
    registro: str
    nome_fantasia: str
    razao_social: str
    cnpj: str
    email: str
    telefone: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    proprietario_id: UUID
    data_registro: date
    ativa: bool = True
    especialidades: list[str] | None = None
    site: str | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome_fantasia: str, razao_social: str, cnpj: str, email: str, telefone: str, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str, proprietario_id: UUID, especialidades: list[str] | None=None, site: str | None=None, observacoes: str | None=None) -> 'AgenciaViagens':
        return cls(id=uuid4(), registro='', nome_fantasia=nome_fantasia.strip(), razao_social=razao_social.strip(), cnpj=cnpj.strip(), email=email.strip().lower(), telefone=telefone.strip(), endereco=endereco.strip(), numero=numero.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), cep=cep.strip(), proprietario_id=proprietario_id, data_registro=date.today(), ativa=True, especialidades=list(especialidades or []), site=site.strip() if site else None, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome_fantasia: str | None=None, razao_social: str | None=None, email: str | None=None, telefone: str | None=None, endereco: str | None=None, numero: str | None=None, bairro: str | None=None, municipio: str | None=None, provincia: str | None=None, cep: str | None=None, especialidades: list[str] | None=None, site: str | None=None, observacoes: str | None=None) -> None:
        if nome_fantasia is not None:
            self.nome_fantasia = nome_fantasia.strip()
        if razao_social is not None:
            self.razao_social = razao_social.strip()
        if email is not None:
            self.email = email.strip().lower()
        if telefone is not None:
            self.telefone = telefone.strip()
        if endereco is not None:
            self.endereco = endereco.strip()
        if numero is not None:
            self.numero = numero.strip()
        if bairro is not None:
            self.bairro = bairro.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if cep is not None:
            self.cep = cep.strip()
        if especialidades is not None:
            self.especialidades = list(especialidades)
        if site is not None:
            self.site = site.strip() if site else None
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def ativar(self) -> None:
        self.ativa = True

    def desativar(self) -> None:
        self.ativa = False