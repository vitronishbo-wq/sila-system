#!/usr/bin/env python3
"""
Script to sync services.json between backend and frontend

This script reads the backend/modules_services.json file and generates
a frontend-compatible services.json file for the frontend application.
"""

import json
import os
from pathlib import Path


def sync_services_json():
    """Synchronize services.json between backend and frontend."""

    # Paths
    backend_services_path = (
        Path(__file__).parent.parent / "backend" / "modules_services.json"
    )
    frontend_services_path = (
        Path(__file__).parent.parent
        / "frontend"
        / "webapp"
        / "src"
        / "config"
        / "services.json"
    )

    # Check if backend file exists
    if not backend_services_path.exists():
        print(f"Error: Backend services file not found: {backend_services_path}")
        return False

    # Load backend services
    try:
        with open(backend_services_path, "r", encoding="utf-8") as f:
            backend_services = json.load(f)
    except Exception as e:
        print(f"Error reading backend services file: {e}")
        return False

    # Convert backend format to frontend format
    frontend_services = []

    for module_name, module_data in backend_services.items():
        # Skip modules without services
        if not module_data.get("services"):
            continue

        # Convert each service
        for service in module_data["services"]:
            frontend_service = {
                "id": service.get(
                    "id", f"servico-{module_name}-{len(frontend_services) + 1:02d}"
                ),
                "name": service.get(
                    "name", service.get("display_name", f"Serviço {module_name}")
                ),
                "category": service.get("category", module_name.title()),
                "description": service.get(
                    "description", f"Serviço do módulo {module_name}"
                ),
                "endpoint": service.get("endpoint", f"/api/servicos/{module_name}"),
                "method": service.get("method", "GET"),
                "rolesAllowed": service.get("roles_allowed", ["admin", "cidadao"]),
            }
            frontend_services.append(frontend_service)

    # Ensure frontend directory exists
    frontend_services_path.parent.mkdir(parents=True, exist_ok=True)

    # Write frontend services file
    try:
        with open(frontend_services_path, "w", encoding="utf-8") as f:
            json.dump(frontend_services, f, ensure_ascii=False, indent=2)
        print(f"Successfully synced services to: {frontend_services_path}")
        print(f"Generated {len(frontend_services)} services")
        return True
    except Exception as e:
        print(f"Error writing frontend services file: {e}")
        return False


if __name__ == "__main__":
    success = sync_services_json()
    exit(0 if success else 1)
