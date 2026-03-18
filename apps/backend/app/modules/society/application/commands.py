"""
Society Module Command Handlers
Shows the pattern for welfare/society operations with event publishing.
"""
import logging
from uuid import UUID
from datetime import date, datetime, timezone
from typing import Optional
from decimal import Decimal
from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.society.domain.events import WelfareApplicationSubmitted, WelfareEligibilityApproved, WelfarePaymentProcessed
logger = logging.getLogger(__name__)

class SubmitWelfareApplicationCommandHandler:
    """Submit welfare application."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, application_id: UUID, applicant_id: UUID, benefit_type: str, household_size: int=1, correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Submitting welfare application for {benefit_type}')
        try:
            event = WelfareApplicationSubmitted(aggregate_id=application_id, aggregate_type='WelfareApplication', event_type='WelfareApplicationSubmitted', application_id=application_id, applicant_id=applicant_id, benefit_type=benefit_type, household_size=household_size, submission_date=date.today(), correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'SubmitWelfareApplication', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Welfare application submitted: {application_id}')
        except Exception as e:
            logger.error(f'Error submitting welfare application: {e}')
            raise

class ApproveWelfareEligibilityCommandHandler:
    """Approve welfare eligibility (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, approval_id: UUID, application_id: UUID, approved: bool, monthly_benefit_amount: Decimal=Decimal('0'), approval_authority: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Approving welfare eligibility {approval_id}')
        try:
            event = WelfareEligibilityApproved(aggregate_id=approval_id, aggregate_type='WelfareEligibility', event_type='WelfareEligibilityApproved', approval_id=approval_id, application_id=application_id, approved=approved, approval_date=date.today(), monthly_benefit_amount=monthly_benefit_amount, approval_authority=approval_authority, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'ApproveWelfareEligibility', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Welfare eligibility approved: {approval_id}')
        except Exception as e:
            logger.error(f'Error approving welfare eligibility: {e}')
            raise

class ProcessWelfarePaymentCommandHandler:
    """Process welfare payment (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, payment_id: UUID, beneficiary_id: UUID, amount: Decimal, period: str='', payment_method: str='bank_transfer', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Processing welfare payment {payment_id}')
        try:
            event = WelfarePaymentProcessed(aggregate_id=payment_id, aggregate_type='WelfarePayment', event_type='WelfarePaymentProcessed', payment_id=payment_id, beneficiary_id=beneficiary_id, amount=amount, payment_date=date.today(), period=period, payment_method=payment_method, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'ProcessWelfarePayment', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Welfare payment processed: {payment_id}')
        except Exception as e:
            logger.error(f'Error processing welfare payment: {e}')
            raise