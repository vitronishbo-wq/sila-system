from abc import ABC, abstractmethod


class CivilRegistryPort(ABC):
    @abstractmethod
    def get_civil_registry_record(self, *args, **kwargs):
        raise NotImplementedError


__all__ = ["CivilRegistryPort"]
