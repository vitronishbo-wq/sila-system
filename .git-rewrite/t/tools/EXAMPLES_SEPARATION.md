# 📸 Exemplos Visuais - Sistema de Separação

## 🎬 Cenário 1: Primeiro Uso (Módulo Location)

### Passo 1: Verificar estado atual

```bash
$ cat backend/modules/location/models.py
```

**Antes:**

```python
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel  # ❌ Misturado

class CountryModel(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)

class ProvinceCreate(BaseModel):  # ❌ Schema em models.py
    name: str
    country_id: int
```

### Passo 2: Executar migração

```bash
$ python tools/migrate_module.py backend/modules/location
```

**Output:**

```
🚀 SILA Module Migration Orchestrator
📦 Módulo: location
📂 Caminho: backend/modules/location

============================================================
📍 ETAPA 1: Validação Inicial
============================================================
✅ Módulo encontrado: location
✅ models.py existe

============================================================
📍 ETAPA 2: Separação Models/Schemas
============================================================
🔍 Analisando módulo: backend/modules/location

📦 Encontrados 2 schemas Pydantic:
   • ProvinceCreate
   • ProvinceResponse

💾 Backup criado: backend/modules/location/models.py.bak
✅ Schemas extraídos para: backend/modules/location/schemas.py
✅ Models limpo: backend/modules/location/models.py

============================================================
📍 ETAPA 3: Auditoria de Importações
============================================================
🔍 Auditando imports...
✅ Nenhum problema de import encontrado

============================================================
📍 ETAPA 4: Validação Final
============================================================
📦 Validando módulo: location
   ✅ Separação correta!
   📊 6 modelos ORM
   📊 14 schemas Pydantic

============================================================
✨ MIGRAÇÃO CONCLUÍDA COM SUCESSO!
============================================================
```

### Passo 3: Verificar resultado

```bash
$ cat backend/modules/location/models.py
```

**Depois:**

```python
from sqlalchemy import Column, Integer, String

class CountryModel(Base):  # ✅ Apenas ORM
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
```

```bash
$ cat backend/modules/location/schemas.py
```

```python
from pydantic import BaseModel
from typing import Optional

class ProvinceCreate(BaseModel):  # ✅ Apenas Pydantic
    name: str
    country_id: int
```

---

## 🎬 Cenário 2: Problema de Import Detectado

### Situação: Import incorreto em routes.py

```python
# backend/modules/location/routes.py
from .models import ProvinceCreate  # ❌ ERRADO
```

### Executar auditor

```bash
$ python tools/audit_imports.py --module location
```

**Output:**

```
🔍 Auditando importações em: backend

📦 location: 14 schemas

⚠️  Encontrados 1 problemas em 1 arquivos:

📄 backend/modules/location/routes.py
   Linha 5: from .models import ProvinceCreate
   → Deveria ser: from .schemas import ProvinceCreate

💡 Execute com --fix para corrigir automaticamente
```

### Corrigir automaticamente

```bash
$ python tools/audit_imports.py --module location --fix
```

**Output:**

```
🔧 Aplicando correções...
   ✅ backend/modules/location/routes.py

✨ 1 arquivos corrigidos!
⚠️  Backups criados com extensão .py.bak
```

### Resultado

```python
# backend/modules/location/routes.py
from .schemas import ProvinceCreate  # ✅ CORRETO
```

---

## 🎬 Cenário 3: Validação de Múltiplos Módulos

### Validar todos os módulos

```bash
$ python tools/validate_separation.py --all
```

**Output:**

```
🔍 SILA Separation Validator
============================================================

📦 Validando 3 módulo(s)...

📦 Validando módulo: location
   ✅ Separação correta!
   📊 6 modelos ORM
   📊 14 schemas Pydantic

📦 Validando módulo: payment
   ❌ Classes Pydantic encontradas em models.py: Payment
   📊 1 modelos ORM
   📊 0 schemas Pydantic

📦 Validando módulo: journeys
   ✅ Separação correta!
   📊 3 modelos ORM
   📊 9 schemas Pydantic

============================================================
📊 RELATÓRIO FINAL
============================================================

✅ Estatísticas:
   • Modelos ORM: 10
   • Schemas Pydantic: 23

❌ 1 erro(s) encontrado(s):

   📦 payment / models.py
      Classes Pydantic encontradas em models.py: Payment

⚠️  Ação necessária:
   Execute: python tools/split_models_schemas.py backend/modules/payment
```

---

## 🎬 Cenário 4: Migração em Lote

### Simular migração de todos os módulos

```bash
$ python tools/migrate_all_modules.py --dry-run
```

**Output:**

```
🌍 SILA Batch Module Migration
============================================================
🔍 DRY RUN - Nenhuma modificação será feita

📦 Encontrados 5 módulos:
   • location
   • payment
   • journeys
   • billing
   • training

🚀 Iniciando migração...

============================================================
📦 Migrando: location
============================================================
   ⏭️  Módulo já está limpo

============================================================
📦 Migrando: payment
============================================================
   ✅ Módulo precisa de migração

============================================================
📦 Migrando: journeys
============================================================
   ⏭️  Módulo já está limpo

============================================================
📊 RESUMO DA MIGRAÇÃO
============================================================

✅ Sucesso: 5/5

⏭️  Excluídos: 0
```

### Executar migração real

```bash
$ python tools/migrate_all_modules.py
```

**Output:**

```
⚠️  ATENÇÃO: Esta operação irá modificar múltiplos arquivos!
Continuar? (s/N): s

🚀 Iniciando migração...

[... processo de migração ...]

============================================================
📊 RESUMO DA MIGRAÇÃO
============================================================

✅ Sucesso: 5/5
   • location
   • payment
   • journeys
   • billing
   • training

🎯 Próximos passos:
   1. Executar testes: pytest tests/
   2. Validar todos: python tools/validate_separation.py --all
   3. Revisar mudanças: git diff
   4. Commit: git add . && git commit -m 'refactor: separate models and schemas'
```

---

## 🎬 Cenário 5: Dry-Run (Simulação)

### Simular separação sem modificar

```bash
$ python tools/split_models_schemas.py backend/modules/payment --dry-run
```

**Output:**

```
🔍 Analisando módulo: backend/modules/payment

📦 Encontrados 1 schemas Pydantic:
   • Payment

🔍 DRY RUN - Nenhum arquivo será modificado

============================================================
PREVIEW: schemas.py
============================================================
"""
Location Schemas - Auto-generated

Pydantic schemas for API validation and serialization.
"""

from pydantic import BaseModel

class Payment(BaseModel):
    id: int

============================================================
PREVIEW: models.py (limpo)
============================================================
# (arquivo vazio - sem modelos ORM)
```

---

## 🎬 Cenário 6: Rollback (Restaurar Backup)

### Se algo der errado

```bash
# Restaurar do backup
$ cp backend/modules/location/models.py.bak backend/modules/location/models.py

# Verificar
$ python tools/validate_separation.py backend/modules/location
```

---

## 🎬 Cenário 7: Integração com Git

### Workflow completo

```bash
# 1. Criar branch
$ git checkout -b refactor/separate-models-schemas

# 2. Migrar módulo
$ python tools/migrate_module.py backend/modules/location

# 3. Verificar mudanças
$ git diff backend/modules/location/

# 4. Testar
$ pytest tests/modules/location/ -v

# 5. Commit
$ git add backend/modules/location/
$ git commit -m "refactor(location): separate models and schemas

- Extract Pydantic schemas to schemas.py
- Clean models.py to contain only ORM models
- Update imports in dependent files
- All tests passing"

# 6. Push
$ git push origin refactor/separate-models-schemas
```

---

## 🎬 Cenário 8: CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/validate-separation.yml
name: Validate Models/Schemas Separation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"

      - name: Validate Separation
        run: |
          python tools/validate_separation.py --all
          if [ $? -ne 0 ]; then
            echo "❌ Models/Schemas separation validation failed"
            exit 1
          fi
```

---

## 🎬 Cenário 9: Troubleshooting

### Problema: Testes falhando após migração

```bash
# 1. Identificar imports quebrados
$ grep -r "from.*models import.*Create" tests/modules/location/

tests/modules/location/test_routes.py:5:from backend.modules.location.models import ProvinceCreate

# 2. Corrigir automaticamente
$ python tools/audit_imports.py --fix

# 3. Executar testes novamente
$ pytest tests/modules/location/ -v

# 4. Se ainda falhar, verificar manualmente
$ pytest tests/modules/location/test_routes.py -v --tb=short
```

---

## 🎬 Cenário 10: Estatísticas do Projeto

### Ver estatísticas completas

```bash
$ python tools/validate_separation.py --all
```

**Output:**

```
============================================================
📊 RELATÓRIO FINAL
============================================================

✅ Estatísticas:
   • Modelos ORM: 42
   • Schemas Pydantic: 87
   • Módulos validados: 15
   • Módulos corretos: 15
   • Taxa de conformidade: 100%

🎉 Todos os módulos estão corretamente separados!
```

---

## 📊 Comparação: Antes vs Depois

### Estrutura de Arquivos

**Antes:**

```
backend/modules/location/
├── models.py          # 🔴 Misturado (ORM + Pydantic)
├── routes.py
└── __init__.py
```

**Depois:**

```
backend/modules/location/
├── models.py          # 🟢 Apenas ORM
├── schemas.py         # 🟢 Apenas Pydantic
├── routes.py
├── __init__.py
└── models.py.bak      # 💾 Backup
```

### Imports

**Antes:**

```python
# routes.py
from .models import CountryModel, ProvinceCreate  # 🔴 Misturado
```

**Depois:**

```python
# routes.py
from .models import CountryModel      # 🟢 ORM
from .schemas import ProvinceCreate   # 🟢 Pydantic
```

---

## 🎯 Comandos Mais Usados

```bash
# Migração completa de um módulo
python tools/migrate_module.py backend/modules/location

# Validar tudo
python tools/validate_separation.py --all

# Auditar e corrigir imports
python tools/audit_imports.py --fix

# Testar sistema
python tools/test_separation_system.py

# Migrar todos os módulos
python tools/migrate_all_modules.py --dry-run
python tools/migrate_all_modules.py
```

---

**Dica**: Sempre use `--dry-run` primeiro para ver o que vai acontecer!
