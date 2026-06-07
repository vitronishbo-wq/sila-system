TEMPLATE = """class {{ module_name_camel }}Exception(Exception):
    # Base exception for the module
    pass

class EntityNotFound({{ module_name_camel }}Exception):
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        super().__init__(f"Entity with ID {entity_id} not found")
"""

__all__ = ["TEMPLATE"]
