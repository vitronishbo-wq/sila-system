from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.industry.domain.enums import PorteIndustrial, RamoIndustrial, StatusEstabelecimento, TipoEstabelecimento
from apps.backend.app.modules.industry.domain.models.porte_industrial import Porte
from apps.backend.app.modules.industry.domain.models.ramo_industrial import Ramo

@dataclass
class EstabelecimentoIndustrial:
    id: UUID
    cnpj: str
    razao_social: str
    ramo: RamoIndustrial
    porte: PorteIndustrial
    tipo: TipoEstabelecimento
    cnae_principal: str
    data_abertura: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    status: StatusEstabelecimento = StatusEstabelecimento.LICENCIAMENTO
    nome_fantasia: str | None = None
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    telefone: str | None = None
    email: str | None = None
    data_inicio_atividades: date | None = None
    data_encerramento: date | None = None
    consumo_medio_energia_kwh: Decimal | None = None
    consumo_medio_agua_m3: Decimal | None = None
    licenca_operacao_id: UUID | None = None
    licenca_ambiental_id: UUID | None = None
    alvara_id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    audit_log: list[str] = field(default_factory=list)
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, cnpj: str, razao_social: str, ramo: RamoIndustrial, porte: PorteIndustrial, tipo: TipoEstabelecimento, cnae_principal: str, data_abertura: date, endereco: str, bairro: str, municipio: str, provincia: str) -> 'EstabelecimentoIndustrial':
        if not cnpj.strip():
            raise ValueError('CNPJ e obrigatorio')
        if not razao_social.strip():
            raise ValueError('Razao social e obrigatoria')
        if not cnae_principal.strip():
            raise ValueError('CNAE principal e obrigatorio')
        if not endereco.strip():
            raise ValueError('Endereco e obrigatorio')
        item = cls(id=uuid4(), cnpj=cnpj.strip(), razao_social=razao_social.strip(), ramo=ramo, porte=porte, tipo=tipo, cnae_principal=cnae_principal.strip(), data_abertura=data_abertura, endereco=endereco.strip(), bairro=bairro.strip(), municipio=municipio.strip(), provincia=provincia.strip())
        item._registrar_evento('Cadastro inicial do estabelecimento industrial')
        return item

    def iniciar_atividades(self, data_inicio: date) -> None:
        if self.status != StatusEstabelecimento.LICENCIAMENTO:
            raise ValueError('Estabelecimento precisa estar em licenciamento')
        self.status = StatusEstabelecimento.ATIVO
        self.data_inicio_atividades = data_inicio
        self._registrar_evento(f'Transicao de status: licenciamento -> ativo (data_inicio={data_inicio.isoformat()})')

    def suspender_atividades(self, motivo: str) -> None:
        if self.status != StatusEstabelecimento.ATIVO:
            raise ValueError('Apenas estabelecimentos ativos podem ser suspensos')
        if not motivo.strip():
            raise ValueError('Motivo da suspensao e obrigatorio')
        self.status = StatusEstabelecimento.SUSPENSO
        self.observacoes = motivo.strip()
        self._registrar_evento('Transicao de status: ativo -> suspenso')

    def paralisar(self, motivo: str) -> None:
        if self.status != StatusEstabelecimento.ATIVO:
            raise ValueError('Apenas estabelecimentos ativos podem ser paralisados')
        if not motivo.strip():
            raise ValueError('Motivo da paralisacao e obrigatorio')
        self.status = StatusEstabelecimento.PARALISADO
        self.observacoes = motivo.strip()
        self._registrar_evento('Transicao de status: ativo -> paralisado')

    def reativar(self) -> None:
        if self.status not in (StatusEstabelecimento.SUSPENSO, StatusEstabelecimento.PARALISADO):
            raise ValueError('Apenas estabelecimentos suspensos ou paralisados podem ser reativados')
        self.status = StatusEstabelecimento.ATIVO
        self._registrar_evento('Transicao de status: suspenso/paralisado -> ativo')

    def encerrar(self, *, data_encerramento: date, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo do encerramento e obrigatorio')
        self.status = StatusEstabelecimento.INATIVO
        self.data_encerramento = data_encerramento
        self.observacoes = motivo.strip()
        self._registrar_evento(f'Transicao de status: -> inativo (data_encerramento={data_encerramento.isoformat()})')

    def atualizar_dados_cadastrais(self, *, nome_fantasia: str | None=None, inscricao_estadual: str | None=None, inscricao_municipal: str | None=None, endereco: str | None=None, telefone: str | None=None, email: str | None=None) -> None:
        if nome_fantasia is not None:
            self.nome_fantasia = nome_fantasia.strip() or None
        if inscricao_estadual is not None:
            self.inscricao_estadual = inscricao_estadual.strip() or None
        if inscricao_municipal is not None:
            self.inscricao_municipal = inscricao_municipal.strip() or None
        if endereco is not None:
            self.endereco = endereco.strip() or self.endereco
        if telefone is not None:
            self.telefone = telefone.strip() or None
        if email is not None:
            self.email = email.strip() or None

    def vincular_licenca_operacao(self, licenca_id: UUID) -> None:
        self.licenca_operacao_id = licenca_id
        self._registrar_evento(f'Licenca de operacao vinculada: {licenca_id}')

    def vincular_licenca_ambiental(self, licenca_id: UUID) -> None:
        self.licenca_ambiental_id = licenca_id
        self._registrar_evento(f'Licenca ambiental vinculada: {licenca_id}')

    def vincular_alvara(self, alvara_id: UUID) -> None:
        self.alvara_id = alvara_id
        self._registrar_evento(f'Alvara vinculado: {alvara_id}')

    def associar_ramo(self, ramo: Ramo) -> None:
        anterior = self.ramo
        self.ramo = ramo.codigo
        self._registrar_evento(f'Ramo associado: {anterior.value} -> {ramo.codigo.value} ({ramo.descricao})')

    def definir_porte(self, porte: Porte) -> None:
        anterior = self.porte
        self.porte = porte.codigo
        self._registrar_evento(f'Porte definido: {anterior.value} -> {porte.codigo.value} ({porte.descricao})')

    def _registrar_evento(self, mensagem: str) -> None:
        self.updated_at = datetime.now(UTC)
        self.audit_log.append(f'{self.updated_at.isoformat()} - {mensagem}')