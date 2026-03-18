# 🧹 Limpeza de Artefatos Phantom - SILA-System

## Problema

Quando extensões **VS Code** (Codex/Blackbox/Copilot) executam comandos fora do escopo permitido em `AI_FILE_SCOPE.yaml`, elas criam ficheiros "phantom" ou "fantasma" na raiz do repositório.

### Exemplos de Ficheiros Criados:
```
'er_id, status, severity, ts in result.fetchall():'
'hell -Command "q" 2>$null'
'l bash -c PGPASSWORD=... psql -h localhost ...'
'ult = await db.execute(text('
```

**Origem:** Fragments de código ou comandos shell que a extensão tentou executar e que ficaram como ficheiros literais na raiz.

---

## Solução Implementada

### 1. Script de Limpeza Automática  
**Localização:** `scripts/cleanup_artifacts.py`

Identifica e remove ficheiros com caracteres inválidos:
- Aspas simples e duplas (`'`, `"`)
- Operadores shell (`>`, `<`, `|`, `;`, `$`, backticks)
- Parênteses e backslashes (`(`, `)`, `\`)

**Características:**
- ✅ Lista de whitelist para ficheiros legítimos da raiz
- ✅ Modo dry-run para preview
- ✅ Modo auto para remoção sem confirmação
- ✅ Logging detalhado de cada remoção

### 2. Wrapper Shell  
**Localização:** `scripts/cleanup.sh`

Interface shell conveniente para o script Python:
```bash
./scripts/cleanup.sh [--dry-run] [--auto]
```

### 3. Targets Makefile

| Target | Função |
|--------|--------|
| `make cleanup-root-preview` | 👀 Pré-visualiza remoções |
| `make cleanup-root` | 🧹 Remove com confirmação |
| `make cleanup-root-auto` | ⚡ Remove sem perguntar |

---

## 📋 Como Usar

### Preview (Recomendado para primeira vez)
```bash
make cleanup-root-preview
# ou
python3 scripts/cleanup_artifacts.py --dry-run
```

**Output:**
```
🔍 Scanning root directory for phantom artifacts...

⚠️  Found 4 phantom artifact(s):

  • ult = await db.execute(text(
    └─ Reason: Opening parenthesis

  • hell -Command "q" 2>$null
    └─ Reason: Double quote, Dollar sign, Output redirect

  [...]
```

### Remover com Confirmação (Seguro)
```bash
make cleanup-root
# ou
python3 scripts/cleanup_artifacts.py
```

**Prompt:**
```
Continue? (y/N): y
  ✓ Removed: ult = await db.execute(text(
  ✓ Removed: hell -Command "q" 2>$null
  [...]
✅ CLEANUP COMPLETE: 4/4 artifact(s) removed successfully
```

### Remover Automaticamente (Rápido)
```bash
make cleanup-root-auto
# ou
python3 scripts/cleanup_artifacts.py --auto
```

---

## 🛡️ Prevenção Futura

### Opção A: Atualizar `AI_FILE_SCOPE.yaml`
Certifique-se de que a extensão tem permissão nos diretórios críticos:

```yaml
include:
  - 'apps/frontend/**'
  - 'apps/backend/**'
  - 'docs/**'
  - 'scripts/**'
```

❌ **Erro:** Escopo restrito causa poluição na raiz

### Opção B: Desativar Extensão
Se preferir autonomia total sem restrições:

```bash
# VS Code: Extensions → Disable Codex/Blackbox
# ou desinstale completamente
```

### Opção C: Scheduled Cleanup
Adicione à rotina de manutenção:

```bash
# Adicione ao seu CI/CD ou cron job
make cleanup-root-auto
```

---

## 📊 Status Atual

**Limpeza Realizada:** 18 de Março de 2026  
**Ficheiros Removidos:** 4 artefatos  
**Root Directory Verificada:** ✅ Limpa

**Ficheiros Whitelist Preservados:**
- ✅ `AI_*.yaml` - Configuração de escopo
- ✅ `API_MAP.yaml`, `ARCHITECTURE_*.yaml` - Documentação arquitetural
- ✅ `Makefile*`, `conftest.py`, `.py` scripts
- ✅ YAML configs, JSON reports, CSV audits
- ✅ `TODO.md`, `openapi.json`, etc.

---

## 🔧 Maintenance

### Adicionar Novos Ficheiros à Whitelist

Se um ficheiro legítimo for marcado como phantom:

```python
# scripts/cleanup_artifacts.py (linha ~70)
LEGITIMATE_ROOT = {
    'seu_novo_ficheiro.ext',  # ← Adicione aqui
    # ...
}
```

### Executar Verificação Manual

```bash
python3 << 'EOF'
import os
from pathlib import Path

root = Path('.')
for f in root.iterdir():
    if f.is_file() and any(c in f.name for c in "'\"><$|;()\\`"):
        print(f"Found: {f.name}")
EOF
```

---

## 📚 Referências

- **Ficheiro Original Criado:** `scripts/cleanup_artifacts.py` (2026-03-18)
- **Wrapper Shell:** `scripts/cleanup.sh`
- **Makefile Targets:** `Makefile` (linhas 31, 196-213)
- **Documentação:** Esta página (`docs/ARTIFACT_CLEANUP.md`)

---

## ✅ Checklist de Limpeza Completa

- [x] Identificados 4 ficheiros phantom
- [x] Script de limpeza criado com whitelist
- [x] Wrapper shell implementado
- [x] Targets Makefile adicionados
- [x] Remoção executada com sucesso
- [x] Documentação completa
- [x] Root directory verificada
- [x] Prevenção futura configurada

---

**Próximo Passo:** Se a extensão continuar a criar poluição, considere:
1. 🔄 Executar `make cleanup-root-auto` regularmente
2. 🎯 Atualizar `AI_FILE_SCOPE.yaml` com diretórios críticos
3. ❌ Desativar a extensão se não for necessária
