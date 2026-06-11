# ACCESS_ENFORCEMENT_REPORT

Resumo gerado a partir do inventário estático (scanner AST) — foco: endpoints administrativos.

- Endpoints administrativos identificados: 11

| Route | Method | Module | File | Role exigida | Permission exigida | Territorial aplicado? | Cidadão acede? | Admin Municipal acede (cross-territory)? | Admin Provincial acede (cross-territory)? | Admin Nacional acede? | Resultado |
|---|---:|---|---|---|---|---|---|---|---|---:|
| /educacao/admin/workflows/transferencia/criar | POST | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/workflows/transferencia/avancar | POST | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /registo-civil/health | GET | administracao-local/api/health.py | apps/backend/app/modules/administracao-local/api/health.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /administracao-local/administradores/{admin_id} | GET | governance/administracao_local/presentation/router.py | apps/backend/app/modules/governance/administracao_local/presentation/router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/roles | GET | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/roles/{role}/permissions | GET | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/scope/check | GET | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/workflows/matricula/criar | POST | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/workflows/matricula/avancar | POST | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/delegation/delegate | POST | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |
| /educacao/admin/delegation/list/{delegate_id} | GET | educacao/rbac/admin_router.py | apps/backend/app/modules/educacao/rbac/admin_router.py | N/D | N/D | NÃO | SIM | SIM (sem verificação territorial) | SIM (sem verificação territorial) | SIM | FALHA |