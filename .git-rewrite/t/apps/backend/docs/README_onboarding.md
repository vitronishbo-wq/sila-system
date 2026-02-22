# 📦 Onboarding de Desenvolvimento de Módulos

## 🧱 Estrutura Padrão

modules/ └── nome_modulo/ ├── endpoints.py ├── schemas.py ├── services.py

## 🛠️ Criação de Novo Módulo

1. Criar diretório em `modules/nome_modulo/`.
2. Criar os 3 arquivos base.
3. Definir schemas com `BaseModel` no `schemas.py`.
4. Criar funções com `Session` no `services.py`.
5. Criar rotas REST com prefixo no `endpoints.py`.

## 🔐 Permissões

Usar:

```python
from app.core.deps import require_role
postgres = Depends(require_role(["postgres"]))
```

## 📥 Registro

```python
from app.modules.nome_modulo import endpoints as nome_endpoints
app.include_router(nome_endpoints.router)
```

## 🧪 Testes

Salvar em `tests/test_nome_modulo.py`, usar TestClient e pytest.

---
