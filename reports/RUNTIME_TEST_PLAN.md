# Runtime Test Plan — PolicyEngine + Middleware Validation

Objetivo
- Validar em runtime se `PolicyEngine`, `PermissionGuard` e os middlewares (ex.: `TrustEvaluationMiddleware`) estão a aplicar corretamente roles, permissões e regras territoriais.

Pré-requisitos
- Ter uma instância da API disponível (`BASE_URL`) com os loaders e middlewares carregados (ou ambiente de homologação equivalente).
- Ter `python3` e `requests` instalados no ambiente que executa os testes.
- Arquivo de endpoints a testar: `reports/ENDPOINTS_TO_TEST.json` (pode partir do template `reports/ENDPOINTS_TO_TEST_TEMPLATE.json`).

Fluxo resumido
1. Gerar JWTs válidos para perfis de teste usando `JWTHandler(secret_key=settings.SECRET_KEY)`.
2. Para cada endpoint e para cada perfil: executar chamada HTTP com `Authorization: Bearer <token>` e cabeçalhos de confiança (`X-Device-Score`, `X-Biometric-Score`, `X-Behavior-Score`, `X-MFA-Token` quando aplicável).
3. Gravar `status_code`, headers e corpo de resposta em `reports/RUNTIME_TEST_RESULTS.json`.
4. Classificar cada par (endpoint, perfil) como `CONFIRMADO` / `FALSO POSITIVO` / `NÃO TESTÁVEL` com base no arquivo de expectativas (`expected_by_profile`) presente em `ENDPOINTS_TO_TEST.json`.

Perfis e mapeamento (sugestão)
- `citizen`: realm role `CITIZEN`, `territory_id` => local citizen territory (ex: `mun-001`).
- `operator`: realm role `MANAGER`, email prefix may indicate tipo (ex.: `mun123@` → municipal manager).
- `municipal_admin`: realm role `MANAGER`, `email` e `territory_id` apontando para município.
- `provincial_admin`: realm role `MANAGER`, `email` e `territory_id` apontando para província.
- `central_admin`: realm role `ADMIN` or omit `territory_id` (user considered national when `territory_id` missing).
- `super_admin`: realm role `SUPERADMIN`.

Cabeçalhos de confiança (TrustEvaluationMiddleware)
- Para evitar bloqueios por trust, envie cabeçalhos altos (ex.: `0.98`) e um `X-MFA-Token` quando necessário:

```
X-Device-Score: 0.98
X-Biometric-Score: 0.98
X-Behavior-Score: 0.98
X-MFA-Token: mfa-test
```

Exemplo: gerar um token via Python (usado também pelo runner)

```python
from apps.backend.core.auth.jwt_handler import JWTHandler
from apps.backend.app.core.settings import settings

jwt = JWTHandler(secret_key=settings.SECRET_KEY)
claims = {
    "email": "prov001-admin@example.com",
    "realm_access": {"roles": ["MANAGER"]},
    "territory_id": "prov-001",
}
token = jwt.create_access_token(subject=claims["email"], data=claims)
print(token)
```

Execução (runner)
- Preencha/edite `reports/ENDPOINTS_TO_TEST.json` (ou use o template `reports/ENDPOINTS_TO_TEST_TEMPLATE.json`).
- Execute o runner:

```bash
BASE_URL=http://localhost:8000 python3 scripts/runtime_test_runner.py reports/ENDPOINTS_TO_TEST.json
```

Classificação (automática quando `expected_by_profile` fornecido)
- Para cada par (endpoint, perfil):
  - Se `expected_by_profile[perfil] == "allow"` e resposta é 2xx → `CONFIRMADO`.
  - Se `expected_by_profile[perfil] == "allow"` e resposta é 401/403 → `FALSO POSITIVO` (esperava permitir, foi negado).
  - Se `expected_by_profile[perfil] == "deny"` and resposta is 2xx → `FALSO POSITIVO` (esperava negar, foi permitido).
  - Se servidor inacessível / endpoint não exposto / TrustMiddleware bloqueia mesmo com headers altos → `NÃO TESTÁVEL`.

Saída
- `reports/RUNTIME_TEST_RESULTS.json`: resultados não-interpretados (por endpoint, por perfil).
- `reports/RUNTIME_TEST_SUMMARY.md`: sumarização (runner gera um JSON; uso do `jq` ou conversão opcional para MD disponível).

Observações importantes
- O projeto contém múltiplas instâncias locais de `PolicyEngine()` em módulos; assegure que o ambiente de teste replica a configuração de runtime (carregadores e políticas registradas). O runner apenas testa comportamento observável.
- Preencha `expected_by_profile` em `ENDPOINTS_TO_TEST.json` para permitir classificação automática.

Próximo passo
- Executar o runner contra a instância de homologação/`run-local` e revisar `reports/RUNTIME_TEST_RESULTS.json`. Posso ajudar a interpretar os resultados e gerar o relatório final `CONFIRMADO` / `FALSO POSITIVO` / `NÃO TESTÁVEL`.
