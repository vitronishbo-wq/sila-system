# Governance Module Expansion Progress

## Status: Em Progresso

Este documento rastreia o progresso da expansão do módulo Governance seguindo o padrão
completo do módulo Health.

## ✅ Concluído

### 1. Repository Completo

- ✅ Criado `repository.py` com todos os métodos CRUD para:
  - Institutions
  - Mandates
  - Decisions
  - Council Meetings
- ✅ Usa SQLAlchemy 2.x async patterns
- ✅ Segue o mesmo padrão do Health module

## 🚧 Em Progresso

### 2. Controller Completo

- ⏳ Criar `controller.py` com rotas tipadas
- ⏳ Implementar endpoints para Institutions
- ⏳ Implementar endpoints para Mandates
- ⏳ Implementar endpoints para Decisions
- ⏳ Implementar endpoints para Council Meetings
- ⏳ Adicionar validações e tratamento de erros
- ⏳ Documentação OpenAPI completa

### 3. Schemas Pydantic

- ⏳ Criar schemas API completos (api_schemas.py) seguindo padrão Health
- ⏳ Atualizar schemas existentes que estão como placeholders
- ⏳ Garantir validação completa de dados

### 4. Service Layer Refatoração

- ⏳ Refatorar `governance_service.py` para usar Repository
- ⏳ Remover acesso direto ao banco de dados do Service
- ⏳ Manter lógica de negócio no Service
- ⏳ Aplicar validações de ownership e regras de negócio

### 5. Models Update

- ⏳ Atualizar models para usar UUID (seguindo padrão Health)
- ⏳ Adicionar soft delete (deleted_at) em todos os models relevantes
- ⏳ Adicionar timestamps (created_at, updated_at) se não existirem

### 6. Seed Data

- ⏳ Criar `seed_data.py` com dados iniciais
- ⏳ Dados para Institutions
- ⏳ Dados para Mandates
- ⏳ Dados para Decisions
- ⏳ Dados para Council Meetings

### 7. Testes

- ⏳ Criar testes unitários para Repository
- ⏳ Criar testes unitários para Service
- ⏳ Criar testes de integração para Controller
- ⏳ Garantir cobertura adequada

## 📋 Próximos Passos

1. **Criar schemas API completos** - Seguir padrão do Health (`api_schemas.py`)
2. **Criar Controller completo** - Seguir padrão do Health (`controller.py`)
3. **Refatorar Service** - Usar Repository ao invés de acesso direto ao DB
4. **Atualizar Models** - Adicionar UUID e soft delete
5. **Criar Seed Data** - Dados iniciais para desenvolvimento
6. **Criar Testes** - Cobertura completa

## 🎯 Padrão de Referência

O módulo **Health** é o padrão de referência completo com:

- ✅ Models com UUID e soft delete
- ✅ Repository completo async
- ✅ Service layer usando Repository
- ✅ Controller completo com rotas tipadas
- ✅ Schemas Pydantic completos
- ✅ Seed data idempotente
- ✅ Testes unitários e integração

## 📝 Notas

- O Repository já foi criado e segue o padrão do Health
- Os schemas existentes são placeholders e precisam ser implementados
- O Service atual usa acesso direto ao DB e precisa ser refatorado
- Os models usam Integer ID e precisam ser atualizados para UUID
