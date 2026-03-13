from ..entities.audit_alert import AuditAlert
from ..value_objects.audit_severity import AuditSeverity

class ContractOverBudgetRule:

    def check(self, event):
        if event.get('type') != 'ContractAwarded':
            return None
        metadata = event.get('metadata', {})
        contract_value = float(metadata.get('value', 0))
        estimated_value = float(metadata.get('estimated', 0))
        if estimated_value <= 0:
            return None
        if contract_value > estimated_value * 1.2:
            return AuditAlert(rule_triggered='CONTRACT_OVERPRICE', entity_id=event['entity_id'], severity=AuditSeverity.HIGH, description='Contract exceeds estimated value by 20%')
        return None