# 🧠 Sistema de Separação Models/Schemas SILA

Sistema automatizado para separar modelos ORM (SQLAlchemy) de schemas Pydantic em
qualquer módulo do SILA.

## 📋 Ferramentas Disponíveis

### 1. 🔧 `split_models_schemas.py` - Separador Automático

Extrai schemas Pydantic de `models.py` e os move para `schemas.py`.

**Uso:**

```bash
# Dry-run (simula sem modificar)
python tools/split_models_schemas.py backend/modules/location --dry-run

# Execução real
python tools/split_models_schemas.py backend/modules/location

# Outro módulo
python tools/split_models_schemas.py backend/modules/payment
```

**O que faz:**

- ✅ Identifica todas as classes que herdam de `BaseModel`
- ✅ Extrai para `schemas.py` com imports corretos
- ✅ Remove do `models.py`
- ✅ Cria backups automáticos (`.py.bak`)
- ✅ Detecta imports necessários (Optional, List, Field, etc.)

---

### 2. 🔍 `audit_imports.py` - Auditor de Importações

Detecta e corrige importações incorretas de schemas a partir de `models.py`.

**Uso:**

```bash
# Auditar todo o projeto
python tools/audit_imports.py

# Auditar módulo específico
python tools/audit_imports.py --module location

# Corrigir automaticamente
python tools/audit_imports.py --fix

# Corrigir módulo específico
python tools/audit_imports.py --module payment --fix
```

**O que detecta:**

```python
# ❌ ERRADO
from backend.modules.location.models import ProvinceCreate

# ✅ CORRETO
from backend.modules.location.schemas import ProvinceCreate
```

---

### 3. ✅ `validate_separation.py` - Validador

Valida que a separação está correta e gera relatório.

**Uso:**

```bash
# Validar um módulo
python tools/validate_separation.py backend/modules/location

# Validar todos os módulos
python tools/validate_separation.py --all
```

**Verificações:**

- ✅ `models.py` contém apenas SQLAlchemy
- ✅ `schemas.py` contém apenas Pydantic
- ✅ Não há classes Pydantic em `models.py`
- ✅ Não há imports de pydantic em `models.py`
- ✅ Estatísticas de classes ORM e Pydantic

---

## 🚀 Fluxo de Trabalho Recomendado

### Para um módulo específico:

```bash
# 1. Simular separação (ver o que vai acontecer)
python tools/split_models_schemas.py backend/modules/location --dry-run

# 2. Executar separação
python tools/split_models_schemas.py backend/modules/location

# 3. Auditar e corrigir imports
python tools/audit_imports.py --module location --fix

# 4. Validar resultado
python tools/validate_separation.py backend/modules/location

# 5. Testar o módulo
pytest tests/modules/location/
```

### Para todo o projeto:

```bash
# 1. Separar todos os módulos (um por vez)
for module in backend/modules/*/; do
    python tools/split_models_schemas.py "$module"
done

# 2. Auditar e corrigir todos os imports
python tools/audit_imports.py --fix

# 3. Validar tudo
python tools/validate_separation.py --all

# 4. Executar testes completos
pytest
```

---

## 📊 Exemplo de Saída

### Split (Separação)

```
🔍 Analisando módulo: backend/modules/location

📦 Encontrados 2 schemas Pydantic:
   • ProvinceCreate
   • ProvinceResponse

💾 Backup criado: backend/modules/location/models.py.bak
✅ Schemas extraídos para: backend/modules/location/schemas.py
✅ Models limpo: backend/modules/location/models.py

✨ Separação concluída com sucesso!
```

### Audit (Auditoria)

```
🔍 Auditando importações em: backend

📦 location: 15 schemas
📦 payment: 8 schemas

⚠️  Encontrados 3 problemas em 2 arquivos:

📄 backend/modules/location/routes.py
   Linha 5: from .models import ProvinceCreate
   → Deveria ser: from .schemas import ProvinceCreate

🔧 Aplicando correções...
   ✅ backend/modules/location/routes.py

✨ 2 arquivos corrigidos!
```

### Validate (Validação)

```
🔍 SILA Separation Validator
============================================================

📦 Validando módulo: location
   ✅ Separação correta!
   📊 6 modelos ORM
   📊 15 schemas Pydantic

============================================================
📊 RELATÓRIO FINAL
============================================================

✅ Estatísticas:
   • Modelos ORM: 6
   • Schemas Pydantic: 15

🎉 Todos os módulos estão corretamente separados!
```

---

## 🛡️ Segurança

- **Backups automáticos**: Todos os arquivos modificados têm backup `.py.bak`
- **Dry-run**: Sempre teste com `--dry-run` primeiro
- **Validação**: Execute o validador após mudanças
- **Testes**: Execute testes do módulo após separação

---

## 🧩 Estrutura Esperada

### Antes (❌ Misturado)

```python
# models.py
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class UserModel(Base):  # ORM
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

class UserCreate(BaseModel):  # Pydantic ❌
    name: str
```

### Depois (✅ Separado)

```python
# models.py
from sqlalchemy import Column, Integer, String

class UserModel(Base):  # ORM apenas
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
```

```python
# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):  # Pydantic apenas
    name: str
```

---

## 🐛 Troubleshooting

### Erro: "Nenhum schema encontrado"

- O arquivo já está limpo ou não tem classes Pydantic
- Verifique se as classes herdam de `BaseModel`

### Erro: "Módulo não encontrado"

- Verifique o caminho: deve ser relativo ao root do projeto
- Exemplo correto: `backend/modules/location`

### Imports quebrados após separação

- Execute: `python tools/audit_imports.py --fix`
- Verifique manualmente arquivos `__init__.py`

### Testes falhando

- Atualize imports nos testes
- Verifique se `conftest.py` importa corretamente

---

## 📝 Checklist de Migração

Para cada módulo:

- [ ] Executar `split_models_schemas.py`
- [ ] Executar `audit_imports.py --fix`
- [ ] Executar `validate_separation.py`
- [ ] Atualizar `__init__.py` se necessário
- [ ] Executar testes do módulo
- [ ] Commit das mudanças
- [ ] Code review

---

## 🎯 Benefícios

1. **Separação de responsabilidades**: ORM vs Validação
2. **Imports mais claros**: `from .models` vs `from .schemas`
3. **Manutenibilidade**: Arquivos focados e organizados
4. **Performance**: Imports mais leves
5. **Padrão consistente**: Todos os módulos seguem a mesma estrutura

---

## 📚 Referências

- [ADR-0002: ORM Migration SQLAlchemy to Prisma](../docs/adr/0002-orm-migration-sqlalchemy-to-prisma.md)
- [Pydantic Best Practices](https://docs.pydantic.dev/latest/concepts/models/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)

---

**Criado por**: Sistema de Automação SILA **Última atualização**: 2025-01-04
