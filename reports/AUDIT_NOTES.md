Eligibility Engine & Orchestration - Audit Notes
===============================================

Scope:
- The audit covers automated decisions and transfer executions produced by the new Eligibility Engine and Automation pipeline.

Where to find logs:
- Transfer requests and evaluations: `audit_events` database table
- Orchestrator DLQ entries: `reports/orchestrator_dlq.log` (JSON lines)

What is recorded:
- `transfer_requested`: includes the incoming request payload and the evaluation result.
- `transfer_executed` / `transfer_completed`: includes request identifiers and execution result.
- `transfer_failed`: includes error information for failed executions.

Audit recommendations:
- Ensure `audit_events` and `reports/orchestrator_dlq.log` are stored on a secure, append-only medium and ingested into centralized SIEM.
- Add immutable event IDs and include actor/context metadata (e.g., requestor IP, authenticated user id) to each audit record.
- Configure retention policy and data redaction rules (PII masking) for stored payloads.
- Implement cryptographic signing or secure transmission to an external audit-store for compliance-critical actions.

Compliance notes:
- Automated transfers should store a decision trace (which rules fired, rule inputs) to allow human review and appeals.
- Any automatic financial actions (propinas, bolsas) require stricter audit trails and payment reconciliations.

Suggested next audit tasks:
1. Run daily audit job to summarize transfer counts, automated vs manual, failure rates.
2. Add monitoring alerts for DLQ growth (indicates systemic failures).
3. Periodically sample a set of automated decisions for manual verification and quality metrics.
