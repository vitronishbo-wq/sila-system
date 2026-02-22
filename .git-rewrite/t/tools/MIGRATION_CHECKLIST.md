# ✅ Checklist de Migração Models/Schemas

Use este checklist para garantir que a migração de cada módulo seja feita corretamente.

---

## 📋 Checklist por Módulo

### Módulo: **\*\***\_\_\_\_**\*\***

#### Pré-Migração

- [ ] Verificar se módulo tem `models.py`
- [ ] Verificar se há schemas Pydantic misturados
- [ ] Criar branch: `git checkout -b refactor/separate-<module>-models-schemas`
- [ ] Fazer backup manual (opcional):
      `cp -r backend/modules/<module> /tmp/backup-<module>`

#### Migração

- [ ] Executar: `python tools/migrate_module.py backend/modules/<module>`
- [ ] Verificar output sem erros
- [ ] Confirmar que backups foram criados (`.py.bak`)

#### Validação

- [ ] Executar: `python tools/validate_separation.py backend/modules/<module>`
- [ ] Confirmar: "✅ Separação correta!"
- [ ] Verificar estatísticas de classes

#### Revisão Manual

- [ ] Revisar `models.py` - apenas SQLAlchemy
- [ ] Revisar `schemas.py` - apenas Pydantic
- [ ] Verificar imports em `__init__.py`
- [ ] Verificar imports em `routes.py` ou `endpoints.py`

#### Testes

- [ ] Executar: `pytest tests/modules/<module>/ -v`
- [ ] Todos os testes passando
- [ ] Sem warnings de imports

#### Git

- [ ] Revisar mudanças: `git diff backend/modules/<module>/`
- [ ] Adicionar: `git add backend/modules/<module>/`
- [ ] Commit: `git commit -m "refactor(<module>): separate models and schemas"`
- [ ] Push: `git push origin refactor/separate-<module>-models-schemas`

#### Pós-Migração

- [ ] Criar Pull Request
- [ ] Code review
- [ ] Merge para main/develop
- [ ] Deletar branch local: `git branch -d refactor/separate-<module>-models-schemas`

---

## 📊 Progresso Geral

### Módulos Migrados

- [x] location ✅
- [ ] payment
- [ ] journeys
- [ ] billing
- [ ] training
- [ ] _adicione outros módulos aqui_

### Estatísticas

- **Total de módulos**: \_\_\_
- **Migrados**: \_\_\_
- **Pendentes**: \_\_\_
- **Progresso**: \_\_\_%

---

## 🚨 Problemas Comuns e Soluções

### Problema: Testes falhando

**Solução:**

```bash
python tools/audit_imports.py --module <module> --fix
pytest tests/modules/<module>/ -v --tb=short
```

### Problema: Imports quebrados

**Solução:**

```bash
# Verificar imports incorretos
grep -r "from.*models import.*Create" backend/modules/<module>/
grep -r "from.*models import.*Response" backend/modules/<module>/

# Corrigir
python tools/audit_imports.py --module <module> --fix
```

### Problema: Validação falhou

**Solução:**

```bash
# Ver detalhes
python tools/validate_separation.py backend/modules/<module>

# Re-executar migração se necessário
python tools/migrate_module.py backend/modules/<module>
```

### Problema: Rollback necessário

**Solução:**

```bash
# Restaurar do backup
cp backend/modules/<module>/models.py.bak backend/modules/<module>/models.py
cp backend/modules/<module>/schemas.py.bak backend/modules/<module>/schemas.py

# Ou reverter commit
git reset --hard HEAD~1
```

---

## 🎯 Comandos Rápidos

```bash
# Migração completa
python tools/migrate_module.py backend/modules/<module>

# Validar
python tools/validate_separation.py backend/modules/<module>

# Testar
pytest tests/modules/<module>/ -v

# Commit
git add backend/modules/<module>/
git commit -m "refactor(<module>): separate models and schemas"
```

---

## 📅 Planejamento

### Sprint 1

- [ ] Módulo 1: \***\*\_\_\_\*\***
- [ ] Módulo 2: \***\*\_\_\_\*\***
- [ ] Módulo 3: \***\*\_\_\_\*\***

### Sprint 2

- [ ] Módulo 4: \***\*\_\_\_\*\***
- [ ] Módulo 5: \***\*\_\_\_\*\***
- [ ] Módulo 6: \***\*\_\_\_\*\***

### Sprint 3

- [ ] Validação completa
- [ ] Documentação atualizada
- [ ] Deploy em staging

---

## 🏆 Critérios de Sucesso

Um módulo está completamente migrado quando:

- ✅ `models.py` contém apenas classes SQLAlchemy
- ✅ `schemas.py` contém apenas classes Pydantic
- ✅ Validador retorna "Separação correta"
- ✅ Todos os testes passando
- ✅ Imports corretos em todos os arquivos
- ✅ Code review aprovado
- ✅ Merged para branch principal

---

## 📝 Notas

_Use este espaço para anotações específicas do projeto:_

```
Data: ___________
Responsável: ___________

Observações:
-
-
-

Problemas encontrados:
-
-

Lições aprendidas:
-
-
```

---

**Dica**: Imprima este checklist ou mantenha aberto em um editor para acompanhar o
progresso!
