# 🛡️ Sila System - AI Guardrails & Safety Manual

Este manual define as proteções técnicas que impedem a degradação da arquitetura durante o desenvolvimento autônomo.

## 🥅 Definição de Guardrails

Os Guardrails são scripts de verificação estática e dinâmica que validam a integridade do sistema.

### 1. Guardrail de Arquitetura (DDD Integrity)
Implementado em `scripts/architecture_scan.py` e disparado por `make architecture-guardrails`.
- **O que verifica**:
    - Imports proibidos (ex: Domain importando FastAPI).
    - Estrutura de pastas incompleta em novos módulos.
    - Ciclos de dependência entre módulos.

### 2. Guardrail de Qualidade (Static Analysis)
- **Flake8**: Garante conformidade com PEP 8.
- **Mypy**: Garante que o sistema de tipos não foi violado.
- **Ruff (se disponível)**: Linting ultra-rápido.

### 3. Guardrail de Segurança (Secret Scanning)
- A IA nunca deve ler ou mover arquivos `.env` para pastas públicas.
- Verificação via `scripts/verify_audit_artifacts.sh` para garantir que segredos não vazaram em logs.

---

## 🚦 Protocolo de Execução

Ao modificar o código, a IA deve seguir o sinalizador de segurança:

1. **🔴 Vermelho (Pós-Mudança)**:
    - O código foi escrito mas ainda não validado.
    - **Ação**: Rodar `make lint architecture-guardrails`.

2. **🟡 Amarelo (Ajuste)**:
    - Erros detectados pelos guardrails.
    - **Ação**: Corrigir erro e rodar novamente.

3. **🟢 Verde (Concluído)**:
    - Todos os guardrails passaram.
    - **Ação**: O trabalho pode ser considerado finalizado.

---

## 🆘 Resolução de Problemas Comuns

- **"ModuleNotFoundError"**: Geralmente causado por import relativo ou falta de `__init__.py`. Verifique [AI_ARCHITECTURE_GUIDE.md](./AI_ARCHITECTURE_GUIDE.md).
- **"Architecture Violation Detected"**: Você tentou importar algo de `infrastructure` dentro do `domain`. Mova a interface para `application/` ou use injeção de dependência.
- **"Missing Migration"**: Banco de Dados está desalinhado com os Modelos. Rode `alembic upgrade head`.

---
*A segurança do sistema é prioridade sobre a velocidade de entrega.*
