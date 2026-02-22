"""
Identity Citizen Model - Proxy to Citizenship Module

This module serves as a proxy that imports the unified Citizen model from
the citizenship module to maintain backward compatibility.
"""

from modules.citizenship.models.citizen import Citizen

# Re-export for backward compatibility
__all__ = ["Citizen"]
