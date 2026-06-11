---
version: 1
enforce: true
owners:
  - platform-team
last_updated: 2026-06-09
ci_check: .github/workflows/verify-agent-rules.yml
---

SILA Workspace

Root: /home/dev03wsl/sila-system

Modules: apps/backend/app/modules/

Architecture: Hexagonal + X-Road interoperability

BOOTSTRAP OBRIGATÓRIO

Carregar e seguir AGENT_RULES.md antes de qualquer ação.

Fontes de verdade

docs/tree.json

docs/modules/tree.modules.json

Comandos principais

- `make update-indexes`
- `make daily-audit`

# Regras do núcleo
- Veja: apps/backend/app/core/governance/GOVERNANCE_RULES.md