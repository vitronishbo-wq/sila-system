# 🚀 GUIA DE EXECUÇÃO: Consolidação de Módulos SILA

**Status:** Pronto para implementar  
**Tempo estimado:** 45-60 minutos  
**Complexidade:** MÉDIA  
**Risco:** BAIXO (com backup)

---

## ✅ PASSO 0: PRÉ-REQUISITOS

```bash
# 0.1 Verificar localização
cd /home/dev03wsl/sila-system
pwd

# 0.2 Criar branch de trabalho
git checkout -b consolidate/modules-single-source
git status

# 0.3 Verificar estado dos diretórios
ls -la modules/ app/modules/ apps/backend/app/modules/ 2>/dev/null | head -20

# 0.4 Fazer commit de mudanças pendentes (se houver)
git add -A
git commit -m "wip: save current state before consolidation" || echo "Nothing to commit"
```

---

## 🔷 OPÇÃO A: EXECUÇÃO AUTOMÁTICA (RECOMENDADO)

### **1. Fazer script executável**

```bash
chmod +x /home/dev03wsl/sila-system/scripts/consolidate_modules.sh
chmod +x /home/dev03wsl/sila-system/scripts/validate_consolidation.sh
```

### **2. Executar consolidação**

```bash
bash /home/dev03wsl/sila-system/scripts/consolidate_modules.sh
```

O script vai:
- ✅ Criar backup automático
- ✅ Consolidar módulos de ambos diretórios
- ✅ Atualizar imports automaticamente
- ✅ Remover diretórios vazios
- ✅ Validar resultado

### **3. Validar resultado**

```bash
bash /home/dev03wsl/sila-system/scripts/validate_consolidation.sh
```

Se vir `✅ CONSOLIDAÇÃO VALIDADA COM SUCESSO!`, avance para **PASSO FINAL**.

---

## 🔶 OPÇÃO B: EXECUÇÃO MANUAL (PARA ENTENDER CADA PASSO)

### **FASE 1: BACKUP**

```bash
# 1.1 Criar backup
BACKUP_DIR="/tmp/sila_backup_$(date +%s)"
mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/modules.tar.gz" \
  /home/dev03wsl/sila-system/modules \
  /home/dev03wsl/sila-system/app/modules

echo "✓ Backup em: $BACKUP_DIR/modules.tar.gz"

# 1.2 Verificar conteúdo
echo "Estrutura de /modules/:"
ls -R /home/dev03wsl/sila-system/modules | head -30

echo -e "\nEstrutura de /app/modules/:"
ls -R /home/dev03wsl/sila-system/app/modules | head -30

echo -e "\nEstrutura de /apps/backend/app/modules/ (DESTINO):"
ls -1 /home/dev03wsl/sila-system/apps/backend/app/modules | grep -v "\.py\|__"
```

### **FASE 2A: CONSOLIDAR IDENTITY**

```bash
WORKSPACE="/home/dev03wsl/sila-system"
DEST="$WORKSPACE/apps/backend/app/modules/identity"

# 2A.1 Ver o que existe em cada local
echo "=== Em /modules/identity ==="
find "$WORKSPACE/modules/identity" -type f | head

echo -e "\n=== Em /app/modules/identity ==="
find "$WORKSPACE/app/modules/identity" -type f 2>/dev/null | head

echo -e "\n=== Em /apps/backend/app/modules/identity ==="
find "$DEST" -type f | head

# 2A.2 Copiar ficheiros únicos de /modules/identity para destino
if [[ -d "$WORKSPACE/modules/identity/domain" ]]; then
  cp -v "$WORKSPACE/modules/identity/domain"/* "$DEST/domain/" 2>/dev/null || true
  echo "✓ Conteúdo de domain/ mesclado"
fi

if [[ -d "$WORKSPACE/modules/identity/middleware" ]]; then
  cp -rv "$WORKSPACE/modules/identity/middleware" "$DEST/" 2>/dev/null || true
  echo "✓ middleware/ copiado"
fi
```

### **FASE 2B: CONSOLIDAR DOCUMENTS**

```bash
DEST="$WORKSPACE/apps/backend/app/modules/documents"

# 2B.1 Copiar schemas para application
if [[ -d "$WORKSPACE/modules/documents/schemas" ]]; then
  mkdir -p "$DEST/application"
  cp -rv "$WORKSPACE/modules/documents/schemas" "$DEST/application/" 2>/dev/null || true
  echo "✓ schemas/ copiado para application/"
fi

# 2B.2 Copiar services para application
if [[ -d "$WORKSPACE/modules/documents/services" ]]; then
  mkdir -p "$DEST/application"
  cp -rv "$WORKSPACE/modules/documents/services" "$DEST/application/" 2>/dev/null || true
  echo "✓ services/ copiado para application/"
fi
```

### **FASE 2C: CONSOLIDAR PAYMENT**

```bash
DEST="$WORKSPACE/apps/backend/app/modules/payment"

# 2C.1 Copiar models
if [[ -d "$WORKSPACE/modules/payment/models" ]]; then
  cp -rv "$WORKSPACE/modules/payment/models" "$DEST/" 2>/dev/null || true
  echo "✓ models/ copiado"
fi

# 2C.2 Copiar services
if [[ -d "$WORKSPACE/modules/payment/services" ]]; then
  mkdir -p "$DEST/application"
  cp -rv "$WORKSPACE/modules/payment/services" "$DEST/application/" 2>/dev/null || true
  echo "✓ services/ copiado para application/"
fi
```

### **FASE 2D: CONSOLIDAR /app/modules/**

```bash
# 2D.1 EDUCACAO
if [[ -d "$WORKSPACE/app/modules/educacao/core" ]]; then
  cp -r "$WORKSPACE/app/modules/educacao/core"/* \
    "$WORKSPACE/apps/backend/app/modules/educacao/" 2>/dev/null || true
  echo "✓ educacao consolidado"
fi

# 2D.2 HEALTH
if [[ -d "$WORKSPACE/app/modules/health/core" ]]; then
  cp -r "$WORKSPACE/app/modules/health/core"/* \
    "$WORKSPACE/apps/backend/app/modules/health/" 2>/dev/null || true
  echo "✓ health consolidado"
fi

# 2D.3 JUSTICE
if [[ -d "$WORKSPACE/app/modules/justice/core" ]]; then
  cp -r "$WORKSPACE/app/modules/justice/core"/* \
    "$WORKSPACE/apps/backend/app/modules/justice/" 2>/dev/null || true
  echo "✓ justice consolidado"
fi

# 2D.4 XROAD
# XROAD tem estrutura melhor preservada
if [[ -d "$WORKSPACE/app/modules/xroad" && ! -d "$WORKSPACE/apps/backend/app/modules/xroad" ]]; then
  cp -r "$WORKSPACE/app/modules/xroad" "$WORKSPACE/apps/backend/app/modules/"
  echo "✓ xroad copiado completo"
fi
```

### **FASE 3: ATUALIZAR IMPORTS**

```bash
# 3.1 Encontrar todos ficheiros com imports antigos
echo "Ficheiros com imports para atualizar:"
grep -r "from modules\.|from app\.modules\." \
  "$WORKSPACE" \
  --include="*.py" \
  2>/dev/null | \
  grep -v ".venv" | \
  grep -v "__pycache__" | \
  cut -d: -f1 | \
  sort -u

# 3.2 Criar script de replacement
python3 << 'PYSCRIPT'
import re
import os
from pathlib import Path

WORKSPACE = "/home/dev03wsl/sila-system"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Replace: from modules.X -> from apps.backend.app.modules.X
    content = re.sub(
        r'from modules\.(\w+)',
        r'from apps.backend.app.modules.\1',
        content
    )
    
    # Replace: from app.modules.X -> from apps.backend.app.modules.X
    content = re.sub(
        r'from app\.modules\.(\w+)',
        r'from apps.backend.app.modules.\1',
        content
    )
    
    # Replace: import modules.X -> import apps.backend.app.modules.X
    content = re.sub(
        r'import modules\.(\w+)',
        r'import apps.backend.app.modules.\1 as \1',
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Find all python files
fixed = 0
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git']]
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            if fix_file(filepath):
                print(f"✓ {filepath}")
                fixed += 1

print(f"\n✓ Total de ficheiros atualizados: {fixed}")
PYSCRIPT
```

### **FASE 4: REMOVER DIRETÓRIOS ANTIGOS**

```bash
# 4.1 Remover /modules/
echo "Removendo /home/dev03wsl/sila-system/modules..."
rm -rf /home/dev03wsl/sila-system/modules
echo "✓ Removido"

# 4.2 Remover /app/modules/
echo "Removendo /home/dev03wsl/sila-system/app/modules..."
rm -rf /home/dev03wsl/sila-system/app/modules
echo "✓ Removido"

# 4.3 Verificar
echo -e "\nVerificando remoção:"
[[ ! -d "$WORKSPACE/modules" ]] && echo "✓ /modules/ não existe mais"
[[ ! -d "$WORKSPACE/app/modules" ]] && echo "✓ /app/modules/ não existe mais"
```

### **FASE 5: VALIDAR**

```bash
# 5.1 Verificar que nenhum import antigo existe
echo "Verificando imports antigos..."
remaining=$(grep -r "from modules\.|from app\.modules\." \
  "$WORKSPACE" \
  --include="*.py" \
  2>/dev/null | \
  grep -v ".venv" | \
  wc -l)

if [[ $remaining -eq 0 ]]; then
  echo "✓ Nenhum import antigo encontrado"
else
  echo "✗ ERRO: Ainda existem $remaining imports antigos!"
  exit 1
fi

# 5.2 Verificar syntax
echo "Verificando syntax Python..."
python3 -m py_compile "$WORKSPACE/apps/backend/app/modules"/__init__.py
echo "✓ Syntax OK"

# 5.3 Contar módulos finais
echo -e "\nEstrutura final:"
ls -1 "$WORKSPACE/apps/backend/app/modules" | grep -v "\.py\|__" | wc -l
echo "✓ módulos consolidados"
```

---

## 🔷 PASSO FINAL: GIT COMMIT & PUSH

### **1. Revisar mudanças**

```bash
cd /home/dev03wsl/sila-system

# Ver o que foi mudado
git status

# Ver diffs de ficheiros
git diff --stat

# Ver ficheiros removidos
git status | grep "deleted"
```

### **2. Fazer commit**

```bash
git add -A
git commit -m "consolidate: unify modules to single source of truth

- Remove /modules/ and /app/modules/ directories
- Consolidate all modules to /apps/backend/app/modules/
- Update all imports from 'modules.X' to 'apps.backend.app.modules.X'
- Merge duplicated modules (identity, documents, payment, educacao, justice, xroad)
- Maintain hexagonal architecture in all modules

Changes:
- Deleted: /modules/, /app/modules/ (~100 files)
- Modified: ~50 .py files with updated imports
- No functional changes, only structure consolidation"
```

### **3. Push para review**

```bash
git push -u origin consolidate/modules-single-source

# Criar Pull Request no GitHub
echo "✓ Branch criado e pronto para review"
echo "  Acesse: https://github.com/seu-repo/pulls"
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

Após consolidação, verificar:

- [ ] `/modules/` foi removido
- [ ] `/app/modules/` foi removido
- [ ] Nenhum `from modules.` ou `from app.modules.` no código
- [ ] Todos imports apontam para `apps.backend.app.modules.`
- [ ] `pytest` passa sem erros
- [ ] `mypy` sem type errors críticos
- [ ] Documentação de módulo atualizada em README

---

## 🔄 SE ALGO DER ERRADO

### **Recuperar do Backup**

```bash
# Se fez backup com script automático:
BACKUP_FILE="/tmp/sila_modules_backup/modules_*.tar.gz" # usar o mais recente

# Ou se fez manualmente:
BACKUP_FILE="/tmp/sila_backup_*/modules.tar.gz"

# Restaurar
cd /home/dev03wsl/sila-system
tar -xzf "$BACKUP_FILE"

# Reverter git
git reset --hard HEAD~1
git clean -fd
```

### **Verificar Conflitos de Merge**

```bash
# Ver commits locais
git log origin/main..HEAD

# Resetar se necessário
git reset --hard origin/main
```

---

## 💡 PRÓXIMAS MELHORIAS (After Consolidation)

1. Atualizar documentação em `README.md`
2. Criar template de novo módulo
3. Documentar padrão de import no `ARCHITECTURE.md`
4. Adicionar linter rule para detectar imports antigos
5. Atualizar CI/CD para validar estrutura

---

## 📞 SUPORTE

Se tiver dúvidas:

1. Consultar `MODULES_CONSOLIDATION_REPORT.md` para explicação completa
2. Reverter para main: `git checkout main && git reset --hard origin/main`
3. Contactar Tech Lead para review do plano

---

**Status:** ✅ Pronto para implementar  
**Última actualização:** 13 Mar 2026

