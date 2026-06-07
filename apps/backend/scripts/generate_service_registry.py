#!/usr/bin/env python3
"""Generate service registry artifacts from source catalog.

Outputs:
  1) module.yaml (source of truth per module)
  2) service_catalog.json (DB payload)
  3) service_forms.json (form schemas)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - explicit error
    raise SystemExit("PyYAML required. Install with `pip install pyyaml`.") from exc


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
MODULES_ROOT = BACKEND_ROOT / "app" / "modules"
REGISTRY_OUTPUT = BACKEND_ROOT / "app" / "core" / "catalog" / "registry"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _read_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict) and "services" in payload:
        return payload["services"] or []
    if isinstance(payload, list):
        return payload
    return []


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def _safe_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value).strip()]


def _nova_matricula_schema() -> dict[str, Any]:
    return {
        "version": "1.0",
        "layout": "wizard",
        "groups": [
            {
                "key": "estudante",
                "label": "Dados do estudante",
                "fields": [
                    {
                        "key": "student_name",
                        "label": "Nome",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "key": "student_birth_date",
                        "label": "Data nascimento",
                        "type": "date",
                        "required": True,
                    },
                    {
                        "key": "student_gender",
                        "label": "Sexo",
                        "type": "select",
                        "required": True,
                        "options": ["feminino", "masculino"],
                    },
                    {
                        "key": "student_bi",
                        "label": "BI",
                        "type": "bi",
                        "required": True,
                        "mask": "bi",
                    },
                    {
                        "key": "student_nif",
                        "label": "NIF",
                        "type": "nif",
                        "required": False,
                        "mask": "nif",
                    },
                ],
            },
            {
                "key": "encarregado",
                "label": "Dados do encarregado",
                "fields": [
                    {
                        "key": "guardian_name",
                        "label": "Nome",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "key": "guardian_relationship",
                        "label": "Parentesco",
                        "type": "select",
                        "required": True,
                        "options": ["mae", "pai", "tutor", "outro"],
                    },
                    {
                        "key": "guardian_phone",
                        "label": "Telefone",
                        "type": "tel",
                        "required": True,
                    },
                    {
                        "key": "guardian_email",
                        "label": "Email",
                        "type": "email",
                        "required": False,
                    },
                    {
                        "key": "guardian_address",
                        "label": "Morada",
                        "type": "text",
                        "required": True,
                    },
                ],
            },
            {
                "key": "escola",
                "label": "Escolha da escola",
                "fields": [
                    {
                        "key": "school_search",
                        "label": "Pesquisar escola",
                        "type": "search",
                        "required": True,
                    },
                    {
                        "key": "school_vacancies",
                        "label": "Vagas",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "school_distance_km",
                        "label": "Distancia",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "school_shift",
                        "label": "Turno",
                        "type": "select",
                        "required": True,
                        "options": ["manha", "tarde", "noite"],
                    },
                    {
                        "key": "school_fee",
                        "label": "Propina",
                        "type": "readonly",
                        "required": False,
                    },
                ],
            },
            {
                "key": "documentos",
                "label": "Documentos",
                "fields": [
                    {
                        "key": "student_bi_file",
                        "label": "BI estudante",
                        "type": "upload",
                        "required": True,
                    },
                    {
                        "key": "guardian_bi_file",
                        "label": "BI encarregado",
                        "type": "upload",
                        "required": True,
                    },
                    {
                        "key": "student_photo",
                        "label": "Fotografia",
                        "type": "upload",
                        "required": True,
                    },
                    {
                        "key": "previous_certificate",
                        "label": "Certificado anterior",
                        "type": "upload",
                        "required": False,
                    },
                    {
                        "key": "previous_report",
                        "label": "Boletim anterior",
                        "type": "upload",
                        "required": False,
                    },
                ],
            },
            {
                "key": "validacao",
                "label": "Validacao",
                "fields": [
                    {
                        "key": "eligibility_status",
                        "label": "Elegivel",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "vacancy_status",
                        "label": "Ha vagas",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "conflict_status",
                        "label": "Conflitos",
                        "type": "readonly",
                        "required": False,
                    },
                ],
            },
            {
                "key": "pagamento",
                "label": "Pagamento",
                "fields": [
                    {
                        "key": "payment_method",
                        "label": "Metodo",
                        "type": "radio",
                        "required": True,
                        "options": ["referencia", "multicaixa", "wallet"],
                    },
                    {
                        "key": "payment_reference",
                        "label": "Referencia",
                        "type": "readonly",
                        "required": False,
                    },
                ],
            },
            {
                "key": "confirmacao",
                "label": "Confirmacao",
                "fields": [
                    {
                        "key": "enrollment_number",
                        "label": "Numero matricula",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "receipt",
                        "label": "Comprovativo",
                        "type": "readonly",
                        "required": False,
                    },
                    {
                        "key": "qr_code",
                        "label": "QR",
                        "type": "readonly",
                        "required": False,
                    },
                ],
            },
        ],
        "validations": [
            {
                "field": "student_bi",
                "type": "regex",
                "pattern": "^[0-9A-Z]{14}$",
                "message": "Numero BI invalido.",
            },
            {
                "field": "student_nif",
                "type": "regex",
                "pattern": "^\\d{10}$",
                "message": "NIF invalido.",
            },
            {
                "field": "student_bi_file",
                "type": "required",
                "message": "Anexe o BI do estudante.",
            },
            {
                "field": "guardian_bi_file",
                "type": "required",
                "message": "Anexe o BI do encarregado.",
            },
        ],
        "dependencies": [
            {
                "field": "student_bi",
                "value": "*",
                "requires": ["student_name", "student_birth_date"],
                "message": (
                    "Enquanto nao houver interoperabilidade certificada, informe BI, nome "
                    "e nascimento."
                ),
            }
        ],
    }


def _service_schema(service: dict[str, Any]) -> dict[str, Any]:
    code = service["id"].lower()
    name = service["name"].lower()
    if code == "educacao_001" or name == "nova matricula escolar":
        return _nova_matricula_schema()

    base_fields = [
        {
            "key": "citizen_name",
            "label": "Nome completo",
            "type": "text",
            "required": True,
            "placeholder": "Nome conforme documento",
        },
        {
            "key": "citizen_document",
            "label": "Documento de identificacao",
            "type": "text",
            "required": True,
            "placeholder": "BI ou Passaporte",
        },
    ]
    request_fields: list[dict[str, Any]] = []

    if "bi" in code or "identidade" in name:
        base_fields.append(
            {
                "key": "bi_number",
                "label": "Numero BI",
                "type": "bi",
                "required": True,
                "mask": "bi",
                "helper": "Formato: 000000000AA000",
            }
        )

    if "nif" in code or "tax" in code or "imposto" in name:
        base_fields.append(
            {
                "key": "nif",
                "label": "Numero de NIF",
                "type": "nif",
                "required": False,
                "mask": "nif",
                "helper": "10 digitos",
            }
        )

    if "certidao" in code or "registo" in name or "registro" in name:
        request_fields.append(
            {
                "key": "certificate_type",
                "label": "Tipo de certidao",
                "type": "select",
                "required": True,
                "options": ["nascimento", "casamento", "obito", "outra"],
            }
        )

    if any(token in code for token in ("agua", "water", "energia", "energy")) or "ligacao" in name:
        request_fields.append(
            {
                "key": "address",
                "label": "Morada",
                "type": "text",
                "required": True,
                "placeholder": "Rua, bairro, municipio",
            }
        )

    request_fields.extend(
        [
            {
                "key": "delivery_mode",
                "label": "Entrega",
                "type": "radio",
                "required": True,
                "options": ["digital", "presencial", "expresso"],
            },
            {
                "key": "supporting_files",
                "label": "Anexos",
                "type": "upload",
                "required": False,
                "multiple": True,
                "min_files": 0,
            },
            {
                "key": "terms_accept",
                "label": "Confirmo que os dados sao verdadeiros",
                "type": "checkbox",
                "required": True,
            },
            {
                "key": "notes",
                "label": "Observacoes",
                "type": "textarea",
                "required": False,
                "placeholder": f"Detalhes adicionais para {service['name']}",
            },
        ]
    )

    return {
        "version": "1.0",
        "groups": [
            {"key": "identificacao", "label": "Identificacao", "fields": base_fields},
            {"key": "pedido", "label": "Detalhes do pedido", "fields": request_fields},
        ],
        "validations": [
            {
                "field": "terms_accept",
                "type": "required_true",
                "message": "Confirme os termos para continuar.",
            },
            {
                "field": "bi_number",
                "type": "regex",
                "pattern": "^[0-9A-Z]{14}$",
                "message": "Numero BI invalido.",
            },
            {"field": "nif", "type": "regex", "pattern": "^\\d{10}$", "message": "NIF invalido."},
        ],
        "dependencies": [
            {
                "field": "delivery_mode",
                "value": "expresso",
                "requires": ["supporting_files"],
                "message": "Entrega expresso requer anexos comprobatórios.",
            }
        ],
    }


def _build_service_item(
    module: dict[str, Any],
    raw: dict[str, Any],
    currency: str = "AOA",
) -> dict[str, Any]:
    service_id = (raw.get("id") or raw.get("code") or raw.get("service_code") or "").strip()
    if not service_id:
        service_id = f"{module['code'].upper()}_{len(module['services']) + 1:03d}"
    name = (raw.get("name") or raw.get("service_name") or service_id).strip()
    description = (raw.get("description") or raw.get("details") or name).strip()
    category = (raw.get("category") or raw.get("module") or module["code"]).strip()
    tags = _safe_list(raw.get("tags") or module.get("default_tags"))

    sla_days = int(raw.get("sla_days") or raw.get("sla") or 5)
    sla_type = raw.get("sla_type") or "business_days"
    price = float(raw.get("price") or raw.get("amount") or 0)

    workflow_steps = _safe_list(raw.get("workflow_steps")) or [
        "request",
        "validation",
        "approval",
        "issuance",
    ]
    workflow_type = raw.get("workflow_type") or "standard"

    requires_auth = bool(raw.get("requires_auth", True))
    requires_biometrics = bool(raw.get("requires_biometrics", False))

    schema_id = raw.get("form_schema") or f"{service_id.lower()}_v1"

    service = {
        "id": service_id,
        "name": name,
        "description": description,
        "category": category,
        "tags": tags,
        "sla": {"days": sla_days, "type": sla_type},
        "pricing": {"amount": price, "currency": currency},
        "requirements": {
            "requires_auth": requires_auth,
            "requires_biometrics": requires_biometrics,
        },
        "workflow": {"type": workflow_type, "steps": workflow_steps},
        "form": {"schema": schema_id},
        "status": raw.get("status") or "active",
        "version": raw.get("version") or "v1",
        # Compatibility fields for portal renderer
        "price": price,
    }

    return service


def _estimate_priority(service: dict[str, Any]) -> tuple[str, str]:
    service["pricing"]["amount"]
    sla_days = service["sla"]["days"]
    if sla_days <= 2:
        return ("high", "platinum")
    if sla_days <= 5:
        return ("medium", "gold")
    return ("low", "silver")


def _to_catalog_entry(
    module: dict[str, Any], service: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Any]:
    priority, tier = _estimate_priority(service)
    return {
        "code": service["id"],
        "name": service["name"],
        "category": module["code"],
        "description": service["description"],
        "price": service["pricing"]["amount"],
        "base_hours": service["sla"]["days"] * 24,
        "priority": priority,
        "tier": tier,
        "version": service["version"].replace("v", ""),
        "legal_basis": module.get("legal_basis"),
        "form_fields": schema,
    }


def _load_blueprint(target_services: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    from apps.backend.app.core.catalog.blueprint import MODULE_BLUEPRINTS, build_service_blueprints

    modules = []
    for module in MODULE_BLUEPRINTS:
        modules.append(
            {
                "code": module.slug,
                "name": module.title,
                "description": module.description,
                "ui": {"icon": module.slug, "color": "#2563eb", "order": None},
                "default_tags": list(module.focus_terms),
            }
        )

    services = []
    for service in build_service_blueprints(target_count=target_services):
        if service.module_slug == "identity":
            continue
        services.append(
            {
                "id": service.code,
                "name": service.name,
                "description": service.description,
                "module": service.module_slug,
                "price": float(service.fee),
                "sla_days": int(service.sla_days),
                "workflow_type": "standard",
                "workflow_steps": ["request", "validation", "approval", "issuance"],
                "requires_auth": True,
                "requires_biometrics": False,
                "tags": [service.module_slug],
            }
        )

    services.extend(_identity_service_templates())

    return modules, services


def _identity_service_templates() -> list[dict[str, Any]]:
    return [
        {
            "id": "BI_EMISSAO",
            "name": "Emissao de Bilhete de Identidade",
            "description": "Solicitar primeira emissao do BI.",
            "module": "identity",
            "price": 1000,
            "sla_days": 7,
            "requires_biometrics": True,
            "tags": ["bi", "identidade", "documento"],
        },
        {
            "id": "BI_RENOVACAO",
            "name": "Renovacao de Bilhete de Identidade",
            "description": "Renovacao do BI expirado.",
            "module": "identity",
            "price": 800,
            "sla_days": 5,
            "requires_biometrics": True,
            "tags": ["bi", "identidade"],
        },
        {
            "id": "BI_SEGUNDA_VIA",
            "name": "Segunda Via do BI",
            "description": "Em caso de perda ou roubo.",
            "module": "identity",
            "price": 1500,
            "sla_days": 3,
            "requires_biometrics": True,
            "tags": ["bi", "identidade"],
        },
        {
            "id": "BI_ALTERACAO_DADOS",
            "name": "Alteracao de Dados do BI",
            "description": "Atualizacao de dados pessoais no BI.",
            "module": "identity",
            "price": 700,
            "sla_days": 4,
            "requires_biometrics": True,
            "tags": ["bi", "dados"],
        },
        {
            "id": "BI_REVALIDACAO",
            "name": "Revalidacao do BI",
            "description": "Revalidar documento proximo do vencimento.",
            "module": "identity",
            "price": 600,
            "sla_days": 5,
            "requires_biometrics": True,
            "tags": ["bi", "documento"],
        },
        {
            "id": "BI_CANCELAMENTO",
            "name": "Cancelamento do BI",
            "description": "Cancelamento por falecimento ou ordem judicial.",
            "module": "identity",
            "price": 0,
            "sla_days": 2,
            "requires_biometrics": False,
            "tags": ["bi"],
        },
        {
            "id": "BI_AGENDAMENTO",
            "name": "Agendamento para BI",
            "description": "Agendar atendimento presencial para BI.",
            "module": "identity",
            "price": 0,
            "sla_days": 1,
            "requires_biometrics": False,
            "tags": ["bi", "agendamento"],
        },
        {
            "id": "BI_CONSULTA_ESTADO",
            "name": "Consulta do Estado do BI",
            "description": "Acompanhar o estado do processo do BI.",
            "module": "identity",
            "price": 0,
            "sla_days": 1,
            "requires_biometrics": False,
            "tags": ["bi", "consulta"],
        },
        {
            "id": "NIF_ATRIBUICAO",
            "name": "Atribuicao de NIF",
            "description": "Emissao de Numero de Identificacao Fiscal.",
            "module": "identity",
            "price": 0,
            "sla_days": 2,
            "requires_biometrics": False,
            "tags": ["nif", "fiscal"],
        },
        {
            "id": "NIF_ATUALIZACAO",
            "name": "Atualizacao de NIF",
            "description": "Atualizar dados fiscais associados ao NIF.",
            "module": "identity",
            "price": 0,
            "sla_days": 3,
            "requires_biometrics": False,
            "tags": ["nif", "fiscal"],
        },
        {
            "id": "NIF_SEGUNDA_VIA",
            "name": "Segunda Via do NIF",
            "description": "Recuperar ou emitir segunda via do NIF.",
            "module": "identity",
            "price": 0,
            "sla_days": 3,
            "requires_biometrics": False,
            "tags": ["nif", "fiscal"],
        },
        {
            "id": "NIF_REGULARIZACAO",
            "name": "Regularizacao de NIF",
            "description": "Regularizar situacao fiscal basica.",
            "module": "identity",
            "price": 0,
            "sla_days": 5,
            "requires_biometrics": False,
            "tags": ["nif", "fiscal"],
        },
        {
            "id": "COMPROVATIVO_RESIDENCIA",
            "name": "Comprovativo de Residencia",
            "description": "Emissao de comprovativo oficial de residencia.",
            "module": "identity",
            "price": 500,
            "sla_days": 1,
            "requires_biometrics": False,
            "tags": ["residencia"],
        },
        {
            "id": "DECLARACAO_RESIDENCIA",
            "name": "Declaracao de Residencia",
            "description": "Declaracao simplificada de residencia.",
            "module": "identity",
            "price": 300,
            "sla_days": 1,
            "requires_biometrics": False,
            "tags": ["residencia"],
        },
        {
            "id": "ATUALIZACAO_MORADA",
            "name": "Atualizacao de Morada",
            "description": "Atualizar endereco no cadastro nacional.",
            "module": "identity",
            "price": 300,
            "sla_days": 2,
            "requires_biometrics": False,
            "tags": ["morada", "cadastro"],
        },
        {
            "id": "ATUALIZACAO_CONTACTOS",
            "name": "Atualizacao de Contactos",
            "description": "Atualizar email e telefone no cadastro.",
            "module": "identity",
            "price": 0,
            "sla_days": 1,
            "requires_biometrics": False,
            "tags": ["contacto", "cadastro"],
        },
        {
            "id": "REGISTO_BIOMETRICO",
            "name": "Registo Biometrico",
            "description": "Coleta ou atualizacao de dados biometricos.",
            "module": "identity",
            "price": 0,
            "sla_days": 2,
            "requires_biometrics": True,
            "tags": ["biometria", "identidade"],
        },
    ]


def _normalize_service(service: dict[str, Any], module_code: str) -> dict[str, Any]:
    service_id = service.get("id") or service.get("code")
    if not service_id:
        service_id = f"{module_code.upper()}_{len(service):03d}"
    service["id"] = service_id
    service.setdefault("name", service_id)
    service.setdefault("description", service["name"])
    service["category"] = service.get("category") or module_code
    service["tags"] = _safe_list(service.get("tags"))

    if "pricing" not in service:
        amount = service.get("price") or 0
        service["pricing"] = {"amount": float(amount), "currency": "AOA"}
    else:
        service["pricing"].setdefault("currency", "AOA")
        service["pricing"]["amount"] = float(service["pricing"].get("amount", 0))

    if "sla" not in service:
        days = service.get("sla_days") or service.get("estimated_days") or 5
        service["sla"] = {"days": int(days), "type": "business_days"}
    else:
        service["sla"]["days"] = int(service["sla"].get("days", 5))
        service["sla"].setdefault("type", "business_days")

    service.setdefault("requirements", {"requires_auth": True, "requires_biometrics": False})
    service.setdefault(
        "workflow", {"type": "standard", "steps": ["request", "validation", "approval", "issuance"]}
    )
    service.setdefault("form", {"schema": f"{service_id.lower()}_v1"})
    service.setdefault("status", "active")
    service.setdefault("version", "v1")
    service["price"] = service["pricing"]["amount"]
    return service


def _load_existing_modules(modules_root: Path) -> dict[str, dict[str, Any]]:
    existing: dict[str, dict[str, Any]] = {}
    for module_path in sorted(modules_root.glob("*/module.yaml")):
        with module_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        code = data.get("code") or data.get("module") or module_path.parent.name
        data.setdefault("code", code)
        data.setdefault("module", code)
        data.setdefault("name", data.get("title") or code.title())
        data.setdefault("description", None)
        data.setdefault("ui", {"icon": "fa-layer-group", "color": "#2563eb", "order": None})
        data.setdefault("services", [])
        existing[code] = data
    return existing


def _index_modules(modules: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for module in modules:
        code = module["code"]
        indexed[code] = {**module, "services": []}
    return indexed


def generate(
    source: Path | None,
    target_services: int,
    modules_root: Path,
    output_dir: Path,
    dry_run: bool,
    include_services: bool,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    if source:
        ext = source.suffix.lower()
        raw_items = _read_json(source) if ext in (".json", ".jsn") else _read_csv(source)
        modules_payload: list[dict[str, Any]] = []
        services_payload: list[dict[str, Any]] = []
        for item in raw_items:
            module_code = (item.get("module") or item.get("category") or "general").strip()
            if module_code not in {m["code"] for m in modules_payload}:
                modules_payload.append(
                    {
                        "code": module_code,
                        "name": item.get("module_name") or module_code.title(),
                        "description": item.get("module_description"),
                        "ui": {
                            "icon": item.get("module_icon") or "fa-layer-group",
                            "color": item.get("module_color") or "#2563eb",
                            "order": item.get("module_order"),
                        },
                        "default_tags": _safe_list(item.get("module_tags")),
                    }
                )
            services_payload.append(item)
    else:
        modules_payload, services_payload = _load_blueprint(target_services)

    modules_index = _index_modules(modules_payload)
    existing_modules = _load_existing_modules(modules_root)
    for code, data in existing_modules.items():
        if code not in modules_index:
            modules_index[code] = {**data, "services": data.get("services", [])}
    registry_services = []
    catalog_entries = []
    form_entries = []

    for raw in services_payload:
        module_code = (raw.get("module") or raw.get("category") or "general").strip()
        if module_code not in modules_index:
            modules_index[module_code] = {
                "code": module_code,
                "name": module_code.title(),
                "description": None,
                "ui": {"icon": "fa-layer-group", "color": "#2563eb", "order": None},
                "default_tags": [],
                "services": [],
            }
        module = modules_index[module_code]
        service = _build_service_item(module, raw)
        schema = _service_schema(service)
        module["services"].append(service)
        registry_services.append(service)
        catalog_entries.append(_to_catalog_entry(module, service, schema))
        form_entries.append({"service_code": service["id"], "version": "1", "schema": schema})

    # Normalize existing services and metadata
    for module_code, module in modules_index.items():
        normalized_services = []
        seen = set()
        for service in module.get("services", []):
            normalized = _normalize_service(service, module_code)
            code = normalized["id"].upper()
            if code in seen:
                continue
            seen.add(code)
            normalized_services.append(normalized)
        module["services"] = normalized_services

    now = datetime.now(UTC).date().isoformat()
    modules_written = 0
    if not dry_run:
        for module in modules_index.values():
            module_path = modules_root / module["code"] / "module.yaml"
            existing = {}
            if module_path.exists():
                with module_path.open("r", encoding="utf-8") as handle:
                    existing = yaml.safe_load(handle) or {}
            merged = dict(existing)
            merged.update(
                {
                    "code": module["code"],
                    "module": module["code"],
                    "name": module["name"],
                    "description": module.get("description"),
                    "version": merged.get("version") or "1.0",
                    "last_updated": now,
                    "ui": {**(merged.get("ui") or {}), **module.get("ui", {})},
                    "services": module["services"] if include_services else [],
                }
            )
            module_path.parent.mkdir(parents=True, exist_ok=True)
            with module_path.open("w", encoding="utf-8") as handle:
                yaml.safe_dump(merged, handle, sort_keys=False, allow_unicode=True)
            modules_written += 1

        with (output_dir / "service_catalog.json").open("w", encoding="utf-8") as handle:
            json.dump({"services": catalog_entries}, handle, ensure_ascii=False, indent=2)

        with (output_dir / "service_forms.json").open("w", encoding="utf-8") as handle:
            json.dump({"forms": form_entries}, handle, ensure_ascii=False, indent=2)

    return {
        "modules": len(modules_index),
        "services": len(registry_services),
        "module_yaml_written": modules_written,
        "output_dir": str(output_dir),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate service registry artifacts")
    parser.add_argument("--source", help="Optional CSV/JSON source catalog")
    parser.add_argument(
        "--target-services", type=int, default=900, help="Services to generate (blueprint only)"
    )
    parser.add_argument(
        "--modules-root", default=str(MODULES_ROOT), help="Modules root to write module.yaml"
    )
    parser.add_argument(
        "--output-dir", default=str(REGISTRY_OUTPUT), help="Output directory for JSON payloads"
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    parser.add_argument(
        "--include-services", action="store_true", help="Write services into module.yaml"
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    source = Path(args.source).resolve() if args.source else None
    result = generate(
        source=source,
        target_services=args.target_services,
        modules_root=Path(args.modules_root),
        output_dir=Path(args.output_dir),
        dry_run=args.dry_run,
        include_services=args.include_services,
    )
    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(
        f"[{mode}] modules={result['modules']} services={result['services']} "
        f"module_yaml_written={result['module_yaml_written']} output_dir={result['output_dir']}"
    )


if __name__ == "__main__":
    main()
