from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, PePreferencial, PosicaoAtleta, StatusAtleta, TipoAtleta

@dataclass
class Atleta:
    id: UUID
    numero_registro: str
    nome: str
    data_nascimento: date
    naturalidade: str
    nacionalidade: str
    tipo: TipoAtleta
    modalidades: list[ModalidadeDesportiva]
    data_cadastro: date
    status: StatusAtleta = StatusAtleta.ATIVO
    posicoes: list[PosicaoAtleta] | None = None
    pe_preferencial: PePreferencial | None = None
    altura_cm: int | None = None
    peso_kg: Decimal | None = None
    clube_atual_id: UUID | None = None
    numero_camisola: int | None = None
    citizen_id: UUID | None = None
    ultimo_exame_id: UUID | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, numero_registro: str, nome: str, data_nascimento: date, naturalidade: str, nacionalidade: str, tipo: TipoAtleta, modalidades: list[ModalidadeDesportiva], citizen_id: UUID | None=None, posicoes: list[PosicaoAtleta] | None=None, pe_preferencial: PePreferencial | None=None, altura_cm: int | None=None, peso_kg: Decimal | None=None, clube_atual_id: UUID | None=None, numero_camisola: int | None=None, ultimo_exame_id: UUID | None=None, observacoes: str | None=None) -> 'Atleta':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do atleta deve ter pelo menos 3 caracteres')
        if data_nascimento >= date.today():
            raise ValueError('Data de nascimento deve ser anterior a hoje')
        if not modalidades:
            raise ValueError('Pelo menos uma modalidade e obrigatoria')
        if altura_cm is not None and altura_cm <= 0:
            raise ValueError('Altura deve ser maior que zero')
        if peso_kg is not None and peso_kg <= 0:
            raise ValueError('Peso deve ser maior que zero')
        return cls(id=uuid4(), numero_registro=numero_registro.strip(), nome=nome_normalizado, data_nascimento=data_nascimento, naturalidade=naturalidade.strip(), nacionalidade=nacionalidade.strip() or 'Angolana', tipo=tipo, modalidades=modalidades, data_cadastro=date.today(), citizen_id=citizen_id, posicoes=list(dict.fromkeys(posicoes)) if posicoes else None, pe_preferencial=pe_preferencial, altura_cm=altura_cm, peso_kg=peso_kg, clube_atual_id=clube_atual_id, numero_camisola=numero_camisola, ultimo_exame_id=ultimo_exame_id, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, tipo: TipoAtleta | None=None, modalidades: list[ModalidadeDesportiva] | None=None, posicoes: list[PosicaoAtleta] | None=None, pe_preferencial: PePreferencial | None=None, altura_cm: int | None=None, peso_kg: Decimal | None=None, clube_atual_id: UUID | None=None, numero_camisola: int | None=None, status: StatusAtleta | None=None, ultimo_exame_id: UUID | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do atleta deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if modalidades is not None:
            if not modalidades:
                raise ValueError('Pelo menos uma modalidade e obrigatoria')
            self.modalidades = modalidades
        if posicoes is not None:
            self.posicoes = list(dict.fromkeys(posicoes)) if posicoes else None
        if pe_preferencial is not None:
            self.pe_preferencial = pe_preferencial
        if altura_cm is not None:
            if altura_cm <= 0:
                raise ValueError('Altura deve ser maior que zero')
            self.altura_cm = altura_cm
        if peso_kg is not None:
            if peso_kg <= 0:
                raise ValueError('Peso deve ser maior que zero')
            self.peso_kg = peso_kg
        if clube_atual_id is not None:
            self.clube_atual_id = clube_atual_id
        if numero_camisola is not None:
            self.numero_camisola = numero_camisola
        if status is not None:
            self.status = status
        if ultimo_exame_id is not None:
            self.ultimo_exame_id = ultimo_exame_id
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def registrar_lesao(self) -> None:
        self.status = StatusAtleta.LESIONADO

    def recuperar(self) -> None:
        self.status = StatusAtleta.ATIVO