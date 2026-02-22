# Docker Backend Fixes

## 🐛 Problemas Identificados

### 1. ModuleNotFoundError: No module named 'bcrypt'

**Causa:** O pacote `bcrypt` não estava listado no `requirements.txt`, mas é usado pelo
código (especialmente em `modules/common/utils/utils.py`).

**Solução:** Adicionado `bcrypt==4.1.2` ao `requirements.txt`.

### 2. FAILED: No 'script_location' key found in configuration

**Causa:** O Alembic estava sendo executado antes de mudar para o diretório `/app`,
então não encontrava o arquivo `alembic.ini`.

**Solução:** Reordenado o `entrypoint.sh` para:

1. Primeiro configurar `PYTHONPATH` e mudar para o diretório correto (`/app`)
2. Depois executar as migrações do Alembic

## ✅ Correções Aplicadas

### `backend/requirements.txt`

Adicionada linha:

```
bcrypt==4.1.2
```

### `backend/entrypoint.sh`

**Antes:**

```bash
# Migrações primeiro
if command -v alembic >/dev/null 2>&1; then
    alembic upgrade head
fi

# Depois mudar diretório
cd /app
```

**Depois:**

```bash
# Mudar diretório primeiro
if [ -d "/app" ]; then
    export PYTHONPATH="/app:$(dirname /app):${PYTHONPATH:-}"
    cd /app
fi

# Depois executar migrações
if command -v alembic >/dev/null 2>&1 && [ -f "alembic.ini" ]; then
    alembic upgrade head
fi
```

## 🚀 Próximos Passos

Após essas correções, você precisa **rebuildar a imagem Docker**:

```bash
cd ~/dev/sila-system/devops
FORCE_REBUILD=true ./start_backend.sh
```

Ou manualmente:

```bash
cd ~/dev/sila-system/devops
docker compose build --no-cache backend
docker compose up -d backend
```

## ✅ Validação

Após rebuild, verifique:

1. **bcrypt instalado:**

   ```bash
   docker exec sila-backend python -c "import bcrypt; print('✅ bcrypt OK')"
   ```

2. **Alembic funcionando:**

   ```bash
   docker exec sila-backend alembic current
   ```

3. **API respondendo:**
   ```bash
   curl http://localhost:8000/health
   ```

## 📝 Notas

- A versão `bcrypt==4.1.2` é compatível com Python 3.11
- O `entrypoint.sh` agora verifica se `alembic.ini` existe antes de executar migrações
- O diretório de trabalho é configurado antes de qualquer operação
