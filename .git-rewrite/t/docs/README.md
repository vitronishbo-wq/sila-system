# 📚 DOCUMENTAÇÃO SILA - PLATAFORMA ÚNICA DIGITAL DO CIDADÃO

## 🎯 Visão Geral

Esta documentação contém todas as diretrizes, estratégias e instruções para a transição
da **Plataforma Única Digital do Cidadão (SILA)** da fase de desenvolvimento para o
lançamento com **900+ serviços**.

---

## 📋 Documentos Principais

### 1. 🚀 [Diretrizes de Transição para Lançamento](./DIRETRIZES_TRANSICAO_LANCAMENTO.md)

**Documento principal** com todas as diretrizes fundamentais para a transição:

- Gestão de credenciais de desenvolvimento
- Diretrizes arquitetônicas centralizadas
- Visibilidade e comunicação dos 900+ serviços
- Estratégia de segurança gradual
- Instruções para o agente de desenvolvimento

### 2. 🔒 [Estratégia de Segurança](./ESTRATEGIA_SEGURANCA_TRANSICAO.md)

**Estratégia detalhada** de transição de segurança:

- Princípio de segurança gradual
- Credenciais de desenvolvimento vs produção
- Checklist de transição de segurança
- Configurações de produção
- Processo de rollback

### 3. 🤖 [Instruções para o Agente](./INSTRUCOES_AGENTE_DESENVOLVIMENTO.md)

**Manual completo** para o agente de desenvolvimento:

- Princípios fundamentais
- Gestão de credenciais (regra de ouro)
- Arquitetura central
- Visibilidade dos 900+ serviços
- Comandos e procedimentos
- Troubleshooting

### 4. 📚 [Estrutura de Documentação](./DOCUMENTATION_STRUCTURE.md)

**Organização completa** da documentação do projeto:

- Estrutura de diretórios padronizada
- Categorias de documentação
- Processos de manutenção
- Padrões de formatação

### 5. 🔧 [Guia de Manutenção](./MAINTENANCE_GUIDE.md)

**Procedimentos operacionais** para sustentabilidade:

- Checklist de manutenção diária/semanal/mensal
- Processo de atualização de documentação
- Ferramentas de validação automática
- Troubleshooting de documentação

---

## 🔑 Credenciais de Desenvolvimento (Regra de Ouro)

| Credencial             | Valor    | Status        |
| :--------------------- | :------- | :------------ |
| **admin@sila.gov.ao**  | `adm123` | ✅ **MANTER** |
| **truman0@sila.co.ao** | `adm123` | ✅ **MANTER** |
| **Marcelo Truman**     | Usuário  | ✅ **MANTER** |
| **926878449**          | Telefone | ✅ **MANTER** |

> **⚠️ IMPORTANTE**: Manter estas credenciais até o Sprint de Pré-Produção

---

## 🆕 Documentação Phase 3 - Concluída ✅

### 📋 O que foi implementado:

#### 🏗️ **Estrutura Padronizada**

- **`DOCUMENTATION_STRUCTURE.md`** - Organização hierárquica da documentação
- **`DOCUMENTATION_TEMPLATE.md`** - Template padrão para nova documentação
- **`MAINTENANCE_GUIDE.md`** - Procedimentos de manutenção contínua

#### 🔧 **Processos Sustentáveis**

- Checklist de manutenção diária/semanal/mensal
- Ferramentas de validação automática
- Métricas de qualidade documental
- Troubleshooting especializado

#### 📊 **Sistema de Qualidade**

- Indicadores de completude, atualidade e verificabilidade
- Dashboard de saúde da documentação
- Processo de revisão e aprovação
- Versionamento e histórico

### 🎯 **Benefícios da Phase 3:**

- ✅ **Onboarding acelerado** para novos desenvolvedores
- ✅ **Manutenção simplificada** com processos padronizados
- ✅ **Qualidade consistente** através de templates
- ✅ **Sustentabilidade a longo prazo** com métricas
- ✅ **Transparência total** com histórico de versões

---

## 🏗️ Arquitetura Central

### Princípio Fundamental

> **"A distinção entre o Portal do Cidadão e a Interface Administrativa é feita **apenas
> no Frontend (UI/UX)** e por meio de **regras de permissão (Roles/Scopes)** no Backend.
> Não crie APIs separadas. O Backend deve sempre servir a mesma API (`/api/v1/`)."**

### Estrutura

```
/opt/sila-system/
├── backend/                 # API única para todos os clientes
├── frontend/
│   ├── webapp/             # Portal do Cidadão (Público)
│   └── admin/              # Interface Administrativa (Interno)
├── setup_admin.sql         # Credenciais de desenvolvimento
└── docs/                   # Esta documentação
```

---

## 👁️ Visibilidade dos 900+ Serviços

### Implementação no Frontend

- ✅ **DashboardPage**: Métricas principais dos 900+ serviços
- ✅ **ServicesPage**: Centro de serviços com referência aos 900+
- ✅ **ServiceMetrics**: Componente reutilizável com métricas

### Referência Estética

> **"900+ Serviços Digitais Ativos. A sua administração na palma da mão."**

---

## 🔒 Estratégia de Segurança

### Fase de Desenvolvimento (Atual)

- **Senhas**: Baixa complexidade (`adm123`)
- **Variáveis**: Acesso livre ao `.env`
- **Autenticação**: Fallback hardcoded
- **Logs**: Detalhados para debug

### Fase de Produção (Futuro)

- **Senhas**: Alta complexidade, rotação automática
- **Variáveis**: Secrets manager (HashiCorp Vault/AWS)
- **Autenticação**: 2FA, rate limiting
- **Logs**: Auditoria completa

---

## 📞 Contatos

| Função                      | Nome           | Email              | Telefone  |
| :-------------------------- | :------------- | :----------------- | :-------- |
| **Desenvolvedor Principal** | Marcelo Truman | truman0@sila.co.ao | 926878449 |
| **Administrador Sistema**   | Admin SILA     | admin@sila.gov.ao  | -         |

---

## 🚀 Comandos Essenciais

### Setup Inicial

```bash
# Credenciais
psql -d sila_db -f setup_admin.sql

# Backend
cd /opt/sila-system/backend
python -m uvicorn app.main:app --reload --port 8000

# Frontend
cd /opt/sila-system/frontend/apps/web
npm run dev
```

### Teste de Autenticação

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@sila.gov.ao", "password": "adm123"}'
```

---

## 📊 Status do Projeto

### ✅ Concluído

- [x] Base arquitetônica sólida (Fases 1-4)
- [x] Gestão de credenciais de desenvolvimento
- [x] Diretrizes arquitetônicas centralizadas
- [x] Referência estética aos 900+ serviços
- [x] Estratégia de transição de segurança
- [x] Instruções completas para o agente
- [x] **Phase 3 - Documentação Sustentável** ✅

### 🔄 Em Andamento

- [ ] Padronização de desenvolvimento
- [ ] Implementação em massa de serviços
- [ ] Preparação para sprint de segurança

### 📋 Próximos Passos

- [ ] Sprint de pré-produção
- [ ] Implementação de segurança robusta
- [ ] Lançamento dos 900+ serviços

---

## 🎯 Objetivo Final

> **Preparar a plataforma para o lançamento dos 900+ serviços mantendo a velocidade de
> desenvolvimento e garantindo uma transição suave para produção quando necessário.**

---

_Esta documentação deve ser consultada diariamente e atualizada conforme a evolução do
projeto._
