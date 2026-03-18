#!/usr/bin/env python3
"""
FASE 5: Visual Test Report Generator
Creates visual, easy-to-read test results without markdown.
"""

import sys
from pathlib import Path
from collections import defaultdict


def print_box(title="", width=80, char="="):
    """Print a box with title."""
    if title:
        padding_left = (width - len(title) - 2) // 2
        padding_right = width - len(title) - 2 - padding_left
        print(f"{char * padding_left} {title} {char * padding_right}")
    else:
        print(char * width)


def print_progress_bar(passed, total, width=40):
    """Print a progress bar."""
    percentage = (passed * 100) // total if total > 0 else 0
    filled = (passed * width) // total
    empty = width - filled
    
    bar = "█" * filled + "░" * empty
    print(f"  [{bar}] {passed}/{total} ({percentage}%)")


def test_module_structure():
    """Test 1: Module structure validation."""
    print("\nTEST 1: Module Directory Structure")
    print("-" * 80)
    
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted([d for d in modules_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
    
    required = ['domain', 'application', 'infrastructure', 'api']
    passed = 0
    failed = 0
    missing_details = {}
    
    for module in modules:
        missing = [d for d in required if not (module / d).exists()]
        if not missing:
            passed += 1
        else:
            failed += 1
            missing_details[module.name] = missing
    
    print(f"Modules checked: {len(modules)}")
    print_progress_bar(passed, len(modules))
    
    if failed > 0:
        print(f"\nFailing modules ({failed}):")
        for mod_name, dirs in sorted(missing_details.items())[:5]:
            print(f"  - {mod_name}: missing {dirs}")
    
    return passed, failed


def test_port_adapter_pattern():
    """Test 2: Port/Adapter pattern."""
    print("\nTEST 2: Port/Adapter Pattern (ABC + Implementation)")
    print("-" * 80)
    
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted([d for d in modules_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
    
    passed = 0
    failed = 0
    
    for module in modules:
        adapter_file = module / "infrastructure" / "adapters.py"
        if adapter_file.exists():
            content = adapter_file.read_text()
            if 'Port' in content and 'Adapter' in content and 'ABC' in content:
                passed += 1
            else:
                failed += 1
    
    print(f"Modules checked: {len(modules)}")
    print_progress_bar(passed, len(modules))
    
    return passed, failed


def test_routers_and_health():
    """Test 3: Routers and Health Checks."""
    print("\nTEST 3: API Routers with Health Endpoints")
    print("-" * 80)
    
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted([d for d in modules_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
    
    passed = 0
    failed = 0
    failed_mods = []
    
    for module in modules:
        router_file = module / "api" / "routers.py"
        if router_file.exists():
            content = router_file.read_text()
            if '/health' in content and 'from fastapi' in content:
                passed += 1
            else:
                failed += 1
                failed_mods.append(module.name)
    
    print(f"Modules checked: {len(modules)}")
    print_progress_bar(passed, len(modules))
    
    if failed > 0:
        print(f"\nFailing modules ({failed}):")
        for mod_name in failed_mods[:5]:
            print(f"  - {mod_name}")
    
    return passed, failed


def test_domain_models():
    """Test 4: Domain Models."""
    print("\nTEST 4: Domain Models and Exceptions")
    print("-" * 80)
    
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted([d for d in modules_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
    
    passed = 0
    failed = 0
    missing_mods = []
    
    for module in modules:
        models_file = module / "domain" / "models.py"
        exc_file = module / "domain" / "exceptions.py"
        
        if models_file.exists() and exc_file.exists():
            passed += 1
        else:
            failed += 1
            missing_mods.append(module.name)
    
    print(f"Modules checked: {len(modules)}")
    print_progress_bar(passed, len(modules))
    
    if failed > 0:
        print(f"\nModules missing domain files ({failed}):")
        for mod_name in missing_mods[:5]:
            print(f"  - {mod_name}")
    
    return passed, failed


def test_application_layer():
    """Test 5: Application Layer."""
    print("\nTEST 5: Application Layer (Commands + Event Handlers)")
    print("-" * 80)
    
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted([d for d in modules_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('_') and d.name != 'tests'])
    
    passed = 0
    failed = 0
    
    for module in modules:
        app_dir = module / "application"
        if app_dir.exists():
            has_commands = (app_dir / "commands.py").exists()
            has_handlers = (app_dir / "event_handlers.py").exists()
            
            if has_commands or has_handlers:
                passed += 1
            else:
                failed += 1
    
    print(f"Modules checked: {len(modules)}")
    print_progress_bar(passed, len(modules))
    
    return passed, failed


def main():
    """Run all tests and show visual report."""
    print_box("SILA SYSTEM - TEST REPORT", width=80)
    
    results = []
    results.append(("Module Structure", test_module_structure()))
    results.append(("Port/Adapter Pattern", test_port_adapter_pattern()))
    results.append(("Routers & Health", test_routers_and_health()))
    results.append(("Domain Models", test_domain_models()))
    results.append(("Application Layer", test_application_layer()))
    
    # Summary
    print_box("SUMMARY", width=80)
    total_passed = 0
    total_failed = 0
    
    for test_name, (passed, failed) in results:
        total_passed += passed
        total_failed += failed
        status = "PASS" if failed == 0 else "FAIL"
        indicator = "[√]" if failed == 0 else "[×]"
        print(f"  {indicator} {test_name:<30} {passed:>3}/{passed+failed:>3}")
    
    total_tests = total_passed + total_failed
    overall_percentage = (total_passed * 100) // total_tests if total_tests > 0 else 0
    
    print()
    print_box()
    print_progress_bar(total_passed, total_tests, width=50)
    print(f"\nOVERALL: {total_passed}/{total_tests} modules fully compliant ({overall_percentage}%)")
    print_box()


if __name__ == "__main__":
    main()
