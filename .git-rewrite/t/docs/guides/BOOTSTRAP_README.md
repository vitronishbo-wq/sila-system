# 🚀 Bootstrap SILA Backend

Script inteligente para automatizar completamente a configuração e inicialização do
ambiente de desenvolvimento do backend SILA.

## ✨ Funcionalidades

- 🔍 **Detecção automática** de dependências ausentes
- 📦 **Instalação automática** de pacotes do sistema
- 🧪 **Criação e ativação** de ambiente virtual Python
- 📚 **Instalação automática** de dependências Python
- 🔐 **Configuração inteligente** de variáveis de ambiente
- 🗄️ **Verificação e criação** de banco de dados PostgreSQL
- 📜 **Aplicação automática** de migrações Alembic
- 🚀 **Inicialização otimizada** do servidor com configurações ideais
- 🔧 **Serviços opcionais** (Redis, logging, etc.)

## 🛠️ Como Usar

### Método 1: Execução Direta

```bash
cd /opt/sila-system
chmod +x bootstrap_sila_backend.sh
./bootstrap_sila_backend.sh
```

### Método 2: Via Make (se disponível)

```bash
make bootstrap-backend
```

## 📋 O que o Script Faz

### 1. Verificação de Dependências do Sistema

- Python 3.12+
- PostgreSQL
- Redis
- Build tools
- Bibliotecas de desenvolvimento

### 2. Ambiente Virtual

- Cria `.venv` se não existir
- Ativa ambiente virtual
- Atualiza pip

### 3. Dependências Python

- Instala todas as dependências do `requirements.txt`
- Verifica compatibilidade

### 4. Configuração de Ambiente

- Cria `.env` se não existir (baseado em `env.example`)
- Gera chave secreta automaticamente
- Configura variáveis essenciais

### 5. Banco de Dados

- Inicia PostgreSQL se necessário
- Cria banco `sila_dev` se não existir
- Configura conexão

### 6. Migrações

- Aplica migrações pendentes do Alembic
- Trata erros de migração graciosamente

### 7. Servidor

- Inicia servidor em `http://localhost:8080`
- Configurações otimizadas para desenvolvimento
- Logging detalhado
- Recarregamento automático

## 🎯 Endpoints Disponíveis

Após inicialização:

- **API Raiz**: `http://localhost:8080/`
- **Documentação Interativa**: `http://localhost:8080/docs`
- **Documentação Alternativa**: `http://localhost:8080/redoc`
- **Health Check**: `http://localhost:8080/health`

## 🔧 Personalização

### Variáveis de Ambiente Personalizadas

O script respeita variáveis existentes no `.env`. Para personalizar:

```bash
# Editar .env antes de executar o script
nano backend/.env
```

### Configurações Comuns

```bash
# Porta personalizada
PORT=9000 ./bootstrap_sila_backend.sh

# Host específico
HOST=127.0.0.1 ./bootstrap_sila_backend.sh

# Ambiente de produção (desabilita reload)
ENVIRONMENT=production ./bootstrap_sila_backend.sh
```

## 🚨 Solução de Problemas

### Problema: Permissões

```bash
# Se houver problemas de permissão
chmod +x bootstrap_sila_backend.sh
```

### Problema: PostgreSQL não inicia

```bash
# Iniciar manualmente
sudo systemctl start postgresql@16-main
sudo -u postgres createdb sila_dev
```

### Problema: Porta ocupada

```bash
# Verificar processos na porta 8080
lsof -i :8080
# Matar processo: kill -9 <PID>
```

### Problema: Ambiente virtual

```bash
# Recriar ambiente virtual
rm -rf backend/.venv
./bootstrap_sila_backend.sh
```

## 📊 Logs e Monitoramento

O script produz logs coloridos detalhados:

- 🔵 **Info**: Operações normais
- ✅ **Sucesso**: Confirmações
- ⚠️ **Aviso**: Problemas não críticos
- ❌ **Erro**: Problemas críticos

## 🔄 Desenvolvimento

Para parar o servidor:

```bash
# Encontrar PID
ps aux | grep uvicorn

# Matar processo
kill <PID_DO_UVICORN>
```

Para reiniciar com mudanças:

```bash
# O servidor tem reload automático ativado
# Apenas salve os arquivos Python
```

## 📚 Arquivos Relacionados

- `bootstrap_sila_backend.sh` - Script principal
- `backend/main.py` - Ponto de entrada da aplicação
- `backend/requirements.txt` - Dependências Python
- `backend/env.example` - Template de configuração
- `backend/.env` - Configuração (criado automaticamente)

## 🎉 Resultado Esperado

Após execução bem-sucedida:

```
╔═══════════════════════════════════════════════════════════╗
║                    🚀 SILA BACKEND READY!                ║
╠═══════════════════════════════════════════════════════════╣
║  🌐 Servidor: http://localhost:8080                      ║
║  📚 Documentação: http://localhost:8080/docs             ║
║  🔄 Recarregar: http://localhost:8080/redoc              ║
║  🆔 PID do servidor: 12345                               ║
╚═══════════════════════════════════════════════════════════╝
```
