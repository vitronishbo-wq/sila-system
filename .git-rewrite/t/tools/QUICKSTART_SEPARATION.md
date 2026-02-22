# ⚡ Guia Rápido - Separação Models/Schemas

## 🎯 Para um módulo específico (Recomendado)

```bash
# Migração completa em um comando
python tools/migrate_module.py backend/modules/location
```

Isso executa automaticamente:

1. ✅ Validação inicial
2. 🔧 Separação models/schemas
3. 🔍 Auditoria e correção de imports
4. ✅ Validação final
5. 🧪 Sugestões de testes

---

## 🌍 Para TODOS os módulos

```bash
# 1. Simular primeiro (SEMPRE!)
python tools/migrate_all_modules.py --dry-run

# 2. Se tudo OK, executar
python tools/migrate_all_modules.py

# 3. Validar tudo
python tools/validate_separation.py --all

# 4. Testar
pytest tests/
```

---

## 🔧 Uso Individual das Ferramentas

### 1. Separar manualmente

```bash
python tools/split_models_schemas.py backend/modules/location
```

### 2. Auditar imports

```bash
python tools/audit_imports.py --module location --fix
```

### 3. Validar

```bash
python tools/validate_separation.py backend/modules/location
```

---

## 🚨 Troubleshooting Rápido

### Problema: Python não encontrado

```bash
# Use python3 ou especifique o caminho
python3 tools/migrate_module.py backend/modules/location
```

### Problema: Módulo não encontrado

```bash
# Verifique o caminho (deve ser relativo ao root)
ls backend/modules/location/models.py
```

### Problema: Imports quebrados

```bash
# Execute o auditor
python tools/audit_imports.py --fix
```

### Problema: Testes falhando

```bash
# Verifique imports nos testes
grep -r "from.*models import.*Create" tests/
grep -r "from.*models import.*Response" tests/
```

---

## 📋 Checklist Rápido

Antes de commitar:

```bash
# 1. Validar separação
python tools/validate_separation.py --all

# 2. Verificar imports
python tools/audit_imports.py

# 3. Executar testes
pytest tests/

# 4. Verificar sintaxe
python -m py_compile backend/modules/*/models.py
python -m py_compile backend/modules/*/schemas.py

# 5. Revisar mudanças
git diff backend/modules/
```

---

## 🎓 Exemplos Práticos

### Exemplo 1: Migrar módulo location

```bash
cd /path/to/sila-system
python tools/migrate_module.py backend/modules/location
pytest tests/modules/location/ -v
git add backend/modules/location/
git commit -m "refactor(location): separate models and schemas"
```

### Exemplo 2: Migrar múltiplos módulos

```bash
# Migrar location, payment e journeys
for module in location payment journeys; do
    python tools/migrate_module.py backend/modules/$module
done

# Validar todos
python tools/validate_separation.py --all

# Testar todos
pytest tests/modules/{location,payment,journeys}/ -v
```

### Exemplo 3: Migrar tudo exceto alguns

```bash
python tools/migrate_all_modules.py --exclude legacy,deprecated
```

---

## 💡 Dicas

1. **Sempre use --dry-run primeiro** para ver o que vai acontecer
2. **Backups são criados automaticamente** (.py.bak)
3. **Execute testes após cada migração**
4. **Revise as mudanças com git diff**
5. **Faça commits pequenos** (um módulo por vez)

---

## 🆘 Ajuda

Para mais detalhes, veja:

- [README_SEPARATION.md](./README_SEPARATION.md) - Documentação completa
- [INDEX_SCRIPTS.md](../INDEX_SCRIPTS.md) - Índice de todos os scripts

Ou execute com `--help`:

```bash
python tools/migrate_module.py --help
python tools/split_models_schemas.py --help
python tools/audit_imports.py --help
python tools/validate_separation.py --help
```
