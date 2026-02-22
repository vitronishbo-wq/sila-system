# 🔧 Dev Setup Helper - `dev_setup.ps1`

> **Consolidador automatizado de setup de desenvolvimento** para o SILA System. Este
> script detecta e invoca scripts de setup existentes, ativa ambientes virtuais Python,
> e instala dependências frontend/backend de forma segura e inteligente.

---

## 📋 O que o script faz

1. **Detecta localização do repositório** — Caminha para cima no diretório até encontrar
   `backend/` ou `README.md`
2. **Encontra scripts setup existentes** — Lista scripts candidatos que já fazem
   configurações específicas
3. **Ativa virtualenv Python** — Procura por `.venv`, `venv`, `backend/.venv` ou
   `backend/venv` em ordem de prioridade
4. **Instala dependências Python** — Executa `pip install -r requirements.txt` (raiz
   e/ou backend)
5. **Instala dependências Frontend** — Se `frontend/package.json` existir, roda
   `npm install` ou `npm ci`
6. **Invoca scripts existentes** — Chama setup scripts candidatos de forma
   não-destrutiva
7. **Executa smoke tests (opcional)** — Se `-RunSmoke` for passado, tenta rodar testes
   básicos
8. **Logs coloridos** — Status em verde/amarelo/vermelho para fácil interpretação

---

## 🚀 Quickstart

### Setup básico (recomendado)

```powershell
cd scripts/windows/dev
.\dev_setup.ps1
```

### Com smoke tests

```powershell
.\dev_setup.ps1 -RunSmoke
```

### Sem instalar dependências (apenas ativa venv)

```powershell
.\dev_setup.ps1 -SkipInstall
```

---

## 📋 Pré-requisitos

| Requisito         | Versão Mínima | Por quê                     |
| ----------------- | ------------- | --------------------------- |
| **Python**        | 3.8+          | Backend (FastAPI)           |
| **Node.js / npm** | 16+           | Frontend (React/TypeScript) |
| **Git**           | Qualquer      | Trabalhar com repo          |

**Verificar instalação:**

```powershell
python --version
npm --version
node --version
git --version
```

---

## 🎯 Fluxo de execução em detalhe

### 1. Detecção de repo root

```
script.ps1 location: scripts/windows/dev/
Walk up from: scripts/ → windows/ → dev/ → 🎯 sila-system/ (tem backend/)
RepoRoot = \\wsl.localhost\Ubuntu\home\truman\dev\sila-system
```

### 2. Scripts candidatos encontrados

O script procura por (em ordem):

- `scripts/windows/dev/setup_env.ps1`
- `scripts/windows/dev/setup_project.ps1`
- `scripts/windows/dev/init_project.ps1`
- `automation/setup/setup/setup_sila_env.ps1`
- `automation/setup/setup/setup_env.ps1`

Se encontrados, serão exibidos como "encontrados mas não invocados ainda".

### 3. Ativação de venv

Procura por (em ordem de prioridade):

1. `.venv/Scripts/Activate.ps1` ← **Preferido** (raiz do repo)
2. `venv/Scripts/Activate.ps1`
3. `backend/.venv/Scripts/Activate.ps1` ← **Alternativa** (backend)
4. `backend/venv/Scripts/Activate.ps1`

Assim que encontrar um válido, ativa e para.

**Se nenhum for encontrado:**

```
[WARN] No venv activation script found in typical locations.
       You can create one with: python -m venv .venv
```

### 4. Instalação de deps Python

Se `requirements.txt` existir em:

- `requirements.txt` (raiz)
- `backend/requirements.txt`

Executa:

```powershell
pip install -r <file>
```

### 5. Instalação de deps Frontend

Se `frontend/package.json` ou `apps/frontend/package.json` existir:

```powershell
# Se package-lock.json ou pnpm-lock.yaml existir (preferido, mais rápido)
npm ci

# Senão, instala tudo
npm install
```

### 6. Invoca scripts existentes

Chama cada script candidato encontrado (não-destrutivo):

```powershell
& $scriptPath
```

Captura erros, não interrompe se um falhar.

### 7. Smoke tests (opcional, com `-RunSmoke`)

Procura por:

- `run_dev_env.ps1`
- `scripts/windows/dev/smoke-test.ps1`
- `smoke-test.ps1`

Executa o primeiro encontrado.

---

## 📊 Output esperado

```
=== SILA: Development environment setup helper ===
Repo root: \\wsl.localhost\Ubuntu\home\truman\dev\sila-system

Found existing setup script: ...scripts\windows\dev\setup_env.ps1
Found existing setup script: ...scripts\windows\dev\setup_project.ps1
Found existing setup script: ...scripts\windows\dev\init_project.ps1

Activating venv: .venv\Scripts\Activate.ps1
[OK]  Activated: .venv\Scripts\Activate.ps1

Installing Python dependencies from requirements.txt
[OK]  Installed: requirements.txt

Installing Python dependencies from backend\requirements.txt
[OK]  Installed: backend\requirements.txt

Running: npm ci in frontend
[OK]  Frontend dependencies installed in frontend

Invoking existing script: ...scripts\windows\dev\setup_env.ps1
[OK]  Ran: ...scripts\windows\dev\setup_env.ps1

[OK]  Ran: ...scripts\windows\dev\setup_project.ps1

...

=== dev_setup completed ===
Next steps: verify DB settings, run migrations, and start services as needed.
```

---

## 🔍 Troubleshooting

### ❌ "No venv activation script found"

**Solução:**

```powershell
cd $RepoRoot
python -m venv .venv
.\dev_setup.ps1
```

### ❌ "pip failed: No module named pip"

**Solução:**

```powershell
python -m ensurepip --upgrade
.\dev_setup.ps1
```

### ❌ "npm command not found"

**Solução:**

1. Instale Node.js de https://nodejs.org/
2. Reinicie o PowerShell
3. Verifique: `npm --version`

### ❌ Script não encontra repo root

**Solução:**

```powershell
# Execute direto da raiz do repo
cd \\wsl.localhost\Ubuntu\home\truman\dev\sila-system
.\scripts\windows\dev\dev_setup.ps1
```

### ⚠️ Alguns pacotes falharam a instalar

**Verificar:**

```powershell
pip list
npm list
```

Se faltarem críticos, instale manualmente:

```powershell
pip install fastapi uvicorn sqlalchemy
npm install
```

---

## 🔐 Segurança e boas práticas

✅ **O que o script NÃO faz:**

- Não sobrescreve arquivos existentes
- Não modifica Git config ou branches
- Não instala pacotes globais (tudo fica no venv)
- Não requer admin/sudo
- Não deleta virtualenvs duplicados (apenas avisa)

✅ **Boas práticas implementadas:**

- Verifica existência antes de ativar
- Captura exceções sem interromper fluxo
- Logs detalhados com cores
- Oferece flags `-SkipInstall` e `-RunSmoke` para controle fino

---

## 📝 Exemplos de uso

### Cenário 1: Setup completo na primeira vez

```powershell
cd sila-system
.\scripts\windows\dev\dev_setup.ps1
```

**Resultado esperado:** Venv ativado, deps instaladas, scripts candidatos invocados.

### Cenário 2: Reativar venv após reboot

```powershell
.\scripts\windows\dev\dev_setup.ps1 -SkipInstall
```

**Resultado esperado:** Venv ativado rapidamente, sem reinstalar deps.

### Cenário 3: Verificar que tudo funciona (smoke)

```powershell
.\scripts\windows\dev\dev_setup.ps1 -RunSmoke
```

**Resultado esperado:** Setup + teste básico rodando.

### Cenário 4: Atualizar apenas deps do backend

```powershell
.\scripts\windows\dev\dev_setup.ps1 -SkipInstall
# Depois, manualmente:
pip install -r backend/requirements.txt --upgrade
```

---

## 🔗 Relacionado

- [Quick Start Backend](./QUICK_START_BACKEND.md)
- [Bootstrap Guide](./BOOTSTRAP_README.md)
- [Comandos Essenciais](./COMANDOS_ESSENCIAIS.md)

---

**Última atualização:** Novembro 2025
