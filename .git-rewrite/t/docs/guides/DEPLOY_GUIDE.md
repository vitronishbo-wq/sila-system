# 🚀 Guia de Deploy Automatizado - Sila System

Este guia explica como usar os scripts de deploy automatizado do projeto.

## 📋 Índice

- [Scripts Disponíveis](#scripts-disponíveis)
- [Pré-requisitos](#pré-requisitos)
- [Configuração Inicial](#configuração-inicial)
- [Uso Diário](#uso-diário)
- [Funcionalidades](#funcionalidades)

---

## 🛠️ Scripts Disponíveis

### 1. `setup_git_remote.sh`

**Propósito:** Configuração inicial dos repositórios remotos (GitHub e GitLab)

**Uso:**

```bash
./setup_git_remote.sh
```

**O que faz:**

- ✅ Configura usuário Git (nome e email)
- ✅ Adiciona remotes GitHub e GitLab via SSH
- ✅ Testa conexões com os repositórios
- ✅ Mostra status atual dos remotes

**Quando usar:** Uma vez, na configuração inicial do projeto

---

### 2. `deploy_final.sh` ⭐

**Propósito:** Deploy completo automatizado (RECOMENDADO)

**Uso:**

```bash
./deploy_final.sh
```

**O que faz:**

1. ✅ Verifica se é um repositório Git (inicializa se necessário)
2. ✅ Adiciona todas as alterações ao staging
3. ✅ Cria commit com timestamp
4. ✅ Gera versão automática (formato: `vYYYYMMDD.HHMMSS`)
5. ✅ Atualiza `VERSION.txt`
6. ✅ Gera/atualiza `CHANGELOG.md` automaticamente
7. ✅ Cria tag Git com a versão
8. ✅ Configura remotes (se necessário)
9. ✅ Faz push para todos os remotes (GitHub e GitLab)
10. ✅ Envia tags para os remotes
11. ✅ Sobe containers Docker com `docker-compose up -d --build`
12. ✅ Mostra resumo completo do deploy

**Quando usar:** Sempre que quiser fazer um deploy completo da fase atual

---

### 3. `quick_deploy.sh`

**Propósito:** Deploy rápido sem perguntas

**Uso:**

```bash
./quick_deploy.sh
```

**O que faz:**

- Verifica se há alterações
- Se houver, executa `deploy_final.sh`
- Se não houver, apenas informa que está tudo atualizado

**Quando usar:** Para verificação rápida e deploy se necessário

---

## 🔧 Pré-requisitos

### 1. Git instalado

```bash
git --version
```

### 2. Chaves SSH configuradas

#### Para GitHub:

```bash
# Gerar chave (se não tiver)
ssh-keygen -t ed25519 -C "silahbo@gmail.com"

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub

# Adicionar em: https://github.com/settings/keys
```

#### Para GitLab:

```bash
# Usar a mesma chave ou gerar outra
cat ~/.ssh/id_ed25519.pub

# Adicionar em: https://gitlab.com/-/profile/keys
```

#### Testar conexões:

```bash
ssh -T git@github.com
ssh -T git@gitlab.com
```

### 3. Docker e Docker Compose instalados

```bash
docker --version
docker-compose --version
```

---

## 🎯 Configuração Inicial

### Passo 1: Tornar scripts executáveis

```bash
chmod +x setup_git_remote.sh
chmod +x deploy_final.sh
chmod +x quick_deploy.sh
```

### Passo 2: Configurar repositórios remotos

```bash
./setup_git_remote.sh
```

Isso vai:

- Configurar seu usuário Git
- Adicionar remotes GitHub e GitLab (via SSH)
- Testar as conexões

### Passo 3: Primeiro deploy

```bash
./deploy_final.sh
```

---

## 💼 Uso Diário

### Cenário 1: Deploy completo de uma fase

```bash
# Fez várias alterações e quer versionar + subir containers
./deploy_final.sh
```

### Cenário 2: Verificação rápida

```bash
# Quer ver se há algo para commitar e fazer deploy se houver
./quick_deploy.sh
```

### Cenário 3: Apenas reconfigurar remotes

```bash
# Se mudou algo nas configurações Git
./setup_git_remote.sh
```

---

## ✨ Funcionalidades

### 🏷️ Versionamento Automático

- Formato: `vYYYYMMDD.HHMMSS` (ex: `v20251005.233045`)
- Salvo em `VERSION.txt`
- Tag Git criada automaticamente
- Tags enviadas para todos os remotes

### 📝 Changelog Automático

- Arquivo `CHANGELOG.md` gerado/atualizado automaticamente
- Lista todos os commits desde a última tag
- Formato organizado por versão e data
- Mantém histórico completo

### 🔄 Push Multi-Remote

- Envia para GitHub e GitLab simultaneamente
- Inclui commits e tags
- Tratamento de erros individual por remote

### 🐳 Docker Integration

- Detecta `docker-compose.yml` automaticamente
- Sobe containers com rebuild (`--build`)
- Modo detached (`-d`)
- Mostra status dos containers após deploy

### 📊 Resumo Detalhado

Após cada deploy, você vê:

- ✅ Versão criada
- ✅ Data e hora
- ✅ Usuário Git
- ✅ Branch atual
- ✅ Hash do commit
- ✅ Remotes configurados
- ✅ Status dos containers Docker

---

## 🎨 Exemplo de Fluxo de Trabalho

```bash
# 1. Trabalhar no código
vim backend/app.py
vim frontend/src/App.jsx

# 2. Testar localmente
docker-compose up

# 3. Quando estiver satisfeito, fazer deploy
./deploy_final.sh

# Resultado:
# ✅ Commit criado
# ✅ Versão: v20251005.233045
# ✅ CHANGELOG.md atualizado
# ✅ Tag criada
# ✅ Push para GitHub ✓
# ✅ Push para GitLab ✓
# ✅ Containers reiniciados
# ✅ Sistema pronto!
```

---

## 🔍 Verificação de Status

### Ver versão atual

```bash
cat VERSION.txt
```

### Ver changelog

```bash
cat CHANGELOG.md
```

### Ver tags Git

```bash
git tag -l
```

### Ver último commit

```bash
git log -1
```

### Ver remotes configurados

```bash
git remote -v
```

### Ver status dos containers

```bash
docker-compose ps
```

---

## 🆘 Troubleshooting

### Erro: "Permission denied (publickey)"

**Problema:** Chave SSH não configurada

**Solução:**

```bash
# Gerar chave
ssh-keygen -t ed25519 -C "silahbo@gmail.com"

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar e adicionar ao GitHub/GitLab
cat ~/.ssh/id_ed25519.pub
```

### Erro: "remote: Repository not found"

**Problema:** URL do repositório incorreta ou sem permissão

**Solução:**

```bash
# Verificar remotes
git remote -v

# Reconfigurar se necessário
./setup_git_remote.sh
```

### Erro: "docker-compose: command not found"

**Problema:** Docker Compose não instalado

**Solução:**

```bash
# Instalar Docker Compose
sudo apt-get install docker-compose

# Ou usar plugin do Docker
docker compose version
```

### Containers não sobem

**Problema:** Erro no docker-compose.yml ou portas ocupadas

**Solução:**

```bash
# Ver logs detalhados
docker-compose logs

# Parar containers existentes
docker-compose down

# Tentar novamente
./deploy_final.sh
```

---

## 📚 Arquivos Gerados

### `VERSION.txt`

Contém a versão atual do sistema

```
v20251005.233045
```

### `CHANGELOG.md`

Histórico de mudanças organizado por versão

```markdown
# Changelog

## [v20251005.233045] - 2025-10-05 23:30:45

### Alterações

- 🚀 Deploy versão v20251005.233045
- ✨ Adiciona nova funcionalidade X
- 🐛 Corrige bug Y
```

### `logs/git_setup.log`

Log da configuração dos remotes Git

---

## 🎯 Boas Práticas

1. **Sempre teste localmente antes do deploy**

   ```bash
   docker-compose up
   ```

2. **Faça commits frequentes durante o desenvolvimento**

   ```bash
   git add .
   git commit -m "feat: adiciona funcionalidade X"
   ```

3. **Use deploy_final.sh apenas para versões estáveis**

   - Não use para cada pequena mudança
   - Use quando a fase estiver completa e testada

4. **Verifique o CHANGELOG.md após cada deploy**

   - Confirme que as mudanças estão documentadas
   - Edite manualmente se necessário

5. **Mantenha suas chaves SSH seguras**
   - Nunca compartilhe chaves privadas
   - Use senhas fortes nas chaves

---

## 🚀 Próximos Passos

Após configurar tudo:

1. ✅ Configure as chaves SSH
2. ✅ Execute `./setup_git_remote.sh`
3. ✅ Teste com `./deploy_final.sh`
4. ✅ Use `./quick_deploy.sh` no dia a dia

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `logs/git_setup.log`
2. Teste conexões SSH manualmente
3. Verifique status do Docker
4. Consulte este guia

---

**Criado por:** Vitronis Sila **Email:** silahbo@gmail.com **Projeto:** Sila System
**Última atualização:** 2025-10-05
