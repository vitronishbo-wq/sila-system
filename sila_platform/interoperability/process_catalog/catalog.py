from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProcessStatus(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    PILOT = "pilot"


@dataclass
class ProcessDefinition:
    """Definição de um processo governamental transversal.

    Exemplo — Constituir Empresa:
        process_id: "constituir_empresa"
        name: "Constituição de Empresa"
        modules: ["justica", "financas-impostos", "apoio-empresarial",
                   "administracao-local", "seguranca-social", "payment"]
        events: ["company_registered", "nif_issued", "payment_confirmed", ...]
        owner_ministry: "MINECON"
    """
    process_id: str
    name: str
    description: str = ""
    modules: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)
    owner_ministry: str = ""
    owner_ministry_code: str = ""
    status: ProcessStatus = ProcessStatus.ACTIVE
    version: str = "1.0.0"
    legislation: str = ""
    estimated_duration_days: int = 0
    requires_citizen_identity: bool = True
    requires_payment: bool = False
    child_processes: list[str] = field(default_factory=list)
    parent_process: Optional[str] = None


NATIONAL_PROCESSES: dict[str, ProcessDefinition] = {
    "constituir_empresa": ProcessDefinition(
        process_id="constituir_empresa",
        name="Constituição de Empresa",
        description="Registo legal de empresa com NIF, licenciamento e registo de empregador",
        modules=["justica", "financas-impostos", "apoio-empresarial",
                 "administracao-local", "seguranca-social", "payment"],
        events=["company_registered", "nif_issued", "payment_confirmed",
                "commercial_license_issued", "employer_registered"],
        owner_ministry="Ministério da Economia",
        owner_ministry_code="MINECON",
        requires_payment=True,
        estimated_duration_days=5,
        legislation="Lei das Sociedades Comerciais",
    ),
    "nascimento_cidadao": ProcessDefinition(
        process_id="nascimento_cidadao",
        name="Nascimento de Cidadão",
        description="Registo de nascimento, emissão de BI, registo de utente de saúde e reserva de vaga escolar",
        modules=["registo-civil", "identity", "saude", "educacao",
                 "administracao-local"],
        events=["birth_registered", "citizen_created", "bi_issued",
                "patient_registered", "student_enrolled"],
        owner_ministry="Ministério da Justiça e dos Direitos Humanos",
        owner_ministry_code="MINJUSDH",
        estimated_duration_days=30,
        legislation="Lei do Registo Civil",
    ),
    "matricula_escolar": ProcessDefinition(
        process_id="matricula_escolar",
        name="Matrícula Escolar",
        description="Inscrição de aluno no sistema nacional de ensino",
        modules=["educacao", "identity", "administracao-local"],
        events=["student_enrolled", "citizen_updated", "residence_confirmed"],
        owner_ministry="Ministério da Educação",
        owner_ministry_code="MINED",
        estimated_duration_days=3,
    ),
    "transferencia_escolar": ProcessDefinition(
        process_id="transferencia_escolar",
        name="Transferência Escolar",
        description="Mudança de escola entre instituições de ensino",
        modules=["educacao", "administracao-local"],
        events=["student_transferred", "residence_confirmed"],
        owner_ministry="Ministério da Educação",
        owner_ministry_code="MINED",
        estimated_duration_days=5,
    ),
    "emissao_bi": ProcessDefinition(
        process_id="emissao_bi",
        name="Emissão de Bilhete de Identidade",
        description="Emissão de BI para cidadão nacional",
        modules=["identity", "registo-civil", "payment"],
        events=["bi_issued", "citizen_updated", "birth_registered", "payment_confirmed"],
        owner_ministry="Ministério do Interior",
        owner_ministry_code="MININT",
        requires_payment=True,
        estimated_duration_days=10,
        legislation="Lei de Identificação Civil",
    ),
    "emissao_nif": ProcessDefinition(
        process_id="emissao_nif",
        name="Emissão de NIF",
        description="Atribuição de Número de Identificação Fiscal",
        modules=["financas-impostos", "identity", "payment"],
        events=["nif_issued", "citizen_updated", "payment_confirmed"],
        owner_ministry="Ministério das Finanças",
        owner_ministry_code="MINFIN",
        requires_payment=False,
        estimated_duration_days=1,
        legislation="Código Geral Tributário",
    ),
    "contratacao_laboral": ProcessDefinition(
        process_id="contratacao_laboral",
        name="Contratação Laboral",
        description="Registo de contrato de trabalho e inscrição na segurança social",
        modules=["emprego", "trabalho-inspecao", "seguranca-social",
                 "financas-impostos", "identity"],
        events=["employer_registered", "social_contribution_received",
                "citizen_updated", "nif_issued"],
        owner_ministry="Ministério da Administração Pública e Segurança Social",
        owner_ministry_code="MAPTSS",
        estimated_duration_days=2,
        legislation="Lei Geral do Trabalho",
    ),
    "aposentacao": ProcessDefinition(
        process_id="aposentacao",
        name="Aposentação / Pensão",
        description="Requerimento e concessão de pensão de velhice ou invalidez",
        modules=["seguranca-social", "identity", "financas-impostos", "payment"],
        events=["benefit_granted", "citizen_updated", "payment_confirmed",
                "social_contribution_received"],
        owner_ministry="Ministério da Administração Pública e Segurança Social",
        owner_ministry_code="MAPTSS",
        requires_citizen_identity=True,
        estimated_duration_days=30,
        legislation="Lei de Bases da Segurança Social",
    ),
    "licenciamento_comercial": ProcessDefinition(
        process_id="licenciamento_comercial",
        name="Licenciamento Comercial",
        description="Obtenção de licença comercial e alvará para estabelecimento",
        modules=["comercio", "administracao-local", "apoio-empresarial",
                 "financas-impostos", "payment"],
        events=["license_permit_issued", "commercial_license_issued",
                "residence_confirmed", "payment_confirmed", "nif_issued"],
        owner_ministry="Ministério da Economia",
        owner_ministry_code="MINECON",
        requires_payment=True,
        estimated_duration_days=7,
    ),
    "pagamento_impostos": ProcessDefinition(
        process_id="pagamento_impostos",
        name="Pagamento de Impostos",
        description="Declaração e pagamento de tributos",
        modules=["financas-impostos", "payment", "identity"],
        events=["tax_declaration_submitted", "tax_payment_received", "payment_confirmed"],
        owner_ministry="Ministério das Finanças",
        owner_ministry_code="MINFIN",
        requires_payment=True,
        estimated_duration_days=1,
        legislation="Código Geral Tributário",
    ),
}


class ProcessCatalog:
    """Catálogo oficial de processos transversais do Estado."""

    def __init__(self) -> None:
        self._processes: dict[str, ProcessDefinition] = {}

    def register(self, proc: ProcessDefinition) -> ProcessDefinition:
        self._processes[proc.process_id] = proc
        return proc

    def get(self, process_id: str) -> Optional[ProcessDefinition]:
        return self._processes.get(process_id)

    def list_active(self) -> list[ProcessDefinition]:
        return [p for p in self._processes.values() if p.status == ProcessStatus.ACTIVE]

    def list_by_ministry(self, code: str) -> list[ProcessDefinition]:
        return [p for p in self._processes.values() if p.owner_ministry_code == code]

    def list_by_module(self, module: str) -> list[ProcessDefinition]:
        return [p for p in self._processes.values() if module in p.modules]

    def list_all(self) -> list[ProcessDefinition]:
        return list(self._processes.values())

    def count(self) -> int:
        return len(self._processes)

    def get_event_processes(self, event: str) -> list[ProcessDefinition]:
        return [p for p in self._processes.values() if event in p.events]


def get_catalog() -> ProcessCatalog:
    cat = ProcessCatalog()
    for p in NATIONAL_PROCESSES.values():
        cat.register(p)
    return cat


list_processes = lambda: list(NATIONAL_PROCESSES.keys())
get_process = lambda pid: NATIONAL_PROCESSES.get(pid)
