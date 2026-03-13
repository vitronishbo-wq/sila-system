"""
SLA/SLO Definitions - Thresholds Operacionais Oficiais do SILA.
Declarativo. Sem lógica de negócio. Apenas definições.
"""
SLA_DEFINITIONS = {'BI_EMISSAO': {'description': 'Emissão de Bilhete de Identidade', 'target_sla_seconds': 172800, 'warning_threshold_seconds': 86400, 'critical_threshold_seconds': 259200}, 'CERTIDAO_NASCIMENTO': {'description': 'Certidão de Nascimento', 'target_sla_seconds': 86400, 'warning_threshold_seconds': 43200, 'critical_threshold_seconds': 172800}, 'CERTIDAO_CASAMENTO': {'description': 'Certidão de Casamento', 'target_sla_seconds': 86400, 'warning_threshold_seconds': 43200, 'critical_threshold_seconds': 172800}, 'CERTIDAO_OBITO': {'description': 'Certidão de Óbito', 'target_sla_seconds': 43200, 'warning_threshold_seconds': 21600, 'critical_threshold_seconds': 86400}, 'DEFAULT': {'description': 'Serviço Genérico', 'target_sla_seconds': 259200, 'warning_threshold_seconds': 172800, 'critical_threshold_seconds': 432000}}
ANOMALY_THRESHOLDS = {'FILE_DELETED': {'window_minutes': 60, 'max_count': 20, 'severity': 'HIGH'}, 'REQUEST_STATUS_UPDATED': {'window_minutes': 5, 'max_count': 100, 'severity': 'MEDIUM'}, 'FILE_UPLOADED': {'window_minutes': 10, 'max_count': 200, 'severity': 'INFO'}}
SLO_TARGETS = {'availability': 99.5, 'request_completion_rate': 95.0, 'error_rate_max': 1.0}

def get_sla_for_service(service_code: str) -> dict:
    """Retorna SLA para um service_code, com fallback para DEFAULT."""
    return SLA_DEFINITIONS.get(service_code, SLA_DEFINITIONS['DEFAULT'])

def evaluate_sla_status(elapsed_seconds: float, service_code: str) -> str:
    """
    Avalia o status de um pedido com base no tempo decorrido.
    Retorna: 'OK', 'WARNING', 'CRITICAL', 'BREACHED'
    """
    sla = get_sla_for_service(service_code)
    if elapsed_seconds <= sla['warning_threshold_seconds']:
        return 'OK'
    elif elapsed_seconds <= sla['target_sla_seconds']:
        return 'WARNING'
    elif elapsed_seconds <= sla['critical_threshold_seconds']:
        return 'CRITICAL'
    else:
        return 'BREACHED'