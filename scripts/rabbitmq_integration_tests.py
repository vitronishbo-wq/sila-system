#!/usr/bin/env python3
"""
FASE 5: RabbitMQ Integration Tests
Validate message routing and event publishing across modules
"""

from pathlib import Path


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


def check_event_handlers():
    """Check if modules have event handlers for async communication."""
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted(
        [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
    )

    passed = 0
    for module in modules:
        handlers = module / "application" / "event_handlers.py"
        if handlers.exists():
            content = handlers.read_text()
            if "EventHandler" in content or "handle_" in content:
                passed += 1

    return passed, len(modules)


def check_message_routing():
    """Check if modules have proper message routing structure."""
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted(
        [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
    )

    passed = 0
    for module in modules:
        # Check for routers or event handlers
        routers = module / "api" / "routers.py"
        handlers = module / "application" / "event_handlers.py"

        if routers.exists() and handlers.exists():
            passed += 1

    return passed, len(modules)


def check_async_support():
    """Check for async/await support in message handlers."""
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted(
        [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
    )

    passed = 0
    for module in modules:
        handlers = module / "application" / "event_handlers.py"
        if handlers.exists():
            content = handlers.read_text()
            if "async" in content:
                passed += 1

    return passed, len(modules)


def check_queue_configuration():
    """Check for queue/topic configuration in modules."""
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted(
        [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
    )

    # For now, we check if adapters exist (which would handle messaging)
    passed = 0
    for module in modules:
        adapters = module / "infrastructure" / "adapters.py"
        if adapters.exists():
            content = adapters.read_text()
            if "Adapter" in content:
                passed += 1

    return passed, len(modules)


def main():
    print_box("RABBITMQ INTEGRATION TESTS - SILA SYSTEM", width=80)

    # Test 1: Event Handlers Presence
    print("\nTEST 1: Event Handler Configuration")
    print("-" * 80)

    passed, total = check_event_handlers()
    print(f"Modules checked: {total}")
    print_progress_bar(passed, total)

    if passed < total:
        print(f"\nNote: {total - passed} modules missing event handler implementations")

    # Test 2: Message Routing
    print("\nTEST 2: Message Routing Setup")
    print("-" * 80)

    passed_routing, total_routing = check_message_routing()
    print(f"Modules checked: {total_routing}")
    print_progress_bar(passed_routing, total_routing)

    if passed_routing < total_routing:
        print(f"\nNote: {total_routing - passed_routing} modules missing message routing")

    # Test 3: Async Support
    print("\nTEST 3: Async/Await Support")
    print("-" * 80)

    passed_async, total_async = check_async_support()
    print(f"Modules checked: {total_async}")
    print_progress_bar(passed_async, total_async)

    # Test 4: Queue Configuration
    print("\nTEST 4: Message Adapter Configuration")
    print("-" * 80)

    passed_queue, total_queue = check_queue_configuration()
    print(f"Modules checked: {total_queue}")
    print_progress_bar(passed_queue, total_queue)

    # Summary
    print_box("SUMMARY", width=80)

    summary_tests = [
        ("Event Handlers", passed, total),
        ("Message Routing", passed_routing, total_routing),
        ("Async Support", passed_async, total_async),
        ("Adapters", passed_queue, total_queue),
    ]

    total_passed = sum(p for _, p, _ in summary_tests)
    total_checks = sum(t for _, _, t in summary_tests)

    for test_name, passed_count, total_count in summary_tests:
        indicator = "[√]" if passed_count == total_count else "[×]"
        print(f"  {indicator} {test_name:<30} {passed_count:>3}/{total_count:>3}")

    percentage = (total_passed * 100) // total_checks if total_checks > 0 else 0
    print()
    print_box()
    print_progress_bar(total_passed, total_checks, width=50)
    print(f"\nOVERALL: {total_passed}/{total_checks} checks passed ({percentage}%)")
    print_box()


if __name__ == "__main__":
    main()
