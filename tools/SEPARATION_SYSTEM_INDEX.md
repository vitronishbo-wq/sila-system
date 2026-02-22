# 🧠 Sistema de Separação Models/Schemas - Índice Completo

## 📚 Arquivos do Sistema

### 🔧 Ferramentas Principais

| Arquivo                     | Descrição                              | Uso                                                             |
| --------------------------- | -------------------------------------- | --------------------------------------------------------------- |
| **split_models_schemas.py** | Separador automático de models/schemas | `python tools/split_models_schemas.py backend/modules/location` |
| **audit_imports.py**        | Auditor e corretor de importações      | `python tools/audit_imports.py --fix`                           |
| **validate_separation.py**  | Validador de separação correta         | `python tools/validate_separation.py --all`                     |
| **migrate_module.py**       | Orquestrador completo (recomendado)    | `python tools/migrate_module.py backend/modules/location`       |
| **migrate_all_modules.py**  | Migração em lote de todos os módulos   | `python tools/migrate_all_modules.py --dry-run`                 |

### 📖 Documentação

| Arquivo                        | Conteúdo                         |
| ------------------------------ | -------------------------------- |
| **README_SEPARATION.md**       | Documentação completa do sistema |
| **QUICKSTART_SEPARATION.md**   | Guia rápido de uso               |
| **SEPARATION_SYSTEM_INDEX.md** | Este arquivo - índice completo   |

---

## 🎯 Fluxos de Trabalho

### 🚀 Fluxo Recomendado (Um Módulo)

```bash
# Comando único que faz tudo
python tools/migrate_module.py backend/modules/location
```

**Executa automaticamente:**

1. Validação inicial
2. Separação models/schemas
3. Auditoria de imports
4. Validação final
5. Sugestões de testes

---

### 🌍 Fluxo para Todos os Módulos

```bash
# 1. Simular (OBRIGATÓRIO)
python tools/migrate_all_modules.py --dry-run

# 2. Executar
python tools/migrate_all_modules.py

# 3. Validar
python tools/validate_separation.py --all

# 4. Testar
pytest tests/
```

---

### 🔧 Fluxo Manual (Passo a Passo)

```bash
# 1. Separar
python tools/split_models_schemas.py backend/modules/location

# 2. Auditar
python tools/audit_imports.py --module location --fix

# 3. Validar
python tools/validate_separation.py backend/modules/location

# 4. Testar
pytest tests/modules/location/
```

---

## 📊 Funcionalidades por Ferramenta

### split_models_schemas.py

- ✅ Identifica classes Pydantic (herdam de BaseModel)
- ✅ Extrai para schemas.py com imports corretos
- ✅ Remove do models.py
- ✅ Cria backups automáticos
- ✅ Detecta imports necessários (Optional, List, Field, etc.)
- ✅ Modo dry-run para simulação

**Flags:**

- `--dry-run` - Simula sem modificar

---

### audit_imports.py

- ✅ Escaneia todos os schemas disponíveis
- ✅ Detecta imports incorretos de models.py
- ✅ Corrige automaticamente para schemas.py
- ✅ Cria backups antes de modificar
- ✅ Relatório detalhado de problemas

**Flags:**

- `--fix` - Corrige automaticamente
- `--module <nome>` - Audita módulo específico
- `--root <path>` - Define diretório raiz

---

### validate_separation.py

- ✅ Verifica que models.py tem apenas SQLAlchemy
- ✅ Verifica que schemas.py tem apenas Pydantic
- ✅ Detecta classes Pydantic em models.py
- ✅ Detecta imports incorretos
- ✅ Estatísticas de classes ORM e Pydantic
- ✅ Relatório detalhado de erros e avisos

**Flags:**

- `--all` - Valida todos os módulos

---

### migrate_module.py

- ✅ Orquestra todo o processo
- ✅ Validação inicial
- ✅ Separação automática
- ✅ Auditoria de imports
- ✅ Validação final
- ✅ Sugestões de testes
- ✅ Resumo completo

**Flags:**

- `--skip-tests` - Pula sugestões de testes

---

### migrate_all_modules.py

- ✅ Descobre todos os módulos automaticamente
- ✅ Migra em lote
- ✅ Permite exclusão de módulos
- ✅ Confirmação antes de executar
- ✅ Relatório consolidado
- ✅ Modo dry-run

**Flags:**

- `--dry-run` - Simula sem modificar
- `--exclude <lista>` - Exclui módulos (separados por vírgula)

---

## 🎓 Exemplos de Uso

### Exemplo 1: Primeiro Uso

```bash
# Entender o que vai acontecer
python tools/split_models_schemas.py backend/modules/location --dry-run

# Executar
python tools/migrate_module.py backend/modules/location

# Testar
pytest tests/modules/location/ -v
```

### Exemplo 2: Migração em Massa

```bash
# Simular tudo
python tools/migrate_all_modules.py --dry-run

# Executar (excluindo módulos legados)
python tools/migrate_all_modules.py --exclude legacy,deprecated

# Validar resultado
python tools/validate_separation.py --all
```

### Exemplo 3: Correção de Imports

```bash
# Apenas auditar
python tools/audit_imports.py

# Auditar e corrigir
python tools/audit_imports.py --fix

# Auditar módulo específico
python tools/audit_imports.py --module payment --fix
```

### Exemplo 4: Validação Contínua

```bash
# Validar um módulo
python tools/validate_separation.py backend/modules/location

# Validar todos
python tools/validate_separation.py --all

# Integrar no CI/CD
python tools/validate_separation.py --all || exit 1
```

---

## 🔍 Detecção de Problemas

### O que cada ferramenta detecta:

**split_models_schemas.py:**

- Classes que herdam de BaseModel
- Imports de pydantic necessários
- Docstrings e métodos internos

**audit_imports.py:**

- `from .models import SchemaName` ❌
- `from backend.modules.X.models import SchemaName` ❌
- Múltiplos imports na mesma linha

**validate_separation.py:**

- Classes Pydantic em models.py
- Classes ORM em schemas.py
- Imports de pydantic em models.py
- Imports de sqlalchemy em schemas.py
- Arquivos faltando

---

## 🛡️ Segurança e Backups

Todas as ferramentas criam backups automáticos:

- `models.py.bak` - Backup do models.py original
- `schemas.py.bak` - Backup do schemas.py (se existir)
- Arquivos modificados têm backup com timestamp

**Restaurar backup:**

```bash
# Se algo der errado
cp backend/modules/location/models.py.bak backend/modules/location/models.py
```

---

## 📈 Métricas e Estatísticas

### Módulo Location (Exemplo)

```
✅ Estatísticas:
   • Modelos ORM: 6
   • Schemas Pydantic: 14
   • Arquivos: models.py, schemas.py
   • Status: ✅ Separação correta
```

### Projeto Completo

```bash
# Ver estatísticas de todos os módulos
python tools/validate_separation.py --all
```

---

## 🚨 Troubleshooting

### Problema: "Python não encontrado"

```bash
# Use python3
python3 tools/migrate_module.py backend/modules/location

# Ou especifique o caminho completo
/usr/bin/python3 tools/migrate_module.py backend/modules/location
```

### Problema: "Módulo não encontrado"

```bash
# Verifique o caminho (deve ser relativo ao root)
ls -la backend/modules/location/

# Caminho correto
python tools/migrate_module.py backend/modules/location
```

### Problema: "Nenhum schema encontrado"

```bash
# O módulo já está limpo
# Verifique manualmente
grep -n "BaseModel" backend/modules/location/models.py
```

### Problema: Imports quebrados após migração

```bash
# Execute o auditor
python tools/audit_imports.py --fix

# Verifique manualmente
grep -r "from.*models import.*Create" backend/
```

### Problema: Testes falhando

```bash
# Atualize imports nos testes
grep -r "from.*models import" tests/modules/location/

# Execute testes com verbose
pytest tests/modules/location/ -v --tb=short
```

---

## 🔗 Integração CI/CD

### GitHub Actions / GitLab CI

```yaml
- name: Validate Models/Schemas Separation
  run: |
    python tools/validate_separation.py --all
    if [ $? -ne 0 ]; then
      echo "❌ Models/Schemas separation validation failed"
      exit 1
    fi
```

### Pre-commit Hook

```bash
# .husky/pre-commit
python tools/validate_separation.py --all || {
  echo "❌ Validação falhou. Execute: python tools/migrate_module.py <module>"
  exit 1
}
```

---

## 📚 Referências

- **ADR-0002**: ORM Migration SQLAlchemy to Prisma
- **Pydantic Docs**: https://docs.pydantic.dev/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/

---

## 🎯 Roadmap

### ✅ Implementado

- [x] Separador automático
- [x] Auditor de imports
- [x] Validador de separação
- [x] Orquestrador de módulo
- [x] Migração em lote
- [x] Documentação completa

### 🔮 Futuro

- [ ] Integração com IDE (VSCode extension)
- [ ] Auto-fix em tempo real
- [ ] Métricas de qualidade
- [ ] Dashboard de status
- [ ] Suporte para outros ORMs

---

**Criado**: 2025-01-04 **Versão**: 1.0.0 **Autor**: Sistema de Automação SILA
**Licença**: MIT
