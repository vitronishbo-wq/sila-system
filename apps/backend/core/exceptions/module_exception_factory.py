"""
ModuleExceptionFactory - Generate module-specific exception classes
Consolidates 181 exceptions.py files (P1 Phase)

Pattern:
  ModuleName + Exception (base)
  ModuleName + NotFound
  ModuleName + ValidationError
  ModuleName + InvalidStateError
"""


class ModuleExceptionFactory:
    """Factory for generating module-specific exception hierarchies"""

    EXCEPTION_TEMPLATES = {
        "NotFound": "Raised when {module} aggregate not found.",
        "ValidationError": "Raised on {module} validation failure.",
        "Unauthorized": "Raised on unauthorized access to {module} resources.",
        "Conflict": "Raised on {module} state conflict.",
        "InvalidState": "Raised on invalid {module} state transition.",
        "InvalidStateError": "Raised on invalid {module} state transition.",
    }

    @staticmethod
    def create_exceptions(module_name: str, base_exception: type = Exception) -> dict[str, type]:
        """
        Auto-generate exception classes for a module.

        Args:
            module_name: Name of the module (e.g., 'Documents', 'Payment', 'Justice')
            base_exception: Base exception class to inherit from (defaults to Exception)

        Returns:
            Dictionary of {exception_name: exception_class}
        """
        exceptions = {}

        # Base module exception
        base_exc_name = f"{module_name}Exception"
        exceptions[base_exc_name] = type(
            base_exc_name,
            (base_exception,),
            {
                "__doc__": f"Base exception for {module_name} domain.",
                "__module__": __name__,
            },
        )

        # Specific exceptions
        for exc_suffix, exc_doc_template in ModuleExceptionFactory.EXCEPTION_TEMPLATES.items():
            exc_name = f"{module_name}{exc_suffix}"
            exc_doc = exc_doc_template.format(module=module_name.lower())

            exceptions[exc_name] = type(
                exc_name,
                (exceptions[base_exc_name],),
                {
                    "__doc__": exc_doc,
                    "__module__": __name__,
                },
            )

        return exceptions

    @staticmethod
    def create_exceptions_with_core_base(
        module_name: str, core_domain_exception: type
    ) -> dict[str, type]:
        """
        Create exceptions inheriting from core DomainException.

        Args:
            module_name: Name of the module
            core_domain_exception: Core DomainException class from core/exceptions/

        Returns:
            Dictionary of {exception_name: exception_class}
        """
        return ModuleExceptionFactory.create_exceptions(
            module_name, base_exception=core_domain_exception
        )


__all__ = ["ModuleExceptionFactory"]
