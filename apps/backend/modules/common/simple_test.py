"""
Simple test to verify the common layer structure and basic functionality.
"""

import os
import sys


def test_file_structure():
    """Test that all required files exist."""
    print("Testing file structure...")

    base_path = "/opt/sila-system/backend/modules/common"

    required_files = [
        "__init__.py",
        "exceptions/__init__.py",
        "exceptions/exceptions.py",
        "bases/__init__.py",
        "bases/bases.py",
        "utils/__init__.py",
        "utils/utils.py",
        "examples.py",
        "README_COMMON_LAYER.md",
    ]

    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False

    print("✅ All required files exist")
    return True


def test_imports():
    """Test that imports work correctly."""
    print("Testing imports...")

    try:
        # Test basic Python imports without external dependencies
        import importlib.util

        base_path = "/opt/sila-system/backend/modules/common"

        # Test exceptions module
        spec = importlib.util.spec_from_file_location(
            "exceptions", os.path.join(base_path, "exceptions/exceptions.py")
        )
        exceptions_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exceptions_module)

        # Test that SILAError class exists
        assert hasattr(exceptions_module, "SILAError")
        assert hasattr(exceptions_module, "ResourceNotFoundError")

        # Test bases module
        spec = importlib.util.spec_from_file_location(
            "bases", os.path.join(base_path, "bases/bases.py")
        )
        bases_module = importlib.util.module_from_spec(spec)

        # Test utils module (without external dependencies)
        spec = importlib.util.spec_from_file_location(
            "utils", os.path.join(base_path, "utils/utils.py")
        )
        utils_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils_module)

        # Test that utility functions exist
        assert hasattr(utils_module, "validate_email")
        assert hasattr(utils_module, "generate_slug")
        assert hasattr(utils_module, "clean_document_number")

        print("✅ All imports work correctly")
        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    print("Testing basic functionality...")

    try:
        import importlib.util

        # Load utils module
        base_path = "/opt/sila-system/backend/modules/common"
        spec = importlib.util.spec_from_file_location(
            "utils", os.path.join(base_path, "utils/utils.py")
        )
        utils_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils_module)

        # Test email validation
        assert utils_module.validate_email("test@example.com") == True
        assert utils_module.validate_email("invalid-email") == False

        # Test slug generation
        slug = utils_module.generate_slug("Test User Name")
        assert slug == "test-user-name"

        # Test document cleaning
        clean = utils_module.clean_document_number("00.123.456/AB-CD")
        assert clean == "00123456ABCD"

        # Test safe conversions
        assert utils_module.safe_int("123") == 123
        assert utils_module.safe_int("invalid") == 0
        assert utils_module.safe_float("12.34") == 12.34
        assert utils_module.safe_float("invalid") == 0.0

        print("✅ Basic functionality works correctly")
        return True

    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_exception_functionality():
    """Test exception functionality."""
    print("Testing exception functionality...")

    try:
        import importlib.util

        # Load exceptions module
        base_path = "/opt/sila-system/backend/modules/common"
        spec = importlib.util.spec_from_file_location(
            "exceptions", os.path.join(base_path, "exceptions/exceptions.py")
        )
        exceptions_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exceptions_module)

        # Test exception creation
        error = exceptions_module.ResourceNotFoundError("User", "123")
        assert error.code == "resource_not_found"
        assert "User not found" in error.message
        assert error.details["resource_type"] == "User"
        assert error.details["resource_id"] == "123"

        # Test validation error
        validation_error = exceptions_module.ValidationError("Invalid format", "email")
        assert validation_error.code == "validation_error"
        assert validation_error.details["field"] == "email"

        print("✅ Exception functionality works correctly")
        return True

    except Exception as e:
        print(f"❌ Exception functionality test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Common Layer Implementation (Simple Version)")
    print("=" * 60)

    tests = [
        test_file_structure,
        test_imports,
        test_basic_functionality,
        test_exception_functionality,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Common layer is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
