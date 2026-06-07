"""
Blueprint Keycloak (A)
Esqueleto de integracao do oidc_provider com Keycloak
"""

# Blueprint Keycloak (A)

## Objetivo
Definir o caminho de integracao do `oidc_provider` com o `core/auth`,
padronizando o fluxo JWT -> claims -> roles/perms.

## Parametros esperados (Realm / Client)
- `KEYCLOAK_ISSUER`: issuer do realm (ex.: `https://auth.sila.gov.ao/realms/sila`)
- `KEYCLOAK_JWKS_URL`: endpoint JWKS (ex.: `.../protocol/openid-connect/certs`)
- `KEYCLOAK_CLIENT_ID`: client id usado para `resource_access`

## Claims -> Roles/Perms (mapeamento base)
- `realm_access.roles` -> roles do realm
- `resource_access[client_id].roles` -> roles do client
- `roles` (se presente) -> roles diretas

Permissoes internas sao derivadas via `RoleManager`:
- roles do token -> `RoleManager.get_permissions(role)`

## Adaptor (KeycloakAuthProvider)
Arquivo: `apps/backend/core/auth/providers/keycloak.py`

Responsabilidades:
- validar JWT via JWKS (RS256)
- checar issuer e audience
- extrair roles do token
- mapear para permissoes internas

## Config/env
Adicionar no `apps/backend/env.example`:
- `KEYCLOAK_ISSUER`
- `KEYCLOAK_JWKS_URL`
- `KEYCLOAK_CLIENT_ID`

## Smoke test (fluxo minimo)
1. Receber `token` do Keycloak
2. `KeycloakAuthProvider.authenticate(token)`
3. Verificar retorno:
   - `subject` (sub)
   - `roles`
   - `permissions`
   - `claims`
