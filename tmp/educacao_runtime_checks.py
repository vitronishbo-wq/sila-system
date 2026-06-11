#!/usr/bin/env python3
import time
import json
import jwt
import requests
from datetime import datetime, timedelta

# Config
BASE_URL = "http://127.0.0.1:8000"
import os

# Load SECRET from backend .env if present (preferred)
SECRET = "Trumanmarcelo_1983_SILA_SECRET_KEY_2026"
env_path = os.path.join(os.path.dirname(__file__), "..", "apps", "backend", ".env")
env_path = os.path.abspath(env_path)
if os.path.exists(env_path):
    try:
        with open(env_path, "r") as f:
            for line in f:
                if line.strip().startswith("SECRET_KEY="):
                    SECRET = line.strip().split("=", 1)[1]
                    break
    except Exception:
        pass
ALG = "HS256"

# Known IDs from DB inspection
CITIZEN_ID = "11111111-1111-4111-8111-111111111111"
MATRICULA_ID = "22222222-2222-4222-8222-222222222222"
BOLETIM_ID = "33333333-3333-4333-8333-333333333333"
CERTIFICADO_ID = "44444444-4444-4444-8444-444444444444"
ESCOLA_ID = "0a59f4cb-2086-4a7f-809f-65ca08a7a9f9"
TURMA_ID = "9dd7ebad-d831-4f48-b177-6f2f6d87d0f7"

# Province IDs (from locations)
HUAMBO_PROVINCE_ID = "fc6cbec6-82f1-457a-98bf-c696aec41c3c"
BENGUELA_PROVINCE_ID = "5932eb58-8131-4cba-a4d8-5005b3b8bd2e"

now = int(time.time())

def make_token(sub: str, roles: list[str], email: str, territory_id: str | None = None) -> str:
    payload = {
        "sub": sub,
        "type": "access",
        "iat": now,
        "exp": now + 3600,
        "realm_access": {"roles": roles},
        "email": email,
    }
    if territory_id:
        payload["territory_id"] = territory_id
    return jwt.encode(payload, SECRET, algorithm=ALG)

# Tokens
prov_huambo_token = make_token("prov_huambo", ["MANAGER"], "prov_huambo@example.com", HUAMBO_PROVINCE_ID)
prov_benguela_token = make_token("prov_benguela", ["MANAGER"], "prov_benguela@example.com", BENGUELA_PROVINCE_ID)
citizen_token = make_token("citizen_demo", ["CITIZEN"], "citizen@example.com")

headers_huambo = {"Authorization": f"Bearer {prov_huambo_token}"}
headers_benguela = {"Authorization": f"Bearer {prov_benguela_token}"}
headers_citizen = {"Authorization": f"Bearer {citizen_token}"}

out = {"phase1": {}, "phase2": {}, "phase3": {}, "collected_at": datetime.utcnow().isoformat()+"Z"}

# Helper to call an endpoint and record

def _safe_parse_json(r):
    try:
        return r.json()
    except Exception:
        # some endpoints may return plain strings
        text = r.text
        # try to interpret as JSON-like string
        try:
            return json.loads(text)
        except Exception:
            return text


def call_get(path: str, headers: dict) -> dict:
    url = BASE_URL + path
    start = time.perf_counter()
    r = requests.get(url, headers=headers, timeout=30)
    elapsed = time.perf_counter() - start
    entry = {"status": r.status_code, "time_s": round(elapsed, 3)}
    parsed = _safe_parse_json(r)
    entry["raw"] = parsed
    # normalize counts
    if isinstance(parsed, list):
        entry["count"] = len(parsed)
    elif isinstance(parsed, dict):
        # common pattern: top-level keys map to lists
        counts = {k: (len(v) if isinstance(v, list) else None) for k, v in parsed.items()}
        entry["counts"] = counts
    else:
        entry["text"] = str(parsed)[:500]
    return entry

# Phase 1 - Validate APIs
out["phase1"]["escolas_huambo"] = call_get("/escolas/", headers_huambo)
out["phase1"]["escolas_benguela"] = call_get("/escolas/", headers_benguela)
out["phase1"]["turmas_huambo"] = call_get("/turmas/", headers_huambo)
out["phase1"]["turmas_benguela"] = call_get("/turmas/", headers_benguela)
out["phase1"]["matriculas_citizen"] = call_get(f"/matriculas/citizen/{CITIZEN_ID}", headers_citizen)
out["phase1"]["fuc_citizen"] = call_get(f"/fuc/{CITIZEN_ID}/educacao", headers_citizen)

# Phase 2 - Validate chain
fuc = out["phase1"]["fuc_citizen"].get("json") or {}
matriculas = out["phase1"]["matriculas_citizen"].get("json") or []

chain_ok = {
    "matricula_present": any((str(m.get("id")) == MATRICULA_ID) for m in matriculas),
    "boletim_present": any((b.get("id") == BOLETIM_ID or str(b.get("id")) == BOLETIM_ID) for b in (fuc.get("boletins") or [])),
    "certificado_present": any((c.get("id") == CERTIFICADO_ID or str(c.get("id")) == CERTIFICADO_ID) for c in (fuc.get("certificados") or [])),
}
out["phase2"]["chain_check"] = chain_ok
out["phase2"]["matriculas_sample"] = matriculas[:3]
out["phase2"]["fuc_sample"] = {k: (v[:3] if isinstance(v, list) else v) for k, v in fuc.items()}

# Phase 3 - Territorial checks (read-only)
# List escolas filtered by provincia param
out["phase3"]= {}
# try Huambo filter and Benguela filter with both tokens
out["phase3"]["huambo_user_list_huambo"] = call_get("/escolas/?provincia=Huambo", headers_huambo)
out["phase3"]["huambo_user_list_benguela"] = call_get("/escolas/?provincia=Benguela", headers_huambo)
out["phase3"]["benguela_user_list_benguela"] = call_get("/escolas/?provincia=Benguela", headers_benguela)
out["phase3"]["benguela_user_list_huambo"] = call_get("/escolas/?provincia=Huambo", headers_benguela)

# Also try reading the specific matricula record via citizen token (list_by_citizen already done)
out["phase3"]["matricula_citizen_read"] = out["phase1"]["matriculas_citizen"]
# Try to read boletins for citizen via workflow endpoint
out["phase3"]["boletins_citizen"] = call_get(f"/boletins/workflow/citizen/{CITIZEN_ID}", headers_citizen)

# Generate markdown report
md_lines = []
md_lines.append("# VALIDACAO_RUNTIME_EDUCACAO")
md_lines.append("")
md_lines.append(f"Data: {out['collected_at']}")
md_lines.append("")
md_lines.append("## Resumo Phase 1 — APIs")
for k, v in out["phase1"].items():
    md_lines.append(f"- **{k}**: status={v.get('status')} time={v.get('time_s')}s count={v.get('count', 'N/A')} ")
md_lines.append("")
md_lines.append("## Resumo Phase 2 — Cadeia Educacional")
md_lines.append(f"- Matricula presente: {chain_ok['matricula_present']}")
md_lines.append(f"- Boletim presente: {chain_ok['boletim_present']}")
md_lines.append(f"- Certificado presente: {chain_ok['certificado_present']}")
md_lines.append("")
md_lines.append("### Matriculas sample")
md_lines.append(json.dumps(out['phase2']['matriculas_sample'], indent=2))
md_lines.append("")
md_lines.append("### FUC summary")
md_lines.append(json.dumps({k: (len(v) if isinstance(v, list) else None) for k, v in (fuc.items() if fuc else {})}, indent=2))
md_lines.append("")
md_lines.append("## Resumo Phase 3 — Territorial checks")
for k, v in out["phase3"].items():
    md_lines.append(f"- **{k}**: status={v.get('status')} time={v.get('time_s')}s count={v.get('count', v.get('counts', 'N/A'))}")

md = "\n".join(md_lines)
with open("VALIDACAO_RUNTIME_EDUCACAO.md", "w") as f:
    f.write(md)

print(json.dumps(out, indent=2))
print("\nWrote VALIDACAO_RUNTIME_EDUCACAO.md")
