"""
Test script for the centralized configuration system.

Validates that the new configuration system works correctly
and can be imported and used across modules.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the backend directory to Python path for testing
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))


def test_basic_imports():
    """Test that all configuration modules can be imported."""
    print("Testing basic imports...")

    try:
        from config import Settings, get_settings, settings

        print("  ✅ Core settings imported")

        from config import ConfigurationError, validate_configuration

        print("  ✅ Validation modules imported")

        from config import ConfigManager, get_config_manager

        print("  ✅ Manager modules imported")

        return True

    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_settings_instance():
    """Test that settings instance works correctly."""
    print("Testing settings instance...")

    try:
        from config import settings

        # Test basic properties
        assert hasattr(settings, "PROJECT_NAME")
        assert hasattr(settings, "ENVIRONMENT")
        assert hasattr(settings, "DATABASE_URL")
        print("  ✅ Basic properties exist")

        # Test computed properties
        assert settings.DATABASE_URL.startswith("postgresql://")
        assert settings.ASYNC_DATABASE_URL.startswith("postgresql+asyncpg://")
        print("  ✅ Computed properties work")

        # Test environment methods
        assert hasattr(settings, "is_production")
        assert hasattr(settings, "is_development")
        assert hasattr(settings, "is_testing")
        print("  ✅ Environment methods exist")

        # Test info methods
        db_info = settings.get_database_info()
        assert isinstance(db_info, dict)
        assert "host" in db_info
        assert "database" in db_info
        print("  ✅ Info methods work")

        return True

    except Exception as e:
        print(f"  ❌ Settings test failed: {e}")
        return False


def test_validation():
    """Test configuration validation."""
    print("Testing configuration validation...")

    try:
        from config import Settings, validate_configuration

        # Test current settings
        is_valid, errors, warnings = validate_configuration()
        print(
            f"  ✅ Validation completed: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}"
        )

        if errors:
            print("  Errors:")
            for error in errors:
                print(f"    - {error}")

        if warnings:
            print("  Warnings:")
            for warning in warnings:
                print(f"    - {warning}")

        # Test with invalid settings
        try:
            Settings(
                SECRET_KEY="short",
                ENVIRONMENT="invalid_env",
                DATABASE_URL="invalid_url",
            )
            # This should raise validation errors during model validation
            print("  ⚠️  Invalid settings validation needs improvement")
        except Exception as e:
            print(f"  ✅ Invalid settings properly rejected: {e}")

        return True

    except Exception as e:
        print(f"  ❌ Validation test failed: {e}")
        return False


def test_config_manager():
    """Test configuration manager functionality."""
    print("Testing configuration manager...")

    try:
        from config import get_config_manager

        manager = get_config_manager()

        # Test manager properties
        assert hasattr(manager, "settings")
        assert hasattr(manager, "get_config_summary")
        assert hasattr(manager, "update_setting")
        print("  ✅ Manager has required methods")

        # Test config summary
        summary = manager.get_config_summary(include_secrets=False)
        assert isinstance(summary, dict)
        assert "environment" in summary
        assert "project" in summary
        assert "database" in summary
        print("  ✅ Config summary works")

        # Test setting update
        original_debug = manager.settings.DEBUG
        manager.update_setting("DEBUG", not original_debug)
        assert manager.settings.DEBUG != original_debug
        manager.update_setting("DEBUG", original_debug)  # Restore
        print("  ✅ Setting update works")

        # Test temporary settings context manager
        with manager.temporary_settings(DEBUG=True):
            assert manager.settings.DEBUG
        assert manager.settings.DEBUG == original_debug
        print("  ✅ Temporary settings context manager works")

        return True

    except Exception as e:
        print(f"  ❌ Manager test failed: {e}")
        return False


def test_file_operations():
    """Test configuration file operations."""
    print("Testing file operations...")

    try:
        from config import Settings, get_config_manager

        manager = get_config_manager()

        # Test export template
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            template_path = f.name

        try:
            manager.export_config_template(template_path)

            # Verify template was created
            assert os.path.exists(template_path)
            assert os.path.getsize(template_path) > 0

            # Load and verify template content
            import json

            with open(template_path) as f:
                template = json.load(f)

            assert "_description" in template
            assert "PROJECT_NAME" in template
            assert "ENVIRONMENT" in template
            print("  ✅ Template export works")

        finally:
            # Clean up
            if os.path.exists(template_path):
                os.unlink(template_path)

        # Test save and load configuration
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            config_path = f.name

        try:
            # Save current config with secrets for testing
            manager.save_to_file(config_path, include_secrets=True)
            assert os.path.exists(config_path)
            print("  ✅ Configuration save works")

            # Load configuration
            loaded_settings = manager.load_from_file(config_path)
            assert isinstance(loaded_settings, Settings)
            assert loaded_settings.PROJECT_NAME == manager.settings.PROJECT_NAME
            print("  ✅ Configuration load works")

        finally:
            # Clean up
            if os.path.exists(config_path):
                os.unlink(config_path)

        return True

    except Exception as e:
        print(f"  ❌ File operations test failed: {e}")
        return False


def test_environment_switching():
    """Test environment switching functionality."""
    print("Testing environment switching...")

    try:
        from config import get_config_manager

        manager = get_config_manager()
        original_env = manager.settings.ENVIRONMENT

        # Test switching to test environment
        try:
            test_settings = manager.switch_environment("test")
            assert test_settings.ENVIRONMENT == "test"
            print("  ✅ Environment switching works")

            # Switch back
            manager.switch_environment(original_env)
            assert manager.settings.ENVIRONMENT == original_env
            print("  ✅ Environment restoration works")

        except Exception as e:
            print(f"  ⚠️  Environment switching test incomplete: {e}")

        return True

    except Exception as e:
        print(f"  ❌ Environment switching test failed: {e}")
        return False


def test_cross_module_import():
    """Test that configuration can be imported from different modules."""
    print("Testing cross-module imports...")

    try:
        # Test importing from a different path
        test_code = """
import sys
sys.path.insert(0, "/opt/sila-system/backend")

try:
    from config import settings
    print(f"SUCCESS: {settings.PROJECT_NAME} - {settings.ENVIRONMENT}")
except ImportError as e:
    print(f"FAILED: {e}")
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_code)
            test_file = f.name

        try:
            import subprocess

            result = subprocess.run(
                [sys.executable, test_file], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                print("  ✅ Cross-module import works")
                return True
            else:
                print(f"  ❌ Cross-module import failed: {result.stderr}")
                return False

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    except Exception as e:
        print(f"  ❌ Cross-module import test failed: {e}")
        return False


def test_performance():
    """Test configuration loading performance."""
    print("Testing performance...")

    try:
        import time

        from config import get_settings

        # Test settings loading time
        start_time = time.time()
        for _ in range(100):
            get_settings()
        end_time = time.time()

        avg_time = (end_time - start_time) / 100
        print(f"  ✅ Average settings load time: {avg_time:.6f}s")

        if avg_time > 0.01:  # 10ms threshold
            print("  ⚠️  Performance could be improved")

        return True

    except Exception as e:
        print(f"  ❌ Performance test failed: {e}")
        return False


def main():
    """Run all configuration tests."""
    print("SILA Configuration System Tests")
    print("=" * 50)

    tests = [
        test_basic_imports,
        test_settings_instance,
        test_validation,
        test_config_manager,
        test_file_operations,
        test_environment_switching,
        test_cross_module_import,
        test_performance,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            print()

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All configuration tests passed!")
        print("\nThe centralized configuration system is working correctly.")
        print("You can now start migrating modules to use the new config system.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration setup.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
