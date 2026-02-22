# 🤖 INSTRUÇÕES COMPLETAS PARA O AGENTE DE DESENVOLVIMENTO

## 📋 Visão Geral

Este documento contém todas as instruções essenciais para o agente de desenvolvimento da
**Plataforma Única Digital do Cidadão (SILA)**, garantindo continuidade, consistência e
preparação adequada para o lançamento dos **900+ serviços**.

---

## 1. 🎯 PRINCÍPIOS FUNDAMENTAIS

### 1.1 Filosofia de Desenvolvimento

> **"A distinção entre o Portal do Cidadão e a Interface Administrativa é feita **apenas
> no Frontend (UI/UX)** e por meio de **regras de permissão (Roles/Scopes)** no Backend.
> Não crie APIs separadas. O Backend deve sempre servir a mesma API (`/api/v1/`), e a
> segurança fará o controle de acesso necessário."**

### 1.2 Regras de Ouro

1. **Backend Único**: Nunca criar APIs separadas para diferentes clientes
2. **Segurança Gradual**: Manter simplicidade em desenvolvimento, complexidade em
   produção
3. **Visibilidade dos Serviços**: Sempre referenciar os 900+ serviços no frontend
4. **Credenciais Padrão**: Manter `adm123` até o sprint de pré-produção
5. **Arquitetura Consistente**: Seguir padrões estabelecidos nas Fases 1-4

---

## 2. 🔐 GESTÃO DE CREDENCIAIS (REGRA DE OURO)

### 2.1 Credenciais Padrão - MANTER

| Credencial             | Valor    | Status        | Ação Requerida                                      |
| :--------------------- | :------- | :------------ | :-------------------------------------------------- |
| **admin@sila.gov.ao**  | `adm123` | ✅ **MANTER** | Deve existir no banco, criado via `setup_admin.sql` |
| **truman0@sila.co.ao** | `adm123` | ✅ **MANTER** | Deve existir no banco, criado via `setup_admin.sql` |
| **Marcelo Truman**     | Usuário  | ✅ **MANTER** | Associado ao `truman0@sila.co.ao`                   |
| **926878449**          | Telefone | ✅ **MANTER** | Essencial para testes de módulos                    |

### 2.2 Instrução Específica

> **"Para fins de desenvolvimento e testes de integração, mantenha as credenciais
> `admin@sila.gov.ao` e `truman0@sila.co.ao` ativas e com a senha de baixa complexidade
> (`adm123`), conforme o padrão `setup_admin.sql`. A segurança será tratada como um
> _sprint_ dedicado antes da produção."**

### 2.3 Comandos Essenciais

```bash
# Setup inicial de credenciais
psql -d sila_db -f setup_admin.sql

# Verificar credenciais
psql -d sila_db -c "SELECT email, full_name FROM users WHERE is_superuser = true;"

# Testar autenticação
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@sila.gov.ao", "password": "adm123"}'
```

---

## 3. 🏗️ ARQUITETURA CENTRAL

### 3.1 Estrutura de Desenvolvimento

```
/opt/sila-system/
├── backend/                 # API única para todos os clientes
│   ├── app/
│   │   ├── core/security.py # Controle de acesso baseado em roles
│   │   └── api/v1/         # Endpoints unificados
├── frontend/
│   ├── webapp/             # Portal do Cidadão (Público)
│   └── admin/              # Interface Administrativa (Interno)
├── setup_admin.sql         # Credenciais de desenvolvimento
└── docs/                   # Documentação e diretrizes
```

### 3.2 Controle de Acesso

```python
# Exemplo de controle de acesso baseado em roles
@require_permissions(["admin", "operador"])
async def admin_endpoint():
    # Acesso restrito a administradores e operadores
    pass

@require_permissions(["cidadão"])
async def citizen_endpoint():
    # Acesso público para cidadãos
    pass
```

### 3.3 Instrução Arquitetônica

> **"A distinção entre o Portal do Cidadão e a Interface Administrativa é feita **apenas
> no Frontend (UI/UX)** e por meio de **regras de permissão (Roles/Scopes)** no Backend
> (`app/core/security.py`). Não crie APIs separadas. O Backend deve sempre servir a
> mesma API (`/api/v1/`), e a segurança fará o controle de acesso necessário."**

---

## 4. 👁️ VISIBILIDADE DOS 900+ SERVIÇOS

### 4.1 Implementação no Frontend

> **"No Frontend (Portal do Cidadão), implemente uma referência estética e informativa
> aos **'900+ Serviços'** no componente principal (`ServiceHubPage` ou `Dashboard`).
> Isso reforça a visão de uma plataforma única e completa, seguindo a sobriedade
> estética de um portal governamental."**

### 4.2 Componente ServiceMetrics

```typescript
// Componente já implementado em /frontend/apps/web/src/components/ServiceMetrics.tsx
const ServiceMetrics = () => {
  return (
    <div className="service-metrics">
      <h2>900+ Serviços Digitais Ativos</h2>
      <p>A sua administração na palma da mão</p>
      <div className="metrics-grid">
        <MetricCard title="Serviços Disponíveis" value="900+" />
        <MetricCard title="Cidadãos Atendidos" value="1M+" />
        <MetricCard title="Tempo Médio de Resposta" value="< 2min" />
      </div>
    </div>
  );
};
```

### 4.3 Locais de Implementação

- ✅ **DashboardPage**: Métricas principais dos 900+ serviços
- ✅ **ServicesPage**: Centro de serviços com referência aos 900+
- 🔄 **Landing Page**: Página inicial com destaque
- 🔄 **ServiceHubPage**: Hub central de serviços

---

## 5. 🔒 ESTRATÉGIA DE SEGURANÇA

### 5.1 Fase de Desenvolvimento (Atual)

| Aspecto                 | Configuração                  | Justificativa                    |
| :---------------------- | :---------------------------- | :------------------------------- |
| **Senhas**              | `adm123` (baixa complexidade) | Velocidade de desenvolvimento    |
| **Variáveis Sensíveis** | Acesso livre ao `.env`        | Facilidade de configuração       |
| **Autenticação**        | Fallback hardcoded            | Desenvolvimento sem dependências |
| **Logs**                | Logs detalhados para debug    | Facilita troubleshooting         |

### 5.2 Instrução de Segurança

> **"Mantenha a liberdade total com senhas de baixa complexidade e acesso ao `.env` de
> desenvolvimento **até o início do Sprint de Pré-Produção**. Naquele momento, todas as
> senhas de superusuário deverão ser **resetadas** para um padrão de alta segurança, e
> as variáveis sensíveis do `.env` deverão ser migradas para o ambiente de _secrets_."**

### 5.3 Checklist de Transição (Futuro)

- [ ] Resetar senhas para alta complexidade
- [ ] Migrar variáveis para secrets manager
- [ ] Implementar 2FA
- [ ] Configurar logs de auditoria
- [ ] Implementar rate limiting
- [ ] Configurar HTTPS obrigatório

---

## 6. 📚 COMANDOS E PROCEDIMENTOS

### 6.1 Comandos de Desenvolvimento

```bash
# Iniciar backend
cd /opt/sila-system/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Iniciar frontend
cd /opt/sila-system/frontend/apps/web
npm run dev

# Executar testes
cd /opt/sila-system/backend
python -m pytest tests/

# Verificar logs
tail -f /opt/sila-system/backend/backend.log
```

### 6.2 Comandos de Banco de Dados

```bash
# Conectar ao banco
psql -d sila_db -U postgres

# Executar setup de credenciais
psql -d sila_db -f setup_admin.sql

# Backup do banco
pg_dump sila_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql -d sila_db < backup_YYYYMMDD_HHMMSS.sql
```

### 6.3 Comandos de Validação

```bash
# Validar autenticação
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@sila.gov.ao", "password": "adm123"}'

# Verificar saúde da API
curl http://localhost:8000/api/v1/health

# Testar endpoints
curl http://localhost:8000/api/v1/services
```

---

## 7. 🚀 ROADMAP PARA 900+ SERVIÇOS

### 7.1 Fases de Implementação

1. **✅ Fase Atual**: Base arquitetônica sólida
2. **🔄 Próxima**: Padronização de desenvolvimento
3. **📋 Seguinte**: Implementação em massa de serviços
4. **🎯 Final**: Sprint de segurança e lançamento

### 7.2 Métricas de Sucesso

- **Desenvolvimento**: Velocidade de implementação mantida
- **Qualidade**: Zero regressões na base arquitetônica
- **Segurança**: Transição suave para produção
- **Usabilidade**: Interface clara e informativa sobre os 900+ serviços

---

## 8. 📞 CONTATOS E SUPORTE

### 8.1 Contatos Principais

| Função                      | Nome           | Email              | Telefone  |
| :-------------------------- | :------------- | :----------------- | :-------- |
| **Desenvolvedor Principal** | Marcelo Truman | truman0@sila.co.ao | 926878449 |
| **Administrador Sistema**   | Admin SILA     | admin@sila.gov.ao  | -         |

### 8.2 Recursos de Ajuda

- **Documentação**: `/opt/sila-system/docs/`
- **Logs**: `/opt/sila-system/backend/backend.log`
- **Configuração**: `/opt/sila-system/.env`
- **Setup**: `/opt/sila-system/setup_admin.sql`

---

## 9. 🔧 TROUBLESHOOTING

### 9.1 Problemas Comuns

#### Problema: Erro de autenticação

```bash
# Solução: Verificar credenciais
psql -d sila_db -c "SELECT email FROM users WHERE is_superuser = true;"
# Deve retornar: admin@sila.gov.ao, truman0@sila.co.ao
```

#### Problema: Frontend não conecta ao backend

```bash
# Solução: Verificar proxy do Vite
cat /opt/sila-system/frontend/apps/web/vite.config.ts
# Deve ter proxy para http://localhost:8000
```

#### Problema: Banco de dados não conecta

```bash
# Solução: Verificar variáveis de ambiente
cat /opt/sila-system/.env
# Deve ter POSTGRES_* configurado
```

### 9.2 Logs de Debug

```bash
# Backend logs
tail -f /opt/sila-system/backend/backend.log

# Frontend logs (browser console)
# Abrir DevTools (F12) e verificar Console

# Database logs
tail -f /var/log/postgresql/postgresql-*.log
```

---

## 10. 📋 CHECKLIST DIÁRIO

### 10.1 Início do Dia

- [ ] Verificar se backend está rodando (porta 8000)
- [ ] Verificar se frontend está rodando (porta 3000/5173)
- [ ] Testar login com credenciais padrão
- [ ] Verificar logs de erro
- [ ] Confirmar conectividade com banco

### 10.2 Durante o Desenvolvimento

- [ ] Seguir padrões arquitetônicos estabelecidos
- [ ] Manter credenciais de desenvolvimento
- [ ] Referenciar 900+ serviços no frontend
- [ ] Usar API única (`/api/v1/`)
- [ ] Implementar controle de acesso por roles

### 10.3 Final do Dia

- [ ] Fazer commit das alterações
- [ ] Documentar mudanças significativas
- [ ] Verificar se não quebrou funcionalidades existentes
- [ ] Preparar para próximo dia de desenvolvimento

---

## 11. 📖 DOCUMENTAÇÃO RELACIONADA

- [Diretrizes de Transição para Lançamento](./DIRETRIZES_TRANSICAO_LANCAMENTO.md)
- [Estratégia de Segurança](./ESTRATEGIA_SEGURANCA_TRANSICAO.md)
- [Arquitetura do Sistema](./ARQUITETURA_SISTEMA.md)
- [API Documentation](./API_DOCUMENTATION.md)

---

## 12. 🎯 RESUMO EXECUTIVO

### 12.1 Instruções Críticas

1. **MANTER** credenciais `admin@sila.gov.ao` e `truman0@sila.co.ao` com senha `adm123`
2. **NUNCA** criar APIs separadas - usar sempre `/api/v1/`
3. **SEMPRE** referenciar os 900+ serviços no frontend
4. **SEGUIR** padrões arquitetônicos das Fases 1-4
5. **AGUARDAR** sprint de pré-produção para implementar segurança robusta

### 12.2 Objetivo Final

> **Preparar a plataforma para o lançamento dos 900+ serviços mantendo a velocidade de
> desenvolvimento e garantindo uma transição suave para produção quando necessário.**

---

_Este documento deve ser consultado diariamente e atualizado conforme a evolução do
projeto._
