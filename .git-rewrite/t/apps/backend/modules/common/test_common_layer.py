"""
Test script to verify the common layer functionality.
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the current directory to Python path for modules import
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def test_exceptions():
    """Test common exceptions."""
    print("Testing exceptions...")

    try:
        from modules.common.exceptions import (
            ResourceNotFoundError,
            handle_sila_error,
        )

        # Test exception creation
        error = ResourceNotFoundError("User", "123")
        assert error.code == "resource_not_found"
        assert "User not found" in error.message

        # Test HTTP conversion
        http_error = handle_sila_error(error)
        assert http_error.status_code == 404

        print("✅ Exceptions test passed")

    except Exception as e:
        print(f"❌ Exceptions test failed: {e}")
        return False

    return True


def test_bases():
    """Test base models and schemas."""
    print("Testing bases...")

    try:
        pass

        from modules.common.bases import (
            BaseListResponse,
            BaseSchema,
        )

        # Test base schema
        class TestSchema(BaseSchema):
            name: str

        schema = TestSchema(name="test")
        assert schema.name == "test"

        # Test list response
        items = [{"id": 1}, {"id": 2}]
        response = BaseListResponse.create(items, 2, 1, 10)
        assert response.total == 2
        assert response.page == 1
        assert len(response.items) == 2

        print("✅ Bases test passed")

    except Exception as e:
        print(f"❌ Bases test failed: {e}")
        return False

    return True


def test_utils():
    """Test utility functions."""
    print("Testing utils...")

    try:
        from modules.common.utils import (
            clean_document_number,
            generate_slug,
            hash_password,
            safe_float,
            safe_int,
            validate_email,
            validate_nif,
            verify_password,
        )

        # Test validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False

        # Test NIF validation
        assert validate_nif("12345678901") == True
        assert validate_nif("123") == False

        # Test slug generation
        slug = generate_slug("Test User Name")
        assert slug == "test-user-name"

        # Test password hashing
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) == True
        assert verify_password("wrong", hashed) == False

        # Test document cleaning
        clean = clean_document_number("00.123.456/AB-CD")
        assert clean == "00123456ABCD"

        # Test safe conversions
        assert safe_int("123") == 123
        assert safe_int("invalid") == 0
        assert safe_float("12.34") == 12.34
        assert safe_float("invalid") == 0.0

        print("✅ Utils test passed")

    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

    return True


def test_integration():
    """Test integration between components."""
    print("Testing integration...")

    try:
        from modules.common.bases import BaseCreateSchema
        from modules.common.exceptions import ValidationError
        from modules.common.utils import validate_email

        # Test integrated usage
        class UserCreate(BaseCreateSchema):
            email: str
            name: str

            def validate(self):
                if not validate_email(self.email):
                    raise ValidationError("Invalid email format", "email")

        user = UserCreate(email="test@example.com", name="Test User")
        user.validate()  # Should not raise exception

        # Test invalid case
        try:
            invalid_user = UserCreate(email="invalid", name="Test")
            invalid_user.validate()
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass  # Expected

        print("✅ Integration test passed")

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("🧪 Testing Common Layer Implementation")
    print("=" * 50)

    tests = [test_exceptions, test_bases, test_utils, test_integration]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
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
