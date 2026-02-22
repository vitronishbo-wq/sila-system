"""
Services module endpoints - Compatibility layer.

This file imports the router from controller.py to maintain compatibility
with the automatic router discovery system while using the typed controller.

The controller.py contains all the typed FastAPI routes with proper
response_model and Pydantic schemas following the OpenAPI contract.
"""

# Import the typed router from controller.py
from .controller import router

__all__ = ["router"]
