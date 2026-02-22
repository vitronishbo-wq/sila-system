# 🎯 DIRETRIZES DE TRANSIÇÃO: DESENVOLVIMENTO PARA LANÇAMENTO (900+ SERVIÇOS)

## 📋 Visão Geral

Este documento estabelece as diretrizes fundamentais para a transição da **Plataforma
Única Digital do Cidadão (SILA)** da fase de desenvolvimento para o lançamento com
**900+ serviços**. A base arquitetônica está sólida, e o foco agora é garantir padrões
de desenvolvimento consistentes e preparação adequada para o crescimento acelerado.

---

## 1. 🔐 GESTÃO DE CREDENCIAIS DE DESENVOLVIMENTO

### 1.1 Credenciais Padrão (Regra de Ouro)

| Credencial             | Status         | Ação Requerida                                               |
| :--------------------- | :------------- | :----------------------------------------------------------- |
| **admin@sila.gov.ao**  | ✅ Manter      | Deve existir no banco de dados, criado via `setup_admin.sql` |
| **truman0@sila.co.ao** | ✅ Manter      | Deve existir no banco de dados, criado via `setup_admin.sql` |
| **Senha Padrão**       | **`adm123`**   | **Manter esta senha em desenvolvimento**                     |
| **Usuário**            | Marcelo Truman | **Manter** (Associado ao `truman0@sila.co.ao`)               |
| **Telefone/WhatsApp**  | `926878449`    | **Manter** (Essencial para testes de módulos)                |

### 1.2 Instrução para o Agente

> **"Para fins de desenvolvimento e testes de integração, mantenha as credenciais
> `admin@sila.gov.ao` e `truman0@sila.co.ao` ativas e com a senha de baixa complexidade
> (`adm123`), conforme o padrão `setup_admin.sql`. A segurança será tratada como um
> _sprint_ dedicado antes da produção."**

### 1.3 Arquivo de Setup

O arquivo `setup_admin.sql` na raiz do projeto contém:

- Criação automática de ambos os superusuários
- Senha hash para `adm123`
- Região LUANDA-CBD configurada
- Comentários explicativos sobre a estratégia de transição

---

## 2. 🏗️ DIRETRIZ ARQUITETÔNICA CENTRAL

### 2.1 Princípio Fundamental: Backend Unificado

| Camada                       | Cliente (Frontend)                                                             | Propósito/Diretriz                                                                     |
| :--------------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| **Backend (Python/FastAPI)** | **Único**                                                                      | **Fonte Única de Verdade (SUVs):** Todos os clientes consomem a mesma API (`/api/v1/`) |
| **Frontend Clientes**        | **Portal do Cidadão (Web):** Acesso Público                                    | Interface de consumo dos **900+ serviços**                                             |
| **Frontend Clientes**        | **Interface Administrativa (Web/Desktop/Móvel):** Acesso Interno/Governamental | Interface de gestão dos **900+ serviços** (CRUD, Auditoria, Aprovações, Workflow)      |

### 2.2 Instrução para o Agente

> **"A distinção entre o Portal do Cidadão e a Interface Administrativa é feita **apenas
> no Frontend (UI/UX)** e por meio de **regras de permissão (Roles/Scopes)** no Backend
> (`app/core/security.py`). Não crie APIs separadas. O Backend deve sempre servir a
> mesma API (`/api/v1/`), e a segurança fará o controle de acesso necessário."**

### 2.3 Estrutura de Permissões

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

---

## 3. 👁️ VISIBILIDADE E COMUNICAÇÃO (PORTAL DO CIDADÃO)

### 3.1 Referência aos 900+ Serviços

| Requisito                    | Local Sugerido (Frontend)                  | Detalhe Estético                                                                                                                    |
| :--------------------------- | :----------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Referência 900+ Serviços** | **Landing Page / Dashboard / Service Hub** | **Estilo Estoniano/Governamental:** Métrica informativa (Ex: "900+ Serviços Digitais Ativos. A sua administração na palma da mão.") |

### 3.2 Instrução para o Agente

> **"No Frontend (Portal do Cidadão), implemente uma referência estética e informativa
> aos **'900+ Serviços'** no componente principal (`ServiceHubPage` ou `Dashboard`).
> Isso reforça a visão de uma plataforma única e completa, seguindo a sobriedade
> estética de um portal governamental."**

### 3.3 Implementação Sugerida

```typescript
// Componente de métricas do dashboard
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

---

## 4. 🔒 DIRETRIZ DE SEGURANÇA E COMPLEXIDADE

### 4.1 Estratégia de Transição

| Aspecto                 | Fase de Desenvolvimento                   | Fase de Produção (Pré-Lançamento)                      |
| :---------------------- | :---------------------------------------- | :----------------------------------------------------- |
| **Senhas**              | Baixa complexidade (`adm123`)             | Alta complexidade, _salting_, _hashing_ obrigatório    |
| **Variáveis Sensíveis** | Acesso livre ao `.env` de desenvolvimento | Rotação de chaves, segredos armazenados fora do código |
| **Autenticação**        | Fallback hardcoded para desenvolvimento   | Autenticação robusta com 2FA                           |
| **Logs**                | Logs detalhados para debug                | Logs auditáveis e seguros                              |

### 4.2 Instrução para o Agente

> **"Mantenha a liberdade total com senhas de baixa complexidade e acesso ao `.env` de
> desenvolvimento **até o início do Sprint de Pré-Produção**. Naquele momento, todas as
> senhas de superusuário deverão ser **resetadas** para um padrão de alta segurança, e
> as variáveis sensíveis do `.env` deverão ser migradas para o ambiente de _secrets_."**

### 4.3 Checklist de Transição de Segurança

- [ ] Implementar rotação automática de senhas
- [ ] Migrar variáveis sensíveis para HashiCorp Vault ou AWS Secrets Manager
- [ ] Implementar autenticação de dois fatores (2FA)
- [ ] Configurar logs de auditoria
- [ ] Implementar rate limiting
- [ ] Configurar HTTPS obrigatório
- [ ] Implementar validação de entrada robusta
- [ ] Configurar backup automático e criptografado

---

## 5. 📚 INSTRUÇÕES PARA O AGENTE DE DESENVOLVIMENTO

### 5.1 Princípios Fundamentais

1. **Backend Único**: Nunca criar APIs separadas para diferentes clientes
2. **Segurança Gradual**: Manter simplicidade em desenvolvimento, complexidade em
   produção
3. **Visibilidade dos Serviços**: Sempre referenciar os 900+ serviços no frontend
4. **Credenciais Padrão**: Manter `adm123` até o sprint de pré-produção
5. **Arquitetura Consistente**: Seguir padrões estabelecidos nas Fases 1-4

### 5.2 Comandos Essenciais

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

### 5.3 Estrutura de Desenvolvimento

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

---

## 6. 🚀 ROADMAP PARA 900+ SERVIÇOS

### 6.1 Fases de Implementação

1. **Fase Atual**: Base arquitetônica sólida ✅
2. **Próxima**: Padronização de desenvolvimento
3. **Seguinte**: Implementação em massa de serviços
4. **Final**: Sprint de segurança e lançamento

### 6.2 Métricas de Sucesso

- **Desenvolvimento**: Velocidade de implementação mantida
- **Qualidade**: Zero regressões na base arquitetônica
- **Segurança**: Transição suave para produção
- **Usabilidade**: Interface clara e informativa sobre os 900+ serviços

---

## 📞 Contato e Suporte

- **Desenvolvedor Principal**: Marcelo Truman
- **Email**: truman0@sila.co.ao
- **Telefone**: 926878449
- **Sistema**: admin@sila.gov.ao

---

_Este documento deve ser atualizado conforme a evolução do projeto e as necessidades de
transição para produção._
