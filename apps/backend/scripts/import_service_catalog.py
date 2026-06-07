#!/usr/bin/env python3
"""
Import official service catalog into service_catalog, service_forms, and sla_base.

Usage:
  python scripts/import_service_catalog.py --file /path/catalog.json
  python scripts/import_service_catalog.py --file /path/catalog.csv --no-sla-base

Expected JSON formats:
  - {"services": [{...}, ...]}
  - [{...}, ...]

Each service item supports:
  code/service_code, name, category/module, description, price,
  base_hours, priority, tier, version, legal_basis, form_fields

form_fields example:
  [
    {"key": "citizen_name", "label": "Nome completo", "type": "text", "required": true},
    {"key": "certificate_type", "label": "Tipo", "type": "select", "options": ["nascimento"]}
  ]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import uuid
from datetime import datetime
from typing import Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(PROJECT_ROOT)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from sqlalchemy import create_engine, text  # noqa: E402

from apps.backend.app.core.settings import settings  # noqa: E402


def _read_json(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict) and "services" in payload:
        return payload["services"] or []
    if isinstance(payload, dict) and "forms" in payload:
        return payload["forms"] or []
    if isinstance(payload, list):
        return payload
    return []


def _read_csv(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def _is_forms_payload(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        return isinstance(payload, dict) and "forms" in payload
    except Exception:
        return False


def import_forms(path: str) -> None:
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, echo=False)

    forms = _read_json(path)
    if not forms:
        print("No forms found in input file.")
        return

    created_at = datetime.utcnow()
    with engine.connect() as conn:
        with conn.begin():
            for item in forms:
                service_code = item.get("service_code") or item.get("code")
                schema = item.get("schema")
                if not service_code or not schema:
                    continue
                conn.execute(
                    text(
                        """
                        INSERT INTO service_forms (
                            id, service_code, version, schema, is_active, created_at, updated_at
                        ) VALUES (
                            :id, :service_code, :version, :schema, true, :created_at, :updated_at
                        )
                        ON CONFLICT (service_code) DO UPDATE SET
                            schema = EXCLUDED.schema,
                            version = EXCLUDED.version,
                            updated_at = EXCLUDED.updated_at
                        """
                    ),
                    {
                        "id": str(uuid.uuid4()),
                        "service_code": service_code,
                        "version": str(item.get("version") or "1"),
                        "schema": json.dumps(schema),
                        "created_at": created_at,
                        "updated_at": created_at,
                    },
                )

    print(f"Imported {len(forms)} forms from {path}.")


def _auto_form_schema(item: dict[str, Any]) -> dict[str, Any]:
    code = item["code"].lower()
    name = item["name"].lower()
    fields: list[dict[str, Any]] = []
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

    if "certidao" in code or "registro" in name or "registo" in name:
        fields.append(
            {
                "key": "certificate_type",
                "label": "Tipo de certidao",
                "type": "select",
                "required": True,
                "options": ["nascimento", "casamento", "obito", "outra"],
            }
        )

    if (
        any(keyword in code for keyword in ["agua", "energy", "energia", "water"])
        or "ligacao" in name
    ):
        fields.append(
            {
                "key": "address",
                "label": "Morada",
                "type": "text",
                "required": True,
                "placeholder": "Rua, bairro, municipio",
            }
        )

    fields.append(
        {
            "key": "delivery_mode",
            "label": "Entrega",
            "type": "radio",
            "required": True,
            "options": ["digital", "presencial", "expresso"],
        }
    )
    fields.append(
        {
            "key": "supporting_files",
            "label": "Anexos",
            "type": "upload",
            "required": False,
            "multiple": True,
        }
    )
    fields.append(
        {
            "key": "terms_accept",
            "label": "Confirmo que os dados sao verdadeiros",
            "type": "checkbox",
            "required": True,
        }
    )
    fields.append({"key": "notes", "label": "Observacoes", "type": "textarea", "required": False})

    schema = {
        "version": "1.0",
        "groups": [
            {"key": "identity", "label": "Identificacao", "fields": base_fields},
            {"key": "request", "label": "Detalhes do pedido", "fields": fields},
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
            },
        ],
    }
    return schema


def _normalize_item(raw: dict[str, Any]) -> dict[str, Any]:
    code = (raw.get("code") or raw.get("service_code") or raw.get("service_id") or "").strip()
    if not code:
        code = f"SERVICE_{uuid.uuid4().hex[:8].upper()}"
    name = (raw.get("name") or raw.get("service_name") or code).strip()
    category = (raw.get("category") or raw.get("module") or raw.get("domain") or "").strip() or None
    description = (raw.get("description") or raw.get("details") or name).strip() or None
    price_raw = raw.get("price") or raw.get("amount") or raw.get("valor") or 0
    try:
        price = float(price_raw)
    except Exception:
        price = 0.0
    base_hours_raw = raw.get("base_hours") or raw.get("base_hours_default") or 24
    try:
        base_hours = float(base_hours_raw)
    except Exception:
        base_hours = 24.0
    priority = (raw.get("priority") or "medium").lower()
    tier = (raw.get("tier") or "silver").lower()
    version = str(raw.get("version") or "1.0")
    legal_basis = raw.get("legal_basis")
    form_fields = (
        raw.get("form_schema")
        or raw.get("form_schema_json")
        or raw.get("form_fields")
        or raw.get("fields")
        or raw.get("form_fields_json")
    )
    if isinstance(form_fields, str):
        try:
            form_fields = json.loads(form_fields)
        except Exception:
            form_fields = None
    if not form_fields:
        form_fields = _auto_form_schema(
            {
                "code": code,
                "name": name,
            }
        )
    if isinstance(form_fields, list):
        form_fields = {
            "version": "1.0",
            "groups": [
                {"key": "default", "label": "Formulario", "fields": form_fields},
            ],
            "validations": [],
            "dependencies": [],
        }
    return {
        "code": code,
        "name": name,
        "category": category,
        "description": description,
        "price": price,
        "base_hours": base_hours,
        "priority": priority,
        "tier": tier,
        "version": version,
        "legal_basis": legal_basis,
        "form_fields": form_fields,
    }


def import_catalog(path: str, to_sla_base: bool = True, to_service_catalog: bool = True) -> None:
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, echo=False)

    ext = os.path.splitext(path)[1].lower()
    if ext in (".json", ".jsn"):
        raw_items = _read_json(path)
    elif ext in (".csv",):
        raw_items = _read_csv(path)
    else:
        raise ValueError("Unsupported file type. Use JSON or CSV.")

    items = [_normalize_item(raw) for raw in raw_items]
    if not items:
        print("No services found in input file.")
        return

    created_at = datetime.utcnow()
    with engine.connect() as conn:
        with conn.begin():
            for item in items:
                if to_service_catalog:
                    conn.execute(
                        text(
                            """
                            INSERT INTO service_catalog (
                                id, service_code, name, category, description, price, is_active, created_at, updated_at
                            ) VALUES (
                                :id, :service_code, :name, :category, :description, :price, true, :created_at, :updated_at
                            )
                            ON CONFLICT (service_code) DO UPDATE SET
                                name = EXCLUDED.name,
                                category = EXCLUDED.category,
                                description = EXCLUDED.description,
                                price = EXCLUDED.price,
                                updated_at = EXCLUDED.updated_at
                            """
                        ),
                        {
                            "id": str(uuid.uuid4()),
                            "service_code": item["code"],
                            "name": item["name"],
                            "category": item["category"],
                            "description": item["description"],
                            "price": item["price"],
                            "created_at": created_at,
                            "updated_at": created_at,
                        },
                    )

                    if item["form_fields"]:
                        conn.execute(
                            text(
                                """
                                INSERT INTO service_forms (
                                    id, service_code, version, schema, is_active, created_at, updated_at
                                ) VALUES (
                                    :id, :service_code, :version, :schema, true, :created_at, :updated_at
                                )
                                ON CONFLICT (service_code) DO UPDATE SET
                                    schema = EXCLUDED.schema,
                                    version = EXCLUDED.version,
                                    updated_at = EXCLUDED.updated_at
                                """
                            ),
                            {
                                "id": str(uuid.uuid4()),
                                "service_code": item["code"],
                                "version": "1",
                                "schema": json.dumps(item["form_fields"]),
                                "created_at": created_at,
                                "updated_at": created_at,
                            },
                        )

                if to_sla_base:
                    conn.execute(
                        text(
                            """
                            INSERT INTO sla_base (
                                id, service_id, service_name, module, base_hours, priority, tier, version, legal_basis
                            ) VALUES (
                                :id, :service_id, :service_name, :module, :base_hours, :priority, :tier, :version, :legal_basis
                            )
                            ON CONFLICT (service_id) DO UPDATE SET
                                service_name = EXCLUDED.service_name,
                                module = EXCLUDED.module,
                                base_hours = EXCLUDED.base_hours,
                                priority = EXCLUDED.priority,
                                tier = EXCLUDED.tier,
                                version = EXCLUDED.version,
                                legal_basis = EXCLUDED.legal_basis
                            """
                        ),
                        {
                            "id": str(uuid.uuid4()),
                            "service_id": item["code"],
                            "service_name": item["name"],
                            "module": item["category"] or "general",
                            "base_hours": item["base_hours"],
                            "priority": item["priority"],
                            "tier": item["tier"],
                            "version": item["version"],
                            "legal_basis": item["legal_basis"],
                        },
                    )

    print(f"Imported {len(items)} services from {path}.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import service catalog into service_catalog and sla_base"
    )
    parser.add_argument("--file", required=True, help="Path to catalog JSON or CSV")
    parser.add_argument("--no-sla-base", action="store_true", help="Do not insert into sla_base")
    parser.add_argument(
        "--no-service-catalog", action="store_true", help="Do not insert into service_catalog"
    )
    parser.add_argument(
        "--generate-only", action="store_true", help="Only generate normalized JSON output"
    )
    parser.add_argument("--out", help="Optional output file for generated JSON")
    args = parser.parse_args()

    if _is_forms_payload(args.file) and not args.generate_only:
        import_forms(args.file)
        return

    if args.generate_only:
        ext = os.path.splitext(args.file)[1].lower()
        if ext in (".json", ".jsn"):
            raw_items = _read_json(args.file)
        else:
            raw_items = _read_csv(args.file)
        items = [_normalize_item(raw) for raw in raw_items]
        output = {"services": items}
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                json.dump(output, handle, ensure_ascii=False, indent=2)
            print(f"Generated schema file at {args.out}")
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    import_catalog(
        path=args.file,
        to_sla_base=not args.no_sla_base,
        to_service_catalog=not args.no_service_catalog,
    )


if __name__ == "__main__":
    main()
