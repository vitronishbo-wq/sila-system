from apps.backend.app.core.observability import trace
import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID
from ....domain.models.invoice import Invoice
from ....domain.models.enums import InvoiceStatus
from ....domain.ports.invoice_repository_port import InvoiceRepositoryPort
from ....domain.ports.educacao_service_port import EducacaoServicePort
from ....domain.ports.juventude_service_port import JuventudeServicePort
from ....domain.ports.emprego_service_port import EmpregoServicePort
from ....domain.ports.saude_service_port import SaudeServicePort
from ....domain.ports.assistencia_social_service_port import AssistenciaSocialServicePort
from ....domain.ports.service_requests_service_port import ServiceRequestsServicePort
from ....domain.ports.identidade_service_port import IdentidadeServicePort
from ....application.dto.invoice_schema import CreateInvoiceSchema
from ....domain.exceptions import InvoiceNotFoundError, DomainValidationError, FUCError
from ....domain.integrations.fuc_client import FUCClient
logger = logging.getLogger(__name__)

class InvoiceService:
    """
    Serviço de Orquestração de Faturas (Motor SILA).
    Garante conformidade com normas: Tesouro Nacional + Ficheiro Único do Cidadão (FUC).

    REGRAS FINANCEIRAS:
    1. Cidadão deve estar ATIVO no FUC para receber faturas
    2. Montante deve ser > 0 (validado no domínio também)
    3. Status válidos: PENDING → (PAID | CANCELLED | OVERDUE)
    4. PAID e CANCELLED são estados finais (sem transições adicionais)
    """

    def __init__(self, repository: InvoiceRepositoryPort, educacao_service: EducacaoServicePort | None=None, juventude_service: JuventudeServicePort | None=None, emprego_service: EmpregoServicePort | None=None, saude_service: SaudeServicePort | None=None, assistencia_social_service: AssistenciaSocialServicePort | None=None, service_requests_service: ServiceRequestsServicePort | None=None, identidade_service: IdentidadeServicePort | None=None):
        self.repository = repository
        self.fuc_client = FUCClient()
        self.educacao_service = educacao_service
        self.juventude_service = juventude_service
        self.emprego_service = emprego_service
        self.saude_service = saude_service
        self.assistencia_social_service = assistencia_social_service
        self.service_requests_service = service_requests_service
        self.identidade_service = identidade_service

    @trace()
    async def create_invoice(self, data: CreateInvoiceSchema) -> Invoice:
        """
        Emite uma nova fatura oficial com validações financeiras.

        Precondições:
        - Cidadão ATIVO no FUC
        - Montante > 0
        - Códigos orçamentais válidos
        """
        logger.info(f'Iniciando emissão de fatura para cidadão: {data.citizen_id}')
        await self._validate_citizen_identity(data.citizen_id)
        try:
            is_valid = await self.fuc_client.validate_citizen(data.citizen_id)
            if not is_valid:
                logger.warning(f'Emissão negada: Cidadão {data.citizen_id} inválido ou inativo no FUC.')
                raise DomainValidationError(f'Cidadão {data.citizen_id} não habilitado para emissão de faturas.')
        except DomainValidationError:
            raise
        except Exception as e:
            logger.error(f'Falha na integração FUC: {str(e)}')
            raise FUCError('Serviço de validação de identidade indisponível. Tente novamente mais tarde.')
        year = datetime.now(timezone.utc).year
        unique_suffix = str(uuid.uuid4()).split('-')[0].upper()
        reference = f'SILA-{year}-{data.service_code}-{unique_suffix}'
        invoice = Invoice(id=str(uuid.uuid4()), citizen_id=data.citizen_id, reference=reference, revenue_code=data.revenue_code, cost_center=data.cost_center, service_code=data.service_code, service_name=data.service_name, amount=data.amount, currency=data.currency, due_date=data.due_date, request_id=data.request_id, status=InvoiceStatus.PENDING, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
        saved_invoice = await self.repository.create(invoice)
        logger.info(f'Fatura {saved_invoice.reference} emitida: {saved_invoice.id}')
        return saved_invoice

    @trace()
    async def create_educacao_tuition_invoice(self, *, matricula_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Propina Escolar') -> Invoice:
        if self.educacao_service is None:
            raise DomainValidationError('Integração com Educação não configurada')
        matricula = await self.educacao_service.get_matricula(matricula_id)
        if matricula is None:
            raise DomainValidationError('Matrícula não encontrada no módulo Educação')
        amount = await self.educacao_service.get_valor_propina(matricula_id)
        if amount <= 0:
            raise DomainValidationError('Valor de propina inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='EDU_PROPINA', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc) + timedelta(days=30), revenue_code=revenue_code, cost_center=cost_center, request_id=str(matricula_id))

    @trace()
    async def create_juventude_scholarship_invoice(self, *, referencia_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Bolsa/Auxílio Juventude') -> Invoice:
        if self.juventude_service is None:
            raise DomainValidationError('Integração com Juventude não configurada')
        beneficio = await self.juventude_service.get_bolsa(referencia_id)
        if beneficio is None:
            raise DomainValidationError('Benefício não encontrado no módulo Juventude')
        amount = await self.juventude_service.get_valor_bolsa(referencia_id)
        if amount <= 0:
            raise DomainValidationError('Valor de bolsa/auxílio inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='JUV_BOLSA', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc), revenue_code=revenue_code, cost_center=cost_center, request_id=str(referencia_id))

    @trace()
    async def create_emprego_salary_invoice(self, *, contrato_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Salário Emprego') -> Invoice:
        if self.emprego_service is None:
            raise DomainValidationError('Integração com Emprego não configurada')
        contrato = await self.emprego_service.get_contrato(contrato_id)
        if contrato is None:
            raise DomainValidationError('Contrato não encontrado no módulo Emprego')
        amount = await self.emprego_service.get_valor_salario(contrato_id)
        if amount <= 0:
            raise DomainValidationError('Valor salarial inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='EMP_SALARIO', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc), revenue_code=revenue_code, cost_center=cost_center, request_id=str(contrato_id))

    @trace()
    async def create_saude_service_invoice(self, *, atendimento_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Taxa de Serviço de Saúde') -> Invoice:
        if self.saude_service is None:
            raise DomainValidationError('Integração com Saúde não configurada')
        atendimento = await self.saude_service.get_atendimento(atendimento_id)
        if atendimento is None:
            raise DomainValidationError('Atendimento não encontrado no módulo Saúde')
        amount = await self.saude_service.get_valor_servico(atendimento_id)
        if amount <= 0:
            raise DomainValidationError('Valor de serviço de saúde inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='SAU_TAXA', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc) + timedelta(days=30), revenue_code=revenue_code, cost_center=cost_center, request_id=str(atendimento_id))

    @trace()
    async def create_assistencia_benefit_invoice(self, *, beneficio_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Benefício Assistência Social') -> Invoice:
        if self.assistencia_social_service is None:
            raise DomainValidationError('Integração com Assistência Social não configurada')
        beneficio = await self.assistencia_social_service.get_beneficio(beneficio_id)
        if beneficio is None:
            raise DomainValidationError('Benefício não encontrado no módulo Assistência Social')
        amount = await self.assistencia_social_service.get_valor_beneficio(beneficio_id)
        if amount <= 0:
            raise DomainValidationError('Valor de benefício inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='ASS_BENEFICIO', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc), revenue_code=revenue_code, cost_center=cost_center, request_id=str(beneficio_id))

    @trace()
    async def create_service_request_fee_invoice(self, *, request_id: UUID, citizen_id: str, revenue_code: str, cost_center: str, due_date: datetime | None=None, service_name: str='Taxa de Pedido de Serviço') -> Invoice:
        if self.service_requests_service is None:
            raise DomainValidationError('Integração com Service Requests não configurada')
        request = await self.service_requests_service.get_request(request_id)
        if request is None:
            raise DomainValidationError('Pedido não encontrado no módulo Service Requests')
        amount = await self.service_requests_service.get_valor_taxa(request_id)
        if amount <= 0:
            raise DomainValidationError('Valor de taxa de serviço inválido para faturação')
        return await self._create_module_invoice(citizen_id=citizen_id, service_code='SRV_TAXA', service_name=service_name, amount=amount, due_date=due_date or datetime.now(timezone.utc) + timedelta(days=15), revenue_code=revenue_code, cost_center=cost_center, request_id=str(request_id))

    @trace()
    async def get_invoice(self, invoice_id: str) -> Invoice:
        """Recupera fatura por ID com validação."""
        invoice = await self.repository.get_by_id(invoice_id)
        if not invoice:
            logger.warning(f'Fatura não encontrada: {invoice_id}')
            raise InvoiceNotFoundError(invoice_id)
        return invoice

    @trace()
    async def list_citizen_invoices(self, citizen_id: str) -> List[Invoice]:
        """Lista histórico de faturas de um cidadão."""
        logger.info(f'Recuperando faturas do cidadão: {citizen_id}')
        return await self.repository.get_by_citizen(citizen_id)

    @trace()
    async def cancel_invoice(self, invoice_id: str, reason: str='Cancelamento administrativo') -> Invoice:
        """
        Cancela fatura com validação de estado.

        REGRA: Apenas PENDING ou OVERDUE podem ser canceladas.
        PAID e CANCELLED são estados finais.
        """
        invoice = await self.get_invoice(invoice_id)
        invoice.change_status(InvoiceStatus.CANCELLED, reason=reason)
        updated_invoice = await self.repository.save(invoice)
        logger.info(f'Fatura {invoice_id} cancelada: {reason}')
        return updated_invoice

    @trace()
    async def mark_overdue(self, invoice_id: str) -> Invoice:
        """
        Marca fatura como OVERDUE se data limite ultrapassada.

        REGRA: Apenas PENDING → OVERDUE é válido.
        """
        invoice = await self.get_invoice(invoice_id)
        if invoice.is_overdue() and invoice.status == InvoiceStatus.PENDING:
            invoice.change_status(InvoiceStatus.OVERDUE, reason='Data limite de pagamento ultrapassada')
            updated_invoice = await self.repository.save(invoice)
            logger.info(f'Fatura {invoice_id} marcada como OVERDUE')
            return updated_invoice
        return invoice

    @trace()
    async def get_pending_by_citizen(self, citizen_id: str) -> List[Invoice]:
        """Recupera faturas pendentes de um cidadão."""
        invoices = await self.repository.get_pending(citizen_id)
        logger.info(f'Encontradas {len(invoices)} faturas pendentes para: {citizen_id}')
        return invoices

    async def _create_module_invoice(self, *, citizen_id: str, service_code: str, service_name: str, amount: float, due_date: datetime, revenue_code: str, cost_center: str, request_id: str, currency: str='AOA') -> Invoice:
        data = CreateInvoiceSchema(citizen_id=citizen_id, service_code=service_code, service_name=service_name, request_id=request_id, revenue_code=revenue_code, cost_center=cost_center, amount=amount, currency=currency, due_date=due_date)
        return await self.create_invoice(data)

    async def _validate_citizen_identity(self, citizen_id: str) -> None:
        if self.identidade_service is None:
            return
        try:
            citizen_uuid = UUID(citizen_id)
        except (TypeError, ValueError):
            return
        is_active = await self.identidade_service.validar_cidadao_ativo(citizen_uuid)
        if not is_active:
            raise DomainValidationError(f'Cidadão {citizen_id} não está ativo em Identidade Civil')
