#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legacy Script Deprecation Wrapper

This script provides backward compatibility for deprecated scaffolding scripts.
It redirects calls to the new unified generate_module.py script.

DEPRECATED: Use 'python tools/codegen/generate_module.py' instead
"""

import sys
import os
from pathlib import Path

def main():
    """Main entry point for deprecated scripts."""
    script_name = Path(sys.argv[0]).name

    print("⚠️  DEPRECATED SCRIPT WARNING"    print(f"   The script '{script_name}' has been deprecated.")
    print("   Please use the new unified generator instead:"    print()
    print("   🔧 NEW USAGE:"    print("   python tools/codegen/generate_module.py [command] [options]")
    print()
    print("   📖 EXAMPLES:"    print("   # Generate a complete module")
    print("   python tools/codegen/generate_module.py module health --title 'Health Services'")
    print()
    print("   # Generate a single service")
    print("   python tools/codegen/generate_module.py service health AgendamentoConsulta \\")
    print("       'Agendamento de Consulta' 'Medical Appointment'")
    print()
    print("   # Generate services from CSV")
    print("   python tools/codegen/generate_module.py batch --csv services.csv")
    print()
    print("   # Generate default services")
    print("   python tools/codegen/generate_module.py batch --default")
    print()
    print("   📚 See 'python tools/codegen/generate_module.py --help' for full documentation")
    print()

    # Map old script names to new commands
    command_map = {
        'add_new_service.py': 'module',
        'batch_generate_services.py': 'batch',
        'create_service.py': 'service',
        'generate_service.py': 'service'
    }

    if script_name in command_map:
        new_command = command_map[script_name]
        print(f"   💡 For '{script_name}', use command: {new_command}")
    else:
        print("   💡 Use 'python tools/codegen/generate_module.py --help' to see all available commands")

    print()
    print("   🔄 This script will be removed in a future version.")
    print("   Please update your automation scripts and documentation.")

    sys.exit(1)

if __name__ == "__main__":
    main()
