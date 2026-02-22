# 🔒 ESTRATÉGIA DE TRANSIÇÃO DE SEGURANÇA: DESENVOLVIMENTO → PRODUÇÃO

## 📋 Visão Geral

Este documento detalha a estratégia de transição de segurança da **Plataforma Única
Digital do Cidadão (SILA)** da fase de desenvolvimento para produção, garantindo que a
complexidade de segurança seja implementada no momento adequado sem comprometer a
velocidade de desenvolvimento.

---

## 1. 🎯 PRINCÍPIO FUNDAMENTAL: SEGURANÇA GRADUAL

### 1.1 Filosofia da Estratégia

> **"Mantenha a liberdade total com senhas de baixa complexidade e acesso ao `.env` de
> desenvolvimento **até o início do Sprint de Pré-Produção**. Naquele momento, todas as
> senhas de superusuário deverão ser **resetadas** para um padrão de alta segurança, e
> as variáveis sensíveis do `.env` deverão ser migradas para o ambiente de _secrets_."**

### 1.2 Justificativa Tática

| Fase                        | Prioridade     | Justificativa                                          |
| :-------------------------- | :------------- | :----------------------------------------------------- |
| **Desenvolvimento (Atual)** | **Velocidade** | Foco na lógica de negócio e arquitetura (Fases 1-4)    |
| **Pré-Produção**            | **Segurança**  | Implementação robusta de segurança antes do lançamento |
| **Produção**                | **Manutenção** | Monitoramento e evolução contínua                      |

---

## 2. 🔐 CREDENCIAIS DE DESENVOLVIMENTO (FASE ATUAL)

### 2.1 Credenciais Padrão Mantidas

| Credencial             | Valor    | Status    | Justificativa                          |
| :--------------------- | :------- | :-------- | :------------------------------------- |
| **admin@sila.gov.ao**  | `adm123` | ✅ Manter | Desenvolvimento e testes de integração |
| **truman0@sila.co.ao** | `adm123` | ✅ Manter | Desenvolvimento e testes de integração |
| **Marcelo Truman**     | Usuário  | ✅ Manter | Referência para testes de módulos      |
| **926878449**          | Telefone | ✅ Manter | Testes de notificações e autenticação  |

### 2.2 Arquivo de Configuração

```sql
-- setup_admin.sql
-- Senha hash para 'adm123': $2b$12$Q3pJ9lXePzW9FdpK1okdyOcbY5ib1qZzxlXK0lLmuDgJd57p22bGK
INSERT INTO users (email, hashed_password, full_name, is_superuser) VALUES
('admin@sila.gov.ao', '$2b$12$Q3pJ9lXePzW9FdpK1okdyOcbY5ib1qZzxlXK0lLmuDgJd57p22bGK', 'Administrador SILA', true),
('truman0@sila.co.ao', '$2b$12$Q3pJ9lXePzW9FdpK1okdyOcbY5ib1qZzxlXK0lLmuDgJd57p22bGK', 'Marcelo Truman', true);
```

### 2.3 Variáveis de Ambiente (.env)

```bash
# Desenvolvimento - Acesso livre permitido
POSTGRES_PASSWORD=Truman1*Marcelo1*
SECRET_KEY=dev-secret-key-not-for-production
DEBUG=True
ENVIRONMENT=development
```

---

## 3. 🚀 SPRINT DE PRÉ-PRODUÇÃO (PONTO DE CORTE)

### 3.1 Checklist de Transição de Segurança

#### 3.1.1 Autenticação e Autorização

- [ ] **Resetar todas as senhas de superusuário**
  - [ ] Gerar senhas complexas (mín. 16 caracteres, símbolos, números)
  - [ ] Implementar rotação automática de senhas
  - [ ] Configurar autenticação de dois fatores (2FA)
  - [ ] Implementar bloqueio de conta após tentativas falhadas

#### 3.1.2 Gerenciamento de Segredos

- [ ] **Migrar variáveis sensíveis para secrets manager**
  - [ ] HashiCorp Vault ou AWS Secrets Manager
  - [ ] Rotação automática de chaves
  - [ ] Auditoria de acesso a segredos
  - [ ] Backup criptografado de segredos

#### 3.1.3 Criptografia e Hashing

- [ ] **Implementar criptografia robusta**
  - [ ] Bcrypt com salt rounds ≥ 12
  - [ ] Criptografia de dados sensíveis em trânsito (TLS 1.3)
  - [ ] Criptografia de dados em repouso
  - [ ] Certificados SSL/TLS válidos

#### 3.1.4 Logs e Auditoria

- [ ] **Configurar logs de auditoria**
  - [ ] Logs de autenticação e autorização
  - [ ] Logs de acesso a dados sensíveis
  - [ ] Logs de alterações de configuração
  - [ ] Retenção de logs conforme LGPD

#### 3.1.5 Proteção de API

- [ ] **Implementar proteções de API**
  - [ ] Rate limiting por usuário/IP
  - [ ] Validação rigorosa de entrada
  - [ ] Sanitização de dados
  - [ ] Proteção contra SQL injection

### 3.2 Script de Transição

```bash
#!/bin/bash
# transition_to_production.sh

echo "🔒 Iniciando transição de segurança para produção..."

# 1. Backup do banco de dados
echo "📦 Criando backup do banco de dados..."
pg_dump sila_db > backup_pre_production_$(date +%Y%m%d_%H%M%S).sql

# 2. Resetar senhas de superusuário
echo "🔑 Resetando senhas de superusuário..."
python scripts/reset_production_passwords.py

# 3. Migrar variáveis sensíveis
echo "🔐 Migrando variáveis sensíveis para secrets manager..."
python scripts/migrate_secrets.py

# 4. Configurar HTTPS obrigatório
echo "🌐 Configurando HTTPS obrigatório..."
python scripts/configure_https.py

# 5. Ativar logs de auditoria
echo "📝 Ativando logs de auditoria..."
python scripts/enable_audit_logs.py

echo "✅ Transição de segurança concluída!"
```

---

## 4. 🛡️ CONFIGURAÇÕES DE PRODUÇÃO

### 4.1 Variáveis de Ambiente de Produção

```bash
# Produção - Segurança máxima
POSTGRES_PASSWORD=${SECRETS_MANAGER:postgres_password}
SECRET_KEY=${SECRETS_MANAGER:secret_key}
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=WARNING
AUDIT_LOGS=True
RATE_LIMIT_ENABLED=True
HTTPS_ONLY=True
```

### 4.2 Configuração de Segurança

```python
# backend/app/core/security.py
class ProductionSecurityConfig:
    # Senhas
    MIN_PASSWORD_LENGTH = 16
    REQUIRE_SPECIAL_CHARS = True
    REQUIRE_NUMBERS = True
    REQUIRE_UPPERCASE = True
    PASSWORD_HISTORY = 5

    # Autenticação
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_DURATION = 900  # 15 minutos
    SESSION_TIMEOUT = 1800  # 30 minutos

    # Criptografia
    BCRYPT_ROUNDS = 14
    JWT_ALGORITHM = "RS256"
    JWT_EXPIRATION = 1800  # 30 minutos

    # Rate Limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 3600  # 1 hora
```

### 4.3 Monitoramento de Segurança

```python
# backend/app/core/monitoring.py
class SecurityMonitoring:
    def log_authentication_attempt(self, username, success, ip_address):
        """Log de tentativas de autenticação"""
        pass

    def log_data_access(self, user_id, resource, action):
        """Log de acesso a dados sensíveis"""
        pass

    def detect_anomalies(self):
        """Detecção de atividades anômalas"""
        pass

    def generate_security_report(self):
        """Relatório de segurança"""
        pass
```

---

## 5. 📊 MÉTRICAS DE SEGURANÇA

### 5.1 KPIs de Segurança

| Métrica                 | Desenvolvimento | Produção  | Meta   |
| :---------------------- | :-------------- | :-------- | :----- |
| **Tempo de Login**      | < 1s            | < 2s      | < 3s   |
| **Tentativas Falhadas** | Não monitorado  | < 5%      | < 2%   |
| **Uptime**              | 95%             | 99.9%     | 99.95% |
| **Tempo de Resposta**   | < 500ms         | < 1s      | < 2s   |
| **Logs de Auditoria**   | Básicos         | Completos | 100%   |

### 5.2 Alertas de Segurança

```yaml
# alerts.yml
security_alerts:
  - name: "Multiple Failed Logins"
    condition: "failed_logins > 5 in 5 minutes"
    action: "lock_account_and_notify_admin"

  - name: "Unusual Data Access"
    condition: "data_access_volume > 1000 in 1 hour"
    action: "investigate_and_alert"

  - name: "API Rate Limit Exceeded"
    condition: "api_requests > 1000 in 1 hour"
    action: "temporary_block_and_log"
```

---

## 6. 🔄 PROCESSO DE ROLLBACK

### 6.1 Plano de Contingência

```bash
#!/bin/bash
# rollback_security.sh

echo "⚠️ Executando rollback de segurança..."

# 1. Restaurar backup do banco
echo "📦 Restaurando backup do banco de dados..."
psql sila_db < backup_pre_production_YYYYMMDD_HHMMSS.sql

# 2. Reverter variáveis de ambiente
echo "🔙 Revertendo variáveis de ambiente..."
cp .env.development .env

# 3. Desativar logs de auditoria
echo "📝 Desativando logs de auditoria..."
python scripts/disable_audit_logs.py

# 4. Restaurar credenciais de desenvolvimento
echo "🔑 Restaurando credenciais de desenvolvimento..."
psql -d sila_db -f setup_admin.sql

echo "✅ Rollback concluído!"
```

---

## 7. 📅 CRONOGRAMA DE IMPLEMENTAÇÃO

### 7.1 Fases de Transição

| Fase              | Duração   | Atividades                      | Responsável       |
| :---------------- | :-------- | :------------------------------ | :---------------- |
| **Preparação**    | 1 semana  | Backup, documentação, testes    | DevOps            |
| **Implementação** | 2 semanas | Configuração de segurança       | Security Team     |
| **Testes**        | 1 semana  | Testes de penetração, validação | QA + Security     |
| **Go-Live**       | 1 dia     | Deploy em produção              | DevOps + Security |
| **Monitoramento** | Contínuo  | Monitoramento e ajustes         | Security Team     |

### 7.2 Marcos Críticos

- [ ] **Semana 1**: Backup completo e documentação
- [ ] **Semana 2**: Implementação de segurança
- [ ] **Semana 3**: Testes de penetração
- [ ] **Semana 4**: Deploy em produção
- [ ] **Pós-Deploy**: Monitoramento 24/7

---

## 8. 📞 CONTATOS E RESPONSABILIDADES

### 8.1 Equipe de Segurança

| Função              | Responsável    | Contato                |
| :------------------ | :------------- | :--------------------- |
| **Security Lead**   | Marcelo Truman | truman0@sila.co.ao     |
| **DevOps Security** | TBD            | devops@sila.gov.ao     |
| **Compliance**      | TBD            | compliance@sila.gov.ao |

### 8.2 Escalação de Incidentes

1. **Nível 1**: Desenvolvedor responsável
2. **Nível 2**: Security Lead (Marcelo Truman)
3. **Nível 3**: Diretor de TI
4. **Nível 4**: Diretor Executivo

---

## 9. 📚 DOCUMENTAÇÃO RELACIONADA

- [Diretrizes de Transição para Lançamento](./DIRETRIZES_TRANSICAO_LANCAMENTO.md)
- [Arquitetura de Segurança](./ARQUITETURA_SEGURANCA.md)
- [Procedimentos de Backup](./PROCEDIMENTOS_BACKUP.md)
- [Política de Senhas](./POLITICA_SENHAS.md)

---

_Este documento deve ser revisado e atualizado antes de cada transição de ambiente._
