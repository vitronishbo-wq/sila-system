from app.core.audit import AuditLog, audit_log, AuditAnalytics, SLA_DEFINITIONS, evaluate_sla_status

print("Imports OK")
print("SLA Defs:", len(SLA_DEFINITIONS))
print("BI eval:", evaluate_sla_status(100000, "BI_EMISSAO"))
print("Default eval:", evaluate_sla_status(500000, "DEFAULT"))
