#!/usr/bin/env python3
"""
Script to sync translations between backend and frontend

This script reads the frontend translation files and ensures backend
translation files are compatible and synchronized.
"""

import json
import os
from pathlib import Path


def merge_dicts(base_dict, overlay_dict):
    """Recursively merge two dictionaries."""
    result = base_dict.copy()

    for key, value in overlay_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def sync_translations():
    """Synchronize translations between backend and frontend."""

    # Paths
    frontend_locales_path = (
        Path(__file__).parent.parent / "frontend" / "webapp" / "src" / "locales"
    )
    backend_translations_path = (
        Path(__file__).parent.parent / "backend" / "translations"
    )

    if not frontend_locales_path.exists():
        print(f"Error: Frontend locales directory not found: {frontend_locales_path}")
        return False

    if not backend_translations_path.exists():
        print(f"Creating backend translations directory: {backend_translations_path}")
        backend_translations_path.mkdir(exist_ok=True)

    # Process each language file in frontend
    for frontend_file in frontend_locales_path.glob("*.json"):
        lang_code = frontend_file.stem  # pt, en, etc.

        # Load frontend translation
        try:
            with open(frontend_file, "r", encoding="utf-8") as f:
                frontend_translations = json.load(f)
        except Exception as e:
            print(f"Error reading frontend translation file {frontend_file}: {e}")
            continue

        # Backend translation file path
        backend_file = backend_translations_path / f"{lang_code}.json"

        # Load or create backend translation
        backend_translations = {}
        if backend_file.exists():
            try:
                with open(backend_file, "r", encoding="utf-8") as f:
                    backend_translations = json.load(f)
            except Exception as e:
                print(f"Error reading backend translation file {backend_file}: {e}")
                backend_translations = {}

        # Merge frontend translations into backend (frontend takes precedence)
        merged_translations = merge_dicts(backend_translations, frontend_translations)

        # Write merged translations back to backend file
        try:
            with open(backend_file, "w", encoding="utf-8") as f:
                json.dump(merged_translations, f, ensure_ascii=False, indent=2)
            print(
                f"Synchronized translations for language '{lang_code}': {backend_file}"
            )
        except Exception as e:
            print(f"Error writing backend translation file {backend_file}: {e}")
            continue

    print("Translation synchronization completed successfully")
    return True


if __name__ == "__main__":
    success = sync_translations()
    exit(0 if success else 1)
