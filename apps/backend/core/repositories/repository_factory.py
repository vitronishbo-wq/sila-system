"""
RepositoryFactory - Generate repository interface classes
Consolidates 28 repositories.py files (P1 Phase)

Pattern:
  IModuleName + Repository (base interface)
  With CRUD methods: find_all, find_by_id, save, delete, exists
"""
from abc import ABC, abstractmethod
from typing import Dict, Type, Generic, TypeVar, List, Optional, Any

T = TypeVar('T')


class RepositoryFactory:
    """Factory for generating repository interface classes"""
    
    @staticmethod
    def create_repository_interface(module_name: str) -> Type:
        """
        Create a standardized repository interface for a module.
        
        Args:
            module_name: Name of the module (e.g., 'Documents', 'Payment')
        
        Returns:
            Repository interface class with CRUD operations
        """
        
        class_name = f'I{module_name}Repository'
        
        class RepositoryInterface(ABC, Generic[T]):
            """Standardized repository interface for CRUD operations"""
            
            @abstractmethod
            async def find_all(self) -> List[T]:
                """Find all entities"""
                pass
            
            @abstractmethod
            async def find_by_id(self, id: Any) -> Optional[T]:
                """Find entity by ID"""
                pass
            
            @abstractmethod
            async def save(self, entity: T) -> T:
                """Save or update entity"""
                pass
            
            @abstractmethod
            async def delete(self, id: Any) -> bool:
                """Delete entity"""
                pass
            
            @abstractmethod
            async def exists(self, id: Any) -> bool:
                """Check if entity exists"""
                pass
        
        # Set proper class name and docstring
        RepositoryInterface.__name__ = class_name
        RepositoryInterface.__qualname__ = class_name
        RepositoryInterface.__doc__ = f'Repository interface for {module_name}'
        
        return RepositoryInterface
    
    @staticmethod
    def create_multiple_interfaces(module_names: List[str]) -> Dict[str, Type]:
        """
        Create repository interfaces for multiple modules.
        
        Args:
            module_names: List of module names
        
        Returns:
            Dictionary of {interface_name: interface_class}
        """
        return {
            f'I{name}Repository': RepositoryFactory.create_repository_interface(name)
            for name in module_names
        }


__all__ = ["RepositoryFactory"]
