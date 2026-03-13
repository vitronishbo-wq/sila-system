from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.economy.trade.services.domain.enums import PorteComercial, RamoComercial, StatusComercial, TipoEstabelecimentoComercial, TipoRegimeTributario
from app.modules.economy.trade.services.domain.models.porte_comercial import PorteComercio
from app.modules.economy.trade.services.domain.models.ramo_comercial import RamoComercio

@dataclass
class EstabelecimentoComercial:
    id: UUID
    cnpj: str
    razao_social: str
    tipo: TipoEstabelecimentoComercial
    ramo: RamoComercial
    porte: PorteComercial
    regime_tributario: TipoRegimeTributario
    cnae_principal: str
    data_abertura: date
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    status: StatusComercial = StatusComercial.LICENCIAMENTO
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    nome_fantasia: str | None = None
    cnaes_secundarios: list[str] | None = None
    data_inicio_atividades: date | None = None
    data_encerramento: date | None = None
    complemento: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    telefone: str | None = None
    celular: str | None = None
    email: str | None = None
    site: str | None = None
    redes_sociais: dict | None = None
    horario_funcionamento: dict | None = None
    dias_funcionamento: list[str] | None = None
    area_m2: Decimal | None = None
    numero_funcionarios: int | None = None
    faturamento_medio_mensal: Decimal | None = None
    matriz_id: UUID | None = None
    franquia_id: UUID | None = None
    grupo_economico_id: UUID | None = None
    proprietario_id: UUID | None = None
    proprietario_tipo: str | None = None
    alvara_id: UUID | None = None
    licenca_sanitaria_id: UUID | None = None
    licenca_ambiental_id: UUID | None = None
    certificacoes: list[UUID] | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    audit_log: list[str] = field(default_factory=list)
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, cnpj: str, razao_social: str, tipo: TipoEstabelecimentoComercial, ramo: RamoComercial, porte: PorteComercial, regime_tributario: TipoRegimeTributario, cnae_principal: str, data_abertura: date, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str) -> 'EstabelecimentoComercial':
        if not cnpj.strip():
            raise ValueError('CNPJ e obrigatorio')
        if not razao_social.strip():
            raise ValueError('Razao social e obrigatoria')
        if not cnae_principal.strip():
            raise ValueError('CNAE principal e obrigatorio')
        item = cls(id=uuid4(), cnpj=cnpj.strip(), razao_social=razao_social.strip(), tipo=tipo, ramo=ramo, porte=porte, regime_tributario=regime_tributario, cnae_principal=cnae_principal.strip(), data_abertura=data_abertura, endereco=endereco.strip(), numero=numero.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip(), cep=cep.strip())
        item._registrar_evento('Cadastro inicial do estabelecimento comercial')
        return item

    def iniciar_atividades(self, data_inicio: date) -> None:
        if self.status != StatusComercial.LICENCIAMENTO:
            raise ValueError('Estabelecimento precisa estar em licenciamento')
        self.status = StatusComercial.ATIVO
        self.data_inicio_atividades = data_inicio
        self._registrar_evento(f'Transicao de status: licenciamento -> ativo (data_inicio={data_inicio.isoformat()})')

    def suspender_atividades(self, motivo: str) -> None:
        if self.status != StatusComercial.ATIVO:
            raise ValueError('Apenas estabelecimentos ativos podem ser suspensos')
        if not motivo.strip():
            raise ValueError('Motivo da suspensao e obrigatorio')
        self.status = StatusComercial.SUSPENSO
        self.observacoes = motivo.strip()
        self._registrar_evento('Transicao de status: ativo -> suspenso')

    def encerrar(self, *, data_encerramento: date, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo do encerramento e obrigatorio')
        self.status = StatusComercial.INATIVO
        self.data_encerramento = data_encerramento
        self.observacoes = motivo.strip()
        self._registrar_evento(f'Transicao de status: -> inativo (data_encerramento={data_encerramento.isoformat()})')

    def atualizar_dados_cadastrais(self, *, nome_fantasia: str | None=None, telefone: str | None=None, email: str | None=None, endereco: str | None=None) -> None:
        if nome_fantasia is not None:
            self.nome_fantasia = nome_fantasia.strip() or None
        if telefone is not None:
            self.telefone = telefone.strip() or None
        if email is not None:
            self.email = email.strip() or None
        if endereco is not None:
            self.endereco = endereco.strip() or self.endereco
        self._registrar_evento('Atualizacao de dados cadastrais')

    def vincular_alvara(self, alvara_id: UUID) -> None:
        self.alvara_id = alvara_id
        self._registrar_evento(f'Alvara vinculado: {alvara_id}')

    def adicionar_certificacao(self, certificacao_id: UUID) -> None:
        if not self.certificacoes:
            self.certificacoes = []
        self.certificacoes.append(certificacao_id)
        self._registrar_evento(f'Certificacao adicionada: {certificacao_id}')

    def associar_ramo(self, ramo: RamoComercio) -> None:
        anterior = self.ramo
        self.ramo = ramo.codigo
        self._registrar_evento(f'Ramo associado: {anterior.value} -> {ramo.codigo.value} ({ramo.descricao})')

    def definir_porte(self, porte: PorteComercio) -> None:
        anterior = self.porte
        self.porte = porte.codigo
        self._registrar_evento(f'Porte definido: {anterior.value} -> {porte.codigo.value} ({porte.descricao})')

    def _registrar_evento(self, mensagem: str) -> None:
        self.updated_at = datetime.now(UTC)
        self.audit_log.append(f'{self.updated_at.isoformat()} - {mensagem}')