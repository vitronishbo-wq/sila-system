# 🎬 PRÓXIMOS PASSOS - PLANO DE AÇÃO CONCRETO

**Status**: ✅ Diagnóstico Concluído  
**Decision**: ✅ GO Aprovado  
**Data**: 23 de Fevereiro de 2026  
**Início Previsto**: 24 de Fevereiro de 2026

---

## 📍 Onde Estamos Agora

✅ **Completado na Sessão Anterior**:
- Saneamento arquitetural completo (5 fases)
- User model consolidado (modules/identity)
- 5 usuários criados com Sila_1983
- Seed script SQL validado
- Imports corrigidos (33 arquivos)
- Banco sincronizado

✅ **Completado Hoje**:
- Auditoria arquitetural profunda
- Identificação de 11 problemas críticos
- Mapa de dependências preciso
- Plano 3 fases realista
- Proteções detalhadas (Git, testes, rollback)

⏳ **Próximo**: Executar FASE 1

---

## 🚀 FASE 1: CONSOLIDAR CORE (Dias 1-3)

### Objetivo
Criar fundação centralizada, eliminar duplicação, manter 100% funcionalidade.

### Tarefas (em ordem)

---

### TASK 1.1: Criar Estrutura core/

**Tempo Estimado**: 30 minutos

**O que fazer**:

1. Criar diretórios:
```bash
cd /home/dev03wsl/sila-system/apps/backend

mkdir -p core/{config,db,security,integrations,events,dependencies,exceptions,logging}
touch core/__init__.py
touch core/{config,db,security,integrations,events,dependencies,exceptions,logging}/__init__.py
```

2. Criar `core/config.py`:
   - Copiar melhor do `app/core/settings.py` OU `core/config.py` existente
   - Unificar Database URL, JWT secret, logging config
   
3. Criar `core/db/`:
   - `session.py`: AsyncSessionLocal factory
   - `base.py`: Base declarativa SQLAlchemy

4. Criar `core/security/`:
   - `auth.py`: JWT, auth decorators
   - `iam_client.py`: **CONSOLIDADO** (vem próxima task)

5. Criar `core/events/`:
   - `event_bus.py`: Interface + in_memory impl
   - `decorators.py`: @event_handler

**Comandos**:
```bash
# Preparar
git checkout -b feature/refactor-phase-1-core
git pull origin develop

# Criar estrutura
python3 << 'EOF'
import os
from pathlib import Path

core = Path("core")
core.mkdir(exist_ok=True)

subdirs = [
    "config",
    "db", 
    "security",
    "integrations",
    "events",
    "dependencies",
    "exceptions",
    "logging"
]

for subdir in subdirs:
    (core / subdir).mkdir(exist_ok=True)
    (core / subdir / "__init__.py").touch()

(core / "__init__.py").touch()

print("✅ Estrutura core/ criada")
EOF
```

**Validação**:
```bash
ls -la core/
# Deve mostrar todos os subdirs
```

---

### TASK 1.2: Consolidar IAM Client (4 → 1)

**Tempo Estimado**: 40 minutos

**O que fazer**:

1. **Analisar** os 4 iam_clients para extrair best of all:

```bash
# Verificar conteúdo dos 4
cat app/modules/bi/integrations/iam_client.py
cat app/modules/service_requests/integrations/iam_client.py
cat app/modules/statistics/integrations/iam_client.py
cat app/modules/workflow/integrations/iam_client.py
```

2. **Criar** melhor versão em `core/security/iam_client.py`:

```python
# core/security/iam_client.py

"""
Integração centralizada com IAM Service.
Single source of truth para autenticação e autorização.
"""

import asyncio
import httpx
from typing import Optional, List, Dict, Any
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class IAMClient:
    """Cliente centralizado para IAM"""
    
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout
        self._client = None
    
    async def get_client(self) -> httpx.AsyncClient:
        """Get or create async client (connection pooling)"""
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetch user from IAM service"""
        try:
            client = await self.get_client()
            response = await client.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"IAM get_user_by_id failed: {e}")
            return None
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            client = await self.get_client()
            response = await client.post(
                f"{self.base_url}/verify",
                json={"token": token}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Token verification failed: {e}")
            return None
    
    async def get_user_roles(self, user_id: str) -> List[str]:
        """Get user roles"""
        try:
            user = await self.get_user_by_id(user_id)
            return user.get("roles", []) if user else []
        except Exception as e:
            logger.error(f"Error fetching roles: {e}")
            return []
    
    async def close(self):
        """Clean up client"""
        if self._client:
            await self._client.aclose()

# Instância global (singleton)
_iam_client_instance: Optional[IAMClient] = None

def get_iam_client(base_url: str = None) -> IAMClient:
    """Factory para IAM client"""
    global _iam_client_instance
    
    if not _iam_client_instance:
        from core.config import settings
        url = base_url or getattr(settings, 'IAM_URL', 'http://iam-service:8001')
        _iam_client_instance = IAMClient(url)
    
    return _iam_client_instance

# Exportar
iam_client = get_iam_client()

__all__ = ["IAMClient", "get_iam_client", "iam_client"]
```

3. **Redirecionar** imports em módulos:

```bash
# Deletar os 4 antigos
rm app/modules/bi/integrations/iam_client.py
rm app/modules/service_requests/integrations/iam_client.py
rm app/modules/statistics/integrations/iam_client.py
rm app/modules/workflow/integrations/iam_client.py

# Atualizar imports nesses módulos
# Antes: from ..integrations.iam_client import iam_client
# Depois: from core.security.iam_client import iam_client
```

**Script de redirecionamento**:
```bash
# Encontrar todos os imports antigos
grep -r "from.*integrations.*iam_client" app/modules/ --include="*.py"

# Criar patch automaticamente
find app/modules -name "*.py" -exec sed -i \
  's|from \.\.[^/]*integrations\.iam_client|from core.security.iam_client|g' {} \;
```

**Validação**:
```bash
# Verificar core/security/iam_client.py existe
ls -la core/security/iam_client.py

# Verificar não há mais imports dos antigos
grep -r "integrations.iam_client" app/modules/ --include="*.py"  # Deve retornar vazio
```

---

### TASK 1.3: Consolidar EventBus (2 → 1)

**Tempo Estimado**: 45 minutos

**O que fazer**:

1. **Criar** `core/events/event_bus.py`:

```python
# core/events/event_bus.py

"""
Event Bus centralizado para comunicação entre módulos.
Implementação in-memory com suporte a async handlers.
"""

import asyncio
from typing import Dict, List, Callable, Any, Coroutine
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Base class for all domain events"""
    name: str
    data: Dict[str, Any]
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            import time
            self.timestamp = time.time()

class EventBus:
    """Central event bus for inter-module communication"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """Register handler for event"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.info(f"Handler registered for event: {event_name}")
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unregister handler"""
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
    
    async def publish(self, event: Event) -> None:
        """Publish event to all subscribers"""
        self._event_history.append(event)
        
        handlers = self._handlers.get(event.name, [])
        if not handlers:
            logger.warning(f"No handlers for event: {event.name}")
            return
        
        # Run all handlers concurrently
        tasks = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(event))
            else:
                # Wrap sync handlers
                tasks.append(asyncio.to_thread(handler, event))
        
        try:
            await asyncio.gather(*tasks)
            logger.info(f"Event published: {event.name} to {len(handlers)} handlers")
        except Exception as e:
            logger.error(f"Error publishing event {event.name}: {e}")
            raise
    
    def get_history(self, event_name: str = None) -> List[Event]:
        """Get event history (for debugging)"""
        if event_name:
            return [e for e in self._event_history if e.name == event_name]
        return self._event_history

# Global instance
_event_bus_instance: EventBus = EventBus()

def get_event_bus() -> EventBus:
    """Factory for event bus"""
    return _event_bus_instance

# Exportar
event_bus = get_event_bus()

__all__ = ["Event", "EventBus", "get_event_bus", "event_bus"]
```

2. **Criar** `core/events/decorators.py`:

```python
# core/events/decorators.py

"""Event handler decorators"""

from .event_bus import event_bus
import logging

logger = logging.getLogger(__name__)

def event_handler(event_name: str):
    """Decorator to register event handler"""
    def decorator(func):
        event_bus.subscribe(event_name, func)
        logger.info(f"Event handler registered: {event_name} -> {func.__name__}")
        return func
    return decorator

__all__ = ["event_handler"]
```

3. **Deletar** os 2 antigos:

```bash
rm modules/taxpayer/application/ports/event_bus_port.py
rm app/modules/service_requests/application/ports/event_bus_port.py
```

4. **Redirecionar** imports:

```bash
# Encontrar
grep -r "event_bus_port\|EventBusPort" . --include="*.py" | grep -v ".venv"

# Substituir
find . -name "*.py" -exec sed -i \
  's|from.*event_bus_port|from core.events|g' {} \;

find . -name "*.py" -exec sed -i \
  's|EventBusPort|event_bus|g' {} \;
```

**Validação**:
```bash
python3 -c "from core.events import event_bus; print('✅ EventBus import OK')"
```

---

### TASK 1.4: Criar core/dependencies.py

**Tempo Estimado**: 20 minutos

**O que fazer**:

Centralizar todas as FastAPI dependencies:

```python
# core/dependencies.py

"""FastAPI dependency injection centralized"""

from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import AsyncSessionLocal
from core.security.auth import verify_jwt_token
from modules.identity.models import User
import logging

logger = logging.getLogger(__name__)

async def get_db() -> Generator[AsyncSession, None, None]:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()

async def get_current_user(
    token: str = Depends(...),  # Extract from header
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        user_data = verify_jwt_token(token)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        # Fetch user from DB
        from sqlalchemy import select
        stmt = select(User).where(User.id == user_data.get("user_id"))
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication"
        )

__all__ = ["get_db", "get_current_user"]
```

---

### TASK 1.5: Testes e Validação

**Tempo Estimado**: 30 minutos

**Executar**:

```bash
# 1. Tests
pytest tests/unit -v

# 2. Startup
source .venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
sleep 5

# 3. Health check
curl http://localhost:8000/docs

# 4. Kill server
pkill -f uvicorn

# 5. Check imports
python3 << 'EOF'
from core.security import iam_client
from core.events import event_bus, event_handler
from core.dependencies import get_db, get_current_user
print("✅ All imports OK")
EOF

# 6. Commit
git add .
git commit -m "feat(core): consolidate core infrastructure (iam_client, event_bus, dependencies)"
git push origin feature/refactor-phase-1-core
```

---

## ✅ Checklist FASE 1

- [ ] TASK 1.1: Estrutura core/ criada
- [ ] TASK 1.2: IAM client consolidado
- [ ] TASK 1.3: EventBus consolidado
- [ ] TASK 1.4: Dependencies centralizadas
- [ ] TASK 1.5: Testes passando 100%
- [ ] PR aberto e revisado
- [ ] Merge em develop
- [ ] Tag: `v1.0.0-refactor-phase-1-complete`

---

## 🎯 Após FASE 1

**Se tudo correr bem** (prognóstico: 99% confiança):

1. ✅ Core centralizado funcionando
2. ✅ IAM consolidado (4 → 1)
3. ✅ EventBus global pronto
4. ✅ Dependencies em um ponto
5. ✅ Testes 100%

**Então**: Prosseguir FASE 2 (Padronizar Módulos)

---

## 🆘 Se Algo Quebrar

**Plano de Recuperação Rápida**:

```bash
# Rollback Imediato
git revert HEAD --no-edit
git push origin feature/refactor-phase-1-core

# Ou reset ao commit anterior
git reset --hard HEAD~1
git push -f origin feature/refactor-phase-1-core
```

**Debug**:
```bash
# Ver imports
python3 -m py_compile core/**/*.py

# Verificar syntax
python3 -m pylint core/

# Tests apenas core
pytest tests/unit/test_core -v
```

---

## 📞 Support

Se tiver dúvidas sobre qualquer TASK:

1. Lê o documento correlacionado
2. Segue os scripts exatamente
3. Valida com comandos provided
4. Commit apenas quando validado

---

## 🚀 Start

**Começar agora**:

```bash
cd /home/dev03wsl/sila-system/apps/backend
git checkout -b feature/refactor-phase-1-core
git pull origin develop

# TASK 1.1
mkdir -p core/{config,db,security,integrations,events,dependencies,exceptions,logging}
# ... etc
```

**Timeline**: 1-3 dias  
**Confiança**: 99%  
**Status**: Ready to go! 🚀

---

_SILA System - Refactoring Fase 1_  
_"Consolidação Base para Sucesso Futuro"_
