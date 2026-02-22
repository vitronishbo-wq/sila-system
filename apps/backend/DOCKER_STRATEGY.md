# Backend - Estratégia de Dependências e Docker

## 📦 Estrutura de Dependências

### `requirements.txt` (Produção)
Contém **todas** as dependências necessárias para rodar a aplicação em produção:
- FastAPI
- SQLAlchemy 2.0+
- Pydantic V2
- Asyncpg
- Redis
- Python-Jose
- Passlib
- Alembic
- Etc.

**Uso:**
```bash
pip install -r requirements.txt
```

### `requirements-test.txt` (Testes)
Contém **apenas** dependências para testes e desenvolvimento:
- pytest
- pytest-asyncio
- pytest-cov
- locust (performance)
- black (formatação)
- flake8 (lint)
- mypy (type checking)

**Nota:** `requirements-test.txt` **não inclui** as dependências de produção (aquelas são transitivas do requirements.txt).

**Uso:**
```bash
pip install -r requirements.txt -r requirements-test.txt
```

---

## 🐳 Multi-stage Dockerfile

O `Dockerfile` foi refatorado para suportar **3 estágios**:

### 1. **BASE** (Comum a todos)
```dockerfile
FROM python:3.12-slim AS base
# ... setup comum (apt-get, PATH, WORKDIR)
```

### 2. **DEVELOPMENT** (Hot reload local)
```dockerfile
FROM base AS development
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--reload"]
```

**Uso no docker-compose.yml (default):**
```yaml
backend:
  build:
    context: ./apps/backend
    target: development  # ← sem especificar, use essa como default
```

### 3. **TEST** (Testes automatizados)
```dockerfile
FROM base AS test
COPY requirements.txt requirements-test.txt ./
RUN pip install -r requirements.txt -r requirements-test.txt
COPY . .
CMD ["pytest", "-v", "--cov=.", "--cov-report=html"]
```

**Uso para rodar testes:**
```bash
docker build --target test -t sila-backend:test ./apps/backend
docker run sila-backend:test
```

### 4. **PRODUCTION** (Otimizado para prod)
```dockerfile
FROM base AS production
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install gunicorn uvicorn[standard]
COPY . .
COPY entrypoint.sh /entrypoint.sh
HEALTHCHECK ...
ENTRYPOINT ["/entrypoint.sh"]
```

**Uso em produção:**
```yaml
backend:
  build:
    context: ./apps/backend
    target: production  # ← especificar target
    dockerfile: Dockerfile
```

---

## 🚀 Como usar

### Desenvolvimento (Hot reload)
```bash
cd ~/dev/sila-system
docker-compose up backend --build
```
O backend vai rodar em `http://localhost:8000` com hot reload ativado.

### Testes
```bash
docker build --target test -t sila-backend:test ./apps/backend
docker run --rm sila-backend:test
```

### Produção
```bash
docker build --target production -t sila-backend:latest ./apps/backend
docker run -p 8000:8000 sila-backend:latest
```

---

## ✅ Benefícios

| Aspecto | Benefício |
|--------|----------|
| **Cache eficiente** | Dependências instaladas uma vez, reutilizadas em etapas diferentes |
| **Imagens leves** | Produção só tem o necessário (sem pytest, black, etc.) |
| **Hot reload** | Desenvolvimento com `--reload` automático |
| **Separação clara** | Cada etapa tem responsabilidade específica |
| **CI/CD amigável** | Fácil rodar testes ou produção no pipeline |
| **Sem conflitos** | Dependências de teste isoladas, não interferem em produção |

---

## 📝 Próximas Melhorias

- [ ] Adicionar `requirements-prod.txt` se houver dependências **apenas** para produção
- [ ] Criar `.dockerignore` para não copiar arquivos desnecessários
- [ ] Usar `pip-compile` para lock de versões exatas
- [ ] Adicionar segurança (scanning de vulnerabilidades)

