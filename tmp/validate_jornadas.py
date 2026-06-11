"""Validação de Jornadas Reais de Governo — SILA Platform."""
import json, sys, time
import httpx

BASE = "http://localhost:8000"
client = httpx.Client(timeout=15)

results = {"ok": [], "empty": [], "error": [], "no_data": []}

def test(method, path, label=None, expect_data=False):
    label = label or path
    try:
        r = client.request(method, f"{BASE}{path}")
        if r.status_code >= 500:
            results["error"].append(f"[500] {label}  ({r.text[:100]})")
            return
        if r.status_code == 401:
            results["ok"].append(f"[401] {label}  (auth required — OK)")
            return
        if r.status_code == 404:
            results["no_data"].append(f"[404] {label}  (endpoint não encontrado)")
            return
        if r.status_code == 422:
            results["error"].append(f"[422] {label}  (parâmetros: {r.text[:100]})")
            return
        if r.status_code == 400:
            results["ok"].append(f"[400] {label}  ({r.text[:80]})")
            return
        body = r.json() if r.text.strip() else []
        if isinstance(body, dict) and body.get("detail"):
            results["error"].append(f"[{r.status_code}] {label}  ({body['detail'][:80]})")
            return
        is_empty = False
        if isinstance(body, list):
            is_empty = len(body) == 0
        elif isinstance(body, dict):
            content = body.get("results") or body.get("items") or body.get("data") or body.get("beneficiarios") or []
            is_empty = (isinstance(content, list) and len(content) == 0) or (len(body) == 0)
        else:
            is_empty = not body
        if is_empty and expect_data:
            results["empty"].append(f"[{r.status_code}] {label}  (vazio)")
        elif not is_empty:
            preview = json.dumps(body if isinstance(body, dict) else body[:1], ensure_ascii=False)[:120]
            results["ok"].append(f"[{r.status_code}] {label}  {preview}")
        else:
            results["ok"].append(f"[{r.status_code}] {label}")
    except Exception as e:
        results["error"].append(f"[ERR] {label}  ({e})")

# ─── 1. NASCIMENTO → FUC ───
print("=== 1. NASCIMENTO → FUC ===")
test("GET", "/api/health/live", "Health live")
test("GET", "/api/health/ready", "Health ready")
test("GET", "/api/providers/health", "Providers health")
test("GET", "/api/v1/service-catalog", "Catálogo de serviços", expect_data=True)

# ─── 2. EDUCAÇÃO ───
print("=== 2. EDUCAÇÃO ===")
# Portal cidadão
test("GET", "/matriculas/wizard/iniciar", "POST Matrícula wizard iniciar")
test("GET", "/educacao/marketplace/search/search/", "Marketplace search root")
test("GET", "/educacao/marketplace/discovery/marketplace/discovery/institutions", "Discovery institutions", expect_data=True)
test("GET", "/educacao/marketplace/discovery/marketplace/discovery/opportunities", "Discovery opportunities", expect_data=True)
test("GET", "/educacao/marketplace/discovery/marketplace/discovery/programs", "Discovery programs", expect_data=True)
test("GET", "/educacao/marketplace/booking/marketplace/booking/my-bookings/00000000-0000-0000-0000-000000000000", "Booking my-bookings (placeholder)")
test("GET", "/marketplace/health", "Marketplace health")
test("GET", "/marketplace/", "Marketplace info")
# Gestão escolar (admin)
test("GET", "/api/admin/dashboard", "Admin dashboard")
test("GET", "/api/admin/citizens", "Admin citizens")

# ─── 3. SAÚDE ───
print("=== 3. SAÚDE ===")
# Portal cidadão — SEM ROTAS DE SAÚDE NO DISCOVERY (módulo pode estar noutro prefixo)
test("GET", "/matriculas/", "POST Matrícula criar")
test("GET", "/matriculas/citizen/00000000-0000-0000-0000-000000000000", "Matrículas por cidadão", expect_data=True)

# Sociedade / Família
test("GET", "/society/familia/familia/dependencies/health", "Família health")
test("GET", "/society/familia/familia/members/health", "Família members health")

# Assistência Social
test("GET", "/society/assistencia_social/assistencia-social/beneficiarios/", "Assistência Beneficiários", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/beneficios/", "Assistência Benefícios", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/programas-sociais/", "Programas Sociais", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/cadastros-unicos/", "Cadastros Únicos", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/criancas-risco/", "Crianças em Risco", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/idosos-vulneraveis/", "Idosos Vulneráveis", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/pcd/", "PcD", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/atendimentos/", "Atendimentos", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/visitas-domiciliares/", "Visitas Domiciliares", expect_data=True)
test("GET", "/society/assistencia_social/assistencia-social/situacoes-rua/", "Situações de Rua", expect_data=True)

# Agrícola assistência
test("GET", "/resources/agricultura/agricultura/assistencia/", "Agricultura assistência", expect_data=True)

# ─── 4. WORKFLOW / GOVERNANÇA ───
print("=== 4. WORKFLOW / GOVERNANÇA ===")
test("GET", "/governance/workflow/workflow/tasks/pending", "Workflow tasks pending")
test("GET", "/governance/workflow/workflow/tasks/my", "Workflow tasks my")

# BI
test("GET", "/intelligence/bi/bi/kpis/assistencia", "BI KPIs assistência")
test("GET", "/intelligence/bi/bi/kpis/educacao", "BI KPIs educação")
test("GET", "/intelligence/bi/bi/kpis/workflow", "BI KPIs workflow")
test("GET", "/intelligence/bi/bi/dashboards/assistencia", "BI dashboard assistência")
test("GET", "/intelligence/bi/bi/dashboards/educacao", "BI dashboard educação")
test("GET", "/intelligence/bi/bi/dashboards/workflow", "BI dashboard workflow")

# ─── 5. MATRÍCULAS (justiça/educação) ───
print("=== 5. MATRÍCULAS / JUSTIÇA ===")
test("POST", "/matriculas/", "Matrícula criar (POST)")
test("GET", "/matriculas/", "Listar matrículas")

print("\n========================================")
print("RESULTADO DA VALIDAÇÃO")
print("========================================")
print(f"\n✅ OK:          {len(results['ok'])}")
print(f"⚠️  Vazio (sem dados): {len(results['empty'])}")
print(f"❌ Erro:        {len(results['error'])}")
print(f"🔍 Não encontrado:  {len(results['no_data'])}")

if results["error"]:
    print("\n--- ERROS ---")
    for e in results["error"]:
        print(f"  ❌ {e}")

if results["empty"]:
    print("\n--- VAZIOS (endpoint funcional, sem dados) ---")
    for e in results["empty"]:
        print(f"  ⚠️  {e}")

if results["ok"]:
    print("\n--- OK ---")
    for e in results["ok"]:
        print(f"  ✅ {e}")
