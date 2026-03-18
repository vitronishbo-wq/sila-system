"""
AdapterFactory - Generate adapter/port classes
Consolidates 30 adapters.py files (P1 Phase)

Pattern:
  ModuleNameAdapter (implements multiple service ports)
  With methods for: create, read, update, delete, query operations
"""
from abc import ABC, abstractmethod
from typing import Dict, Type, List, Optional, Any


class AdapterFactory:
    """Factory for generating adapter/port implementation classes"""
    
    @staticmethod
    def create_adapter_base(module_name: str, service_ports: List[Type] = None) -> Type:
        """
        Create a standardized adapter base class for a module.
        
        Args:
            module_name: Name of the module (e.g., 'Documents', 'Payment')
            service_ports: List of port/interface classes to implement
        
        Returns:
            Adapter base class
        """
        
        class_name = f'{module_name}Adapter'
        base_classes = service_ports or (ABC,)
        if ABC not in base_classes:
            base_classes = (ABC,) + tuple(base_classes)
        
        class AdapterBase(ABC):
            """Base adapter for service integration"""
            
            def __init__(self):
                """Initialize adapter"""
                self.module_name = module_name
            
            @abstractmethod
            async def connect(self) -> bool:
                """Connect to external service"""
                pass
            
            @abstractmethod
            async def disconnect(self) -> bool:
                """Disconnect from external service"""
                pass
            
            @abstractmethod
            async def health_check(self) -> Dict[str, Any]:
                """Check adapter health status"""
                pass
        
        # Set proper class name
        AdapterBase.__name__ = class_name
        AdapterBase.__qualname__ = class_name
        AdapterBase.__doc__ = f'Adapter for {module_name} service integration'
        
        return AdapterBase
    
    @staticmethod
    def create_infrastructure_adapter(
        module_name: str, 
        repository_interface: Type,
        domain_model: Type = None
    ) -> Type:
        """
        Create infrastructure adapter implementing repository pattern.
        
        Args:
            module_name: Module name
            repository_interface: Repository interface to implement
            domain_model: Domain model class
        
        Returns:
            Infrastructure adapter class
        """
        
        class_name = f'Infrastructure{module_name}Adapter'
        
        class InfrastructureAdapter(repository_interface):
            """Infrastructure adapter implementing repository pattern"""
            
            def __init__(self, db_session=None):
                """Initialize infrastructure adapter with database session"""
                self.db_session = db_session
                self.module_name = module_name
            
            async def connect(self) -> bool:
                """Connect to database"""
                return self.db_session is not None
            
            async def disconnect(self) -> bool:
                """Disconnect from database"""
                if self.db_session:
                    await self.db_session.close()
                    return True
                return False
            
            async def health_check(self) -> Dict[str, Any]:
                """Check database connectivity"""
                try:
                    connected = await self.connect()
                    return {
                        "status": "healthy" if connected else "disconnected",
                        "module": self.module_name,
                    }
                except Exception as e:
                    return {"status": "error", "error": str(e)}
        
        # Set proper class name
        InfrastructureAdapter.__name__ = class_name
        InfrastructureAdapter.__qualname__ = class_name
        
        return InfrastructureAdapter
    
    @staticmethod
    def create_multiple_adapters(
        module_names: List[str],
        repository_interfaces: Dict[str, Type]
    ) -> Dict[str, Type]:
        """
        Create adapters for multiple modules.
        
        Args:
            module_names: List of module names
            repository_interfaces: Dict of {module: repository_interface}
        
        Returns:
            Dictionary of {adapter_name: adapter_class}
        """
        adapters = {}
        for module_name in module_names:
            repo_interface = repository_interfaces.get(f'I{module_name}Repository')
            adapter_class = AdapterFactory.create_infrastructure_adapter(
                module_name,
                repo_interface
            )
            adapters[f'{module_name}Adapter'] = adapter_class
        
        return adapters


__all__ = ["AdapterFactory"]
