#!/usr/bin/env python3
"""
FASE 5: Module Generator
Creates missing domain/api/application/infrastructure files for all modules.
Real code generation, not documentation.
"""

from pathlib import Path
from textwrap import dedent
import sys

class ModuleGenerator:
    def __init__(self, modules_path):
        self.modules_path = Path(modules_path)
    
    def generate_all(self):
        """Generate missing files for all modules."""
        modules = sorted([d for d in self.modules_path.iterdir() 
                         if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
        
        print(f"\n{'='*80}")
        print(f"[GENERATING CODE FOR {len(modules)} MODULES]")
        print(f"{'='*80}\n")
        
        files_created = 0
        for module in modules:
            files_created += self._generate_module(module)
        
        print(f"\n[GENERATED {files_created} FILES]\n")
    
    def _generate_module(self, module_path):
        """Generate missing files for a single module."""
        module_name = module_path.name
        files_created = 0
        
        # Ensure directories exist
        (module_path / "domain").mkdir(exist_ok=True)
        (module_path / "application").mkdir(exist_ok=True)
        (module_path / "infrastructure").mkdir(exist_ok=True)
        (module_path / "api").mkdir(exist_ok=True)
        
        # Generate domain/models.py
        models_file = module_path / "domain" / "models.py"
        if not models_file.exists():
            models_file.write_text(self._template_models(module_name))
            print(f"[OK] {module_name}/domain/models.py")
            files_created += 1
        
        # Generate domain/exceptions.py
        exc_file = module_path / "domain" / "exceptions.py"
        if not exc_file.exists():
            exc_file.write_text(self._template_exceptions(module_name))
            print(f"[OK] {module_name}/domain/exceptions.py")
            files_created += 1
        
        # Generate application/commands.py
        cmd_file = module_path / "application" / "commands.py"
        if not cmd_file.exists():
            cmd_file.write_text(self._template_commands(module_name))
            print(f"[OK] {module_name}/application/commands.py")
            files_created += 1
        
        # Generate application/event_handlers.py
        handlers_file = module_path / "application" / "event_handlers.py"
        if not handlers_file.exists():
            handlers_file.write_text(self._template_event_handlers(module_name))
            print(f"[OK] {module_name}/application/event_handlers.py")
            files_created += 1
        
        # Generate infrastructure/adapters.py
        adapters_file = module_path / "infrastructure" / "adapters.py"
        if not adapters_file.exists():
            adapters_file.write_text(self._template_adapters(module_name))
            print(f"[OK] {module_name}/infrastructure/adapters.py")
            files_created += 1
        
        # Generate infrastructure/repositories.py
        repos_file = module_path / "infrastructure" / "repositories.py"
        if not repos_file.exists():
            repos_file.write_text(self._template_repositories(module_name))
            print(f"[OK] {module_name}/infrastructure/repositories.py")
            files_created += 1
        
        # Generate api/routers.py
        routers_file = module_path / "api" / "routers.py"
        if not routers_file.exists():
            routers_file.write_text(self._template_routers(module_name))
            print(f"[OK] {module_name}/api/routers.py")
            files_created += 1
        
        return files_created
    
    def _template_models(self, module_name):
        return dedent(f'''"""
Domain models for {module_name} module.
"""

from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class {self._capitalize(module_name)}ID:
    """Value object for {module_name} aggregate ID."""
    value: UUID = field(default_factory=uuid4)
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass
class {self._capitalize(module_name)} Aggregate:
    """{self._capitalize(module_name)} aggregate root."""
    id: {self._capitalize(module_name)}ID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if self.id is None:
            object.__setattr__(self, 'id', {self._capitalize(module_name)}ID())
''')
    
    def _template_exceptions(self, module_name):
        return dedent(f'''"""
Domain exceptions for {module_name} module.
"""


class {self._capitalize(module_name)}Exception(Exception):
    """Base exception for {module_name} domain."""
    pass


class {self._capitalize(module_name)}NotFound({self._capitalize(module_name)}Exception):
    """Raised when {module_name} aggregate not found."""
    pass


class {self._capitalize(module_name)}ValidationError({self._capitalize(module_name)}Exception):
    """Raised on {module_name} validation failure."""
    pass


class {self._capitalize(module_name)}InvalidStateError({self._capitalize(module_name)}Exception):
    """Raised on invalid {module_name} state transition."""
    pass
''')
    
    def _template_commands(self, module_name):
        return dedent(f'''"""
Application commands for {module_name} module.
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Create{self._capitalize(module_name)}Command:
    """Command to create a new {module_name}."""
    id: Optional[UUID] = None
    
    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            object.__setattr__(self, 'id', uuid4())


@dataclass
class Update{self._capitalize(module_name)}Command:
    """Command to update a {module_name}."""
    id: UUID
    
    def validate(self) -> None:
        if not self.id:
            raise ValueError("ID required for update")


@dataclass
class Delete{self._capitalize(module_name)}Command:
    """Command to delete a {module_name}."""
    id: UUID
''')
    
    def _template_event_handlers(self, module_name):
        return dedent(f'''"""
Event handlers for {module_name} module.
"""

from typing import Dict, Callable, Any


class {self._capitalize(module_name)}EventHandlers:
    """Handles all events for {module_name} module."""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {{}}
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register all event handlers."""
        # Override in subclass to add handlers
        pass
    
    def handle(self, event_type: str, event_data: Any) -> None:
        """Handle an event if handler exists."""
        if event_type in self.handlers:
            self.handlers[event_type](event_data)


# Global registry
handlers = {self._capitalize(module_name)}EventHandlers()
''')
    
    def _template_adapters(self, module_name):
        return dedent(f'''"""
Infrastructure adapters for {module_name} module.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class {self._capitalize(module_name)}Port(ABC):
    """Port (interface) for {module_name} operations."""
    
    @abstractmethod
    async def get(self, id: str) -> Any:
        """Get {module_name} by ID."""
        pass
    
    @abstractmethod
    async def create(self, data: dict) -> Any:
        """Create new {module_name}."""
        pass
    
    @abstractmethod
    async def update(self, id: str, data: dict) -> Any:
        """Update {module_name}."""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete {module_name}."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all {module_name}."""
        pass


class {self._capitalize(module_name)}Adapter({self._capitalize(module_name)}Port):
    """Adapter (implementation) for {module_name} operations."""
    
    async def get(self, id: str) -> Any:
        """Get {module_name} by ID."""
        return None
    
    async def create(self, data: dict) -> Any:
        """Create new {module_name}."""
        return {{"id": id, **data}}
    
    async def update(self, id: str, data: dict) -> Any:
        """Update {module_name}."""
        return {{"id": id, **data}}
    
    async def delete(self, id: str) -> bool:
        """Delete {module_name}."""
        return True
    
    async def list_all(self) -> List[Any]:
        """List all {module_name}."""
        return []
''')
    
    def _template_repositories(self, module_name):
        return dedent(f'''"""
Repository pattern for {module_name} module.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any


class {self._capitalize(module_name)}Repository(ABC):
    """Abstract repository for {module_name}."""
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get {module_name} by ID."""
        pass
    
    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save {module_name}."""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete {module_name}."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all {module_name}."""
        pass


class {self._capitalize(module_name)}MemoryRepository({self._capitalize(module_name)}Repository):
    """In-memory repository for {module_name}."""
    
    def __init__(self):
        self.data = {{}}
    
    async def get_by_id(self, id: str) -> Optional[Any]:
        return self.data.get(id)
    
    async def save(self, entity: Any) -> Any:
        self.data[entity.id] = entity
        return entity
    
    async def delete(self, id: str) -> bool:
        if id in self.data:
            del self.data[id]
            return True
        return False
    
    async def list_all(self) -> List[Any]:
        return list(self.data.values())
''')
    
    def _template_routers(self, module_name):
        return dedent(f'''"""
API routers for {module_name} module.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID


router = APIRouter(
    prefix="/api/v1/{module_name}",
    tags=["{module_name}"],
    responses={{404: {{"description": "Not found"}}}},
)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check for {module_name} service."""
    return {{"status": "healthy", "service": "{module_name}"}}


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness check for {module_name} service."""
    return {{"ready": True, "service": "{module_name}"}}


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """Liveness check for {module_name} service."""
    return {{"alive": True, "service": "{module_name}"}}


@router.get("", status_code=status.HTTP_200_OK)
async def list_{module_name}():
    """List all {module_name} records."""
    return {{"items": [], "total": 0}}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_{module_name}(data: dict):
    """Create a new {module_name} record."""
    return {{"id": "new-id", **data}}


@router.get("/{{id}}", status_code=status.HTTP_200_OK)
async def get_{module_name}(id: str):
    """Get {module_name} record by ID."""
    return {{"id": id, "name": "{module_name}"}}


@router.put("/{{id}}", status_code=status.HTTP_200_OK)
async def update_{module_name}(id: str, data: dict):
    """Update {module_name} record."""
    return {{"id": id, **data}}


@router.delete("/{{id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{module_name}(id: str):
    """Delete {module_name} record."""
    return None
''')
    
    def _capitalize(self, text: str) -> str:
        """Convert snake_case to PascalCase."""
        return ''.join(word.capitalize() for word in text.split('_'))


if __name__ == "__main__":
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    
    if not modules_path.exists():
        print(f"[ERROR] Modules path not found: {modules_path}")
        sys.exit(1)
    
    generator = ModuleGenerator(modules_path)
    generator.generate_all()
