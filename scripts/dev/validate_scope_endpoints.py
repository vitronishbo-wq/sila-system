#!/usr/bin/env python3
"""
Lightweight validation script that calls a subset of admin endpoints
from `apps.backend.app.platform.runtime.compat_router` directly using a
fake async DB session. This avoids bringing up the whole app and lets
us verify scoping logic paths quickly.

Run: python3 scripts/dev/validate_scope_endpoints.py
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List
import os
import sys

# Ensure repo root is importable when running this script directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure application package imports that expect `core` as top-level work
APP_PKG = os.path.abspath(os.path.join(ROOT, "apps/backend/app"))
if APP_PKG not in sys.path:
    sys.path.append(APP_PKG)

# Also expose `apps/backend` so top-level `core` package (used in some providers)
# can be imported as `core.*` during lightweight module imports.
APPS_BACKEND = os.path.abspath(os.path.join(ROOT, "apps/backend"))
if APPS_BACKEND not in sys.path:
    sys.path.append(APPS_BACKEND)

from apps.backend.app.platform.runtime import compat_router as cr


class FakeResult:
    def __init__(self, rows=None, scalar=None):
        self._rows = rows or []
        self._scalar = scalar

    def mappings(self):
        return self

    def all(self):
        return self._rows

    def scalars(self):
        class Scalars:
            def __init__(self, vals):
                self._vals = vals

            def all(self):
                return self._vals

        return Scalars(self._rows)

    def scalar_one(self):
        if self._scalar is not None:
            return self._scalar
        if self._rows:
            # If it's a one-row scalar-ish response
            first = self._rows[0]
            if isinstance(first, dict):
                return first
            return first
        return None

    def scalar_one_or_none(self):
        return self.scalar_one()

    def first(self):
        return self._rows[0] if self._rows else None


class DBStub:
    def __init__(self, provinces, municipalities, communes, citizens, documents, closure_map):
        self.provinces = provinces
        self.municipalities = municipalities
        self.communes = communes
        self.citizens = citizens
        self.documents = documents
        self.closure_map = closure_map

    async def execute(self, query, params=None):
        sql = str(query).lower()
        params = params or {}

        # Provinces (unscoped)
        if "where type = 'province'" in sql and "parent_id is null" in sql:
            return FakeResult(rows=self.provinces)

        # Provinces via closure
        if "from territory_closure tc" in sql and "a.type = 'province'" in sql:
            allowed = params.get("allowed_ids") or []
            rows = []
            for anc, descendants in self.closure_map.items():
                if any(d in allowed for d in descendants):
                    for p in self.provinces:
                        if p["id"] == anc:
                            rows.append(p)
            return FakeResult(rows=rows)

        # Municipalities - simple parent lookup
        if "where type = 'municipality'" in sql and "parent_id = :province_id::uuid" in sql:
            province_id = params.get("province_id")
            rows = [m for m in self.municipalities if m.get("parent_id") == province_id]
            return FakeResult(rows=rows)

        # Municipalities with allowed_ids filtering
        if "from locations m" in sql and "m.type = 'municipality'" in sql and "m.parent_id = :province_id::uuid" in sql:
            province_id = params.get("province_id")
            allowed = params.get("allowed_ids") or []
            rows = []
            for m in self.municipalities:
                if m.get("parent_id") == province_id:
                    if m.get("id") in allowed or any(d in allowed for d in self.closure_map.get(m.get("id"), [])):
                        rows.append(m)
            return FakeResult(rows=rows)

        # Permission checks against territory_closure
        if "select 1 from territory_closure" in sql:
            ancestor_id = params.get("province_id") or params.get("municipality_id") or params.get("ancestor_id")
            allowed = params.get("allowed_ids") or []
            if not ancestor_id:
                return FakeResult(rows=[])
            descendants = self.closure_map.get(ancestor_id, [])
            if any(d in allowed for d in descendants):
                return FakeResult(rows=[(1,)])
            return FakeResult(rows=[])

        # Communes by parent
        if "where type = 'commune'" in sql and "parent_id = :municipality_id::uuid" in sql:
            municipality_id = params.get("municipality_id")
            rows = [c for c in self.communes if c.get("parent_id") == municipality_id]
            return FakeResult(rows=rows)

        # Citizens (count and select)
        if "from citizenship_citizens" in sql:
            allowed = params.get("allowed_ids")
            if allowed:
                filtered = [c for c in self.citizens if c.get("residence_location_id") in allowed or c.get("birth_location_id") in allowed]
            else:
                filtered = list(self.citizens)
            if "count(" in sql:
                return FakeResult(scalar=len(filtered))
            return FakeResult(rows=filtered)

        # Documents
        if "from wallet_documents d" in sql:
            allowed = params.get("allowed_ids")
            rows = []
            for doc in self.documents:
                citizen = next((c for c in self.citizens if c.get("id") == doc.get("citizen_id")), None)
                if not citizen:
                    continue
                if allowed:
                    if citizen.get("residence_location_id") in allowed or citizen.get("birth_location_id") in allowed:
                        merged = {**doc, "citizen_name": citizen.get("name"), "bi_number": citizen.get("bi_number"), "citizen_email": citizen.get("email")}
                        rows.append(merged)
                else:
                    merged = {**doc, "citizen_name": citizen.get("name"), "bi_number": citizen.get("bi_number"), "citizen_email": citizen.get("email")}
                    rows.append(merged)
            return FakeResult(rows=rows)

        # Default empty
        return FakeResult(rows=[])


async def run_validation():
    # Sample data
    provinces = [
        {"id": "prov1", "name": "Huambo", "code": "HU", "type": "province", "parent_id": None},
        {"id": "prov2", "name": "Luanda", "code": "LU", "type": "province", "parent_id": None},
    ]

    municipalities = [
        {"id": "mun1", "name": "Huambo City", "code": "HU-1", "type": "municipality", "parent_id": "prov1"},
        {"id": "mun2", "name": "Luanda City", "code": "LU-1", "type": "municipality", "parent_id": "prov2"},
    ]

    communes = [
        {"id": "com1", "name": "Comuna A", "code": "C1", "type": "commune", "parent_id": "mun1"},
        {"id": "com2", "name": "Comuna B", "code": "C2", "type": "commune", "parent_id": "mun2"},
    ]

    citizens = [
        {"id": "cit1", "name": "Alice", "email": "alice@example.com", "bi_number": "BI123", "birth_location_id": "prov1", "residence_location_id": "mun1", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow(), "is_active": True},
        {"id": "cit2", "name": "Bob", "email": "bob@example.com", "bi_number": "BI456", "birth_location_id": "prov2", "residence_location_id": "mun2", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow(), "is_active": True},
    ]

    documents = [
        {"id": "doc1", "citizen_id": "cit1", "document_type": "BI", "file_url": "/files/1", "issued_at": datetime.utcnow(), "valid_until": None},
        {"id": "doc2", "citizen_id": "cit2", "document_type": "BI", "file_url": "/files/2", "issued_at": datetime.utcnow(), "valid_until": None},
    ]

    closure_map = {
        "prov1": ["prov1", "mun1", "com1", "school1"],
        "prov2": ["prov2", "mun2", "com2"],
        "mun1": ["mun1", "com1", "school1"],
        "mun2": ["mun2", "com2"],
        "com1": ["com1"],
        "com2": ["com2"],
        "school1": ["school1"],
    }

    db = DBStub(provinces, municipalities, communes, citizens, documents, closure_map)

    central_scope = {"role": "ADMIN_CENTRAL", "allowed_territories": None}
    prov_scope = {"role": "ADMIN_PROVINCIAL", "allowed_territories": ["prov1", "mun1", "com1", "school1"]}
    mun_scope = {"role": "ADMIN_MUNICIPAL", "allowed_territories": ["mun1", "com1", "school1"]}
    school_scope = {"role": "ADMIN_COMMUNAL", "allowed_territories": ["school1"]}

    print("\n--- CENTRAL USER ---")
    provs = await cr.admin_list_provinces(current_user={"role": "ADMIN_CENTRAL"}, db=db, scope=central_scope)
    print("Provinces visible:", [p.get("id") for p in provs])
    muns = await cr.admin_list_municipalities("prov1", current_user={"role": "ADMIN_CENTRAL"}, db=db, scope=central_scope)
    print("Municipalities for prov1:", [m.get("id") for m in muns])
    citizens_res = await cr.admin_list_citizens(current_user={"role": "ADMIN_CENTRAL"}, db=db, scope=central_scope)
    print("Citizens total:", citizens_res.get("total"), "ids:", [c.get("id") for c in citizens_res.get("items")])

    print("\n--- PROVINCIAL USER (prov1) ---")
    provs_p = await cr.admin_list_provinces(current_user={"role": "ADMIN_PROVINCIAL"}, db=db, scope=prov_scope)
    print("Provinces visible:", [p.get("id") for p in provs_p])
    muns_p = await cr.admin_list_municipalities("prov1", current_user={"role": "ADMIN_PROVINCIAL"}, db=db, scope=prov_scope)
    print("Municipalities for prov1:", [m.get("id") for m in muns_p])
    citizens_p = await cr.admin_list_citizens(current_user={"role": "ADMIN_PROVINCIAL"}, db=db, scope=prov_scope)
    print("Citizens total:", citizens_p.get("total"), "ids:", [c.get("id") for c in citizens_p.get("items")])

    print("\n--- MUNICIPAL USER (mun1) ---")
    provs_m = await cr.admin_list_provinces(current_user={"role": "ADMIN_MUNICIPAL"}, db=db, scope=mun_scope)
    print("Provinces visible:", [p.get("id") for p in provs_m])
    muns_m = await cr.admin_list_municipalities("prov1", current_user={"role": "ADMIN_MUNICIPAL"}, db=db, scope=mun_scope)
    print("Municipalities for prov1 (as municipal user):", [m.get("id") for m in muns_m])
    citizens_m = await cr.admin_list_citizens(current_user={"role": "ADMIN_MUNICIPAL"}, db=db, scope=mun_scope)
    print("Citizens total:", citizens_m.get("total"), "ids:", [c.get("id") for c in citizens_m.get("items")])

    print("\n--- SCHOOL USER (school1) ---")
    provs_s = await cr.admin_list_provinces(current_user={"role": "ADMIN_COMMUNAL"}, db=db, scope=school_scope)
    print("Provinces visible:", [p.get("id") for p in provs_s])
    citizens_s = await cr.admin_list_citizens(current_user={"role": "ADMIN_COMMUNAL"}, db=db, scope=school_scope)
    print("Citizens total:", citizens_s.get("total"), "ids:", [c.get("id") for c in citizens_s.get("items")])


if __name__ == "__main__":
    asyncio.run(run_validation())
