from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural

@dataclass
class EspacoCultural:
    id: UUID
    codigo_espaco: str
    nome: str
    tipo: TipoEspacoCultural
    municipio: str
    provincia: str
    endereco: str
    capacidade: int
    area_m2: float
    administracao: str
    responsavel_cpf: str
    data_registro: date
    orgao_gestor: str | None = None
    ano_inauguracao: int | None = None
    acessibilidade: bool = False
    visitas_anuais: int = 0
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, codigo_espaco: str, nome: str, tipo: TipoEspacoCultural, municipio: str, provincia: str, endereco: str, capacidade: int, area_m2: float, administracao: str, responsavel_cpf: str, orgao_gestor: str | None=None, ano_inauguracao: int | None=None, acessibilidade: bool=False, observacoes: str | None=None) -> 'EspacoCultural':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do espaco cultural deve ter pelo menos 3 caracteres')
        if capacidade <= 0:
            raise ValueError('Capacidade deve ser positiva')
        if area_m2 <= 0:
            raise ValueError('Area m2 deve ser positiva')
        return cls(id=uuid4(), codigo_espaco=codigo_espaco.strip(), nome=nome_normalizado, tipo=tipo, municipio=municipio.strip(), provincia=provincia.strip(), endereco=endereco.strip(), capacidade=capacidade, area_m2=area_m2, administracao=administracao.strip().upper(), responsavel_cpf=responsavel_cpf.strip(), data_registro=date.today(), orgao_gestor=orgao_gestor.strip() if orgao_gestor else None, ano_inauguracao=ano_inauguracao, acessibilidade=acessibilidade, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, tipo: TipoEspacoCultural | None=None, municipio: str | None=None, provincia: str | None=None, endereco: str | None=None, capacidade: int | None=None, area_m2: float | None=None, administracao: str | None=None, responsavel_cpf: str | None=None, orgao_gestor: str | None=None, ano_inauguracao: int | None=None, acessibilidade: bool | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do espaco cultural deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if endereco is not None:
            self.endereco = endereco.strip()
        if capacidade is not None:
            if capacidade <= 0:
                raise ValueError('Capacidade deve ser positiva')
            self.capacidade = capacidade
        if area_m2 is not None:
            if area_m2 <= 0:
                raise ValueError('Area m2 deve ser positiva')
            self.area_m2 = area_m2
        if administracao is not None:
            self.administracao = administracao.strip().upper()
        if responsavel_cpf is not None:
            self.responsavel_cpf = responsavel_cpf.strip()
        if orgao_gestor is not None:
            self.orgao_gestor = orgao_gestor.strip() if orgao_gestor else None
        if ano_inauguracao is not None:
            self.ano_inauguracao = ano_inauguracao
        if acessibilidade is not None:
            self.acessibilidade = acessibilidade
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def registrar_visita(self) -> None:
        self.visitas_anuais += 1