"""Workflows cross-sector que atravessam múltiplos módulos.

Exemplo: Constituição de Empresa
    Justiça (validar sócios) → Finanças (NIF) → Admin Local (licenciamento) → SegSocial (registo empregador) → Pagamento (taxas)
"""

from sila_platform.interoperability.workflow_orchestrator.engine import WorkflowOrchestrator
from sila_platform.interoperability.process_manager.engine import ProcessManager

orchestrator = WorkflowOrchestrator()
process_manager = ProcessManager()

CROSS_SECTOR_WORKFLOWS: dict[str, list[dict]] = {
    "constituir_empresa": [
        {"module": "justica", "service_id": "validar_socios", "input": {"tipo": "socios"}},
        {"module": "financas-impostos", "service_id": "emitir_nif", "input": {"tipo": "empresa"}},
        {"module": "administracao-local", "service_id": "licenciamento", "input": {"tipo": "comercial"}},
        {"module": "seguranca-social", "service_id": "registo_empregador", "input": {}},
        {"module": "payment", "service_id": "pagamento_taxas", "input": {"taxa": "constituicao"}},
    ],
    "nascimento_cidadao": [
        {"module": "registo-civil", "service_id": "registar_nascimento", "input": {}},
        {"module": "identity", "service_id": "emitir_bi", "input": {"tipo": "menor"}},
        {"module": "saude", "service_id": "registar_utente", "input": {}},
        {"module": "educacao", "service_id": "reservar_vaga", "input": {"nivel": "primario"}},
    ],
    "transferencia_escolar": [
        {"module": "educacao", "service_id": "validar_matricula_origem", "input": {}},
        {"module": "educacao", "service_id": "aceitar_matricula_destino", "input": {}},
        {"module": "administracao-local", "service_id": "confirmar_residencia", "input": {}},
    ],
}


def list_workflows() -> dict[str, list[str]]:
    return {name: [s["module"] for s in steps]
            for name, steps in CROSS_SECTOR_WORKFLOWS.items()}


def start_workflow(wf_name: str, citizen_id: str, metadata: dict | None = None) -> dict:
    steps = CROSS_SECTOR_WORKFLOWS.get(wf_name)
    if not steps:
        raise ValueError(f"Workflow desconhecido: {wf_name}")
    orch = orchestrator.create(wf_name, "portal", citizen_id, steps, metadata)
    return {"id": orch.id, "workflow": wf_name, "steps": len(orch.steps), "status": orch.status.value}
