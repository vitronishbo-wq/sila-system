from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import Escolaridade, FaixaEtaria, SituacaoOcupacional, TipoVulnerabilidade

@dataclass
class Jovem:
    id: UUID
    numero_registro: str
    nome: str
    data_nascimento: date
    faixa_etaria: FaixaEtaria
    genero: str
    naturalidade: str
    escolaridade: Escolaridade
    situacao_ocupacional: SituacaoOcupacional
    endereco: str
    municipio: str
    provincia: str
    data_cadastro: date
    nacionalidade: str = 'Angolana'
    telefone: str | None = None
    email: str | None = None
    citizen_id: UUID | None = None
    vulnerabilidades: list[TipoVulnerabilidade] | None = None
    programas: list[UUID] | None = None
    auxilios: list[UUID] | None = None
    formacoes: list[UUID] | None = None
    experiencias: list[dict] | None = None
    interesses: list[str] | None = None
    habilidades: list[str] | None = None
    encaminhamentos: list[dict] | None = None
    acompanhamento_psicossocial: bool = False
    observacoes: str | None = None
    ativo: bool = True

    @staticmethod
    def calcular_faixa_etaria(data_nascimento: date) -> FaixaEtaria:
        idade = (date.today() - data_nascimento).days // 365
        if idade < 15:
            raise ValueError('Idade minima para cadastro de juventude e 15 anos')
        if idade > 35:
            raise ValueError('Idade maxima para cadastro de juventude e 35 anos')
        if idade <= 17:
            return FaixaEtaria.JOVEM_15_17
        if idade <= 24:
            return FaixaEtaria.JOVEM_18_24
        if idade <= 29:
            return FaixaEtaria.JOVEM_25_29
        return FaixaEtaria.JOVEM_30_35

    @classmethod
    def cadastrar(cls, *, numero_registro: str, nome: str, data_nascimento: date, genero: str, naturalidade: str, escolaridade: Escolaridade, situacao_ocupacional: SituacaoOcupacional, endereco: str, municipio: str, provincia: str, nacionalidade: str='Angolana', telefone: str | None=None, email: str | None=None, citizen_id: UUID | None=None, observacoes: str | None=None) -> 'Jovem':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do jovem deve ter pelo menos 3 caracteres')
        if data_nascimento >= date.today():
            raise ValueError('Data de nascimento deve ser anterior a hoje')
        return cls(id=uuid4(), numero_registro=numero_registro.strip(), nome=nome_normalizado, data_nascimento=data_nascimento, faixa_etaria=cls.calcular_faixa_etaria(data_nascimento), genero=genero.strip(), naturalidade=naturalidade.strip(), escolaridade=escolaridade, situacao_ocupacional=situacao_ocupacional, endereco=endereco.strip(), municipio=municipio.strip(), provincia=provincia.strip(), data_cadastro=date.today(), nacionalidade=nacionalidade.strip() or 'Angolana', telefone=telefone.strip() if telefone else None, email=email.strip().lower() if email else None, citizen_id=citizen_id, observacoes=observacoes.strip() if observacoes else None)

    def atualizar_escolaridade(self, nova_escolaridade: Escolaridade) -> None:
        self.escolaridade = nova_escolaridade

    def atualizar_situacao_ocupacional(self, nova_situacao: SituacaoOcupacional) -> None:
        self.situacao_ocupacional = nova_situacao

    def atualizar_contato(self, *, telefone: str | None=None, email: str | None=None) -> None:
        if telefone is not None:
            self.telefone = telefone.strip() or None
        if email is not None:
            self.email = email.strip().lower() or None

    def adicionar_vulnerabilidade(self, vulnerabilidade: TipoVulnerabilidade) -> None:
        if self.vulnerabilidades is None:
            self.vulnerabilidades = []
        if vulnerabilidade not in self.vulnerabilidades:
            self.vulnerabilidades.append(vulnerabilidade)

    def adicionar_auxilio(self, auxilio_id: UUID) -> None:
        if self.auxilios is None:
            self.auxilios = []
        if auxilio_id not in self.auxilios:
            self.auxilios.append(auxilio_id)