#!/usr/bin/env python3
"""
catalog_mapper.py
-----------------
Mapeia CSV/JSON bruto para o schema de importacao do SILA (service_catalog).

Uso:
  python scripts/catalog_mapper.py --input raw.csv --output catalog.csv
  python scripts/catalog_mapper.py --input raw.csv --output catalog.json --ministry "Geral"
  python scripts/catalog_mapper.py --input raw.csv --output catalog.csv --schema-template docs/templates/ministry_schema_templates.json

Saida (CSV/JSON) eh compativel com:
  python apps/backend/scripts/import_service_catalog.py --file <saida>
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any

CANONICAL_FIELDS = [
    "service_code",
    "service_name",
    "ministry",
    "category",
    "description",
    "price",
    "currency",
    "base_hours",
    "priority",
    "tier",
    "version",
    "legal_basis",
    "form_schema_json",
]

FIELD_SYNONYMS: dict[str, list[str]] = {
    "service_code": [
        "codigo",
        "code",
        "id_servico",
        "service_id",
        "codigo_servico",
        "servico_id",
        "servico_codigo",
    ],
    "service_name": ["nome", "nome_servico", "servico", "nome do servico", "servico_nome", "name"],
    "ministry": ["ministerio", "orgao", "entidade", "ministry"],
    "category": ["categoria", "module", "modulo", "dominio", "domain", "area", "setor", "category"],
    "description": ["descricao", "detalhe", "details", "resumo", "summary", "description"],
    "price": ["valor", "preco", "taxa", "custo", "amount", "price"],
    "currency": ["moeda", "currency"],
    "base_hours": ["sla", "sla_hours", "tempo", "prazo", "prazo_horas", "base_hours"],
    "priority": ["prioridade", "priority"],
    "tier": ["nivel", "tier"],
    "version": ["versao", "version"],
    "legal_basis": ["base_legal", "lei", "decreto", "legal_basis"],
    "form_schema_json": [
        "schema",
        "form_schema",
        "form_schema_json",
        "form",
        "formulario",
        "formulario_json",
        "fields",
        "campos",
    ],
}


@dataclass
class MappingResult:
    mapped: dict[str, str]
    unmapped: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _build_mapping(columns: Iterable[str]) -> MappingResult:
    normalized_cols = {_normalize(col): col for col in columns}
    mapped: dict[str, str] = {}
    used_cols: set[str] = set()

    for canonical in CANONICAL_FIELDS:
        candidates = FIELD_SYNONYMS.get(canonical, []) + [canonical]
        found = None
        for candidate in candidates:
            norm_candidate = _normalize(candidate)
            if norm_candidate in normalized_cols:
                found = normalized_cols[norm_candidate]
                break
        if not found:
            # Fuzzy match
            best_score = 0.0
            best_col = None
            for norm_col, original in normalized_cols.items():
                score = _similarity(norm_col, canonical)
                if score > best_score:
                    best_score = score
                    best_col = original
            if best_score >= 0.78:
                found = best_col
        if found and found not in used_cols:
            mapped[canonical] = found
            used_cols.add(found)

    unmapped = [col for col in columns if col not in used_cols]
    return MappingResult(mapped=mapped, unmapped=unmapped)


def _infer_type(value: str, column_name: str) -> str:
    name = _normalize(column_name)
    if "anexo" in name or "documento" in name or "upload" in name:
        return "upload"
    if "email" in name:
        return "text"
    if "data" in name or "date" in name or re.match(r"\\d{4}-\\d{2}-\\d{2}", value or ""):
        return "date"
    if value is None:
        return "text"
    value_str = str(value).strip()
    if value_str.lower() in {"true", "false", "sim", "nao", "não"}:
        return "checkbox"
    if re.match(r"^-?\\d+(\\.\\d+)?$", value_str):
        return "number"
    if len(value_str) > 120:
        return "textarea"
    return "text"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", _normalize(text)).strip("_")
    return slug or "field"


def _build_schema_from_columns(row: Mapping[str, Any], extra_columns: list[str]) -> dict[str, Any]:
    fields: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for col in extra_columns:
        value = row.get(col)
        field_type = _infer_type("" if value is None else str(value), col)
        required = bool(re.search(r"(obrigatorio|obrigatório|\\*)", col.lower()))
        key = _slugify(col)
        field: dict[str, Any] = {
            "key": key,
            "label": col.strip(),
            "type": field_type,
            "required": required,
        }
        if field_type == "upload":
            field["multiple"] = True
        if "nif" in col.lower():
            field["mask"] = "nif"
            validations.append(
                {
                    "field": key,
                    "type": "regex",
                    "pattern": "^\\d{10}$",
                    "message": "NIF invalido.",
                }
            )
        if "bi" in col.lower() or "bilhete" in col.lower():
            field["mask"] = "bi"
            validations.append(
                {
                    "field": key,
                    "type": "regex",
                    "pattern": "^[0-9A-Z]{14}$",
                    "message": "Numero BI invalido.",
                }
            )
        fields.append(field)

    schema = {
        "version": "1.0",
        "groups": [
            {"key": "auto", "label": "Formulario", "fields": fields},
        ],
        "validations": validations,
        "dependencies": [],
    }
    return schema


def _load_schema_template(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict) and "schema" in payload:
        return payload["schema"]
    if isinstance(payload, dict):
        return payload
    return None


def _read_rows(input_path: str) -> list[dict[str, Any]]:
    ext = os.path.splitext(input_path)[1].lower()
    if ext in {".json", ".jsn"}:
        with open(input_path, encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict) and "services" in payload:
            return payload["services"]
        if isinstance(payload, list):
            return payload
        raise ValueError("JSON invalido: esperado lista ou {'services': []}.")
    if ext in {".csv"}:
        with open(input_path, encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return [row for row in reader]
    raise ValueError("Formato nao suportado. Use CSV ou JSON.")


def map_raw_to_sila(
    input_path: str, output_path: str, ministry_default: str, schema_template: dict[str, Any] | None
) -> None:
    rows = _read_rows(input_path)
    if not rows:
        raise ValueError("Nenhuma linha encontrada no arquivo de entrada.")

    columns = list(rows[0].keys())
    mapping = _build_mapping(columns)
    output: list[dict[str, Any]] = []
    now = datetime.utcnow().isoformat()

    for row in rows:
        item: dict[str, Any] = {}
        for canonical, source in mapping.mapped.items():
            item[canonical] = row.get(source)

        if not item.get("service_code"):
            item["service_code"] = f"SERVICE_{len(output) + 1:04d}"
        if not item.get("service_name"):
            item["service_name"] = item["service_code"]
        if not item.get("ministry"):
            item["ministry"] = ministry_default

        item.setdefault("version", "1.0")
        item.setdefault("priority", "medium")
        item.setdefault("tier", "silver")
        item.setdefault("base_hours", 24)
        item.setdefault("price", 0)
        item.setdefault("description", item["service_name"])

        if not item.get("form_schema_json"):
            if schema_template:
                item["form_schema_json"] = json.dumps(schema_template, ensure_ascii=False)
            else:
                schema = _build_schema_from_columns(row, mapping.unmapped)
                item["form_schema_json"] = json.dumps(schema, ensure_ascii=False)

        item["mapped_at"] = now
        output.append(item)

    ext = os.path.splitext(output_path)[1].lower()
    if ext in {".json", ".jsn"}:
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(output, handle, ensure_ascii=False, indent=2)
        return

    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        fieldnames = CANONICAL_FIELDS + ["mapped_at"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in output:
            writer.writerow({key: item.get(key, "") for key in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description="Mapear CSV/JSON bruto para catalogo SILA.")
    parser.add_argument("--input", required=True, help="Arquivo de entrada CSV/JSON.")
    parser.add_argument("--output", required=True, help="Arquivo de saida CSV/JSON.")
    parser.add_argument(
        "--ministry", default="Geral", help="Ministerio default quando nao houver coluna."
    )
    parser.add_argument("--schema-template", help="JSON com schema base para todos os servicos.")
    args = parser.parse_args()

    schema_template = _load_schema_template(args.schema_template)
    map_raw_to_sila(args.input, args.output, args.ministry, schema_template)
    print(f"Arquivo gerado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
