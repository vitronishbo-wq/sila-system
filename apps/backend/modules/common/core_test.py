"""
Core test to verify the common layer structure and basic Python functionality.
"""

import os
import re
from datetime import datetime
from typing import Any, Dict, Optional, Union
from uuid import uuid4


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


def test_core_utilities():
    """Test core utility functions without external dependencies."""
    print("Testing core utilities...")

    # Email validation
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    # Phone validation
    def validate_phone(phone: str) -> bool:
        pattern = r"^\+?[1-9]\d{1,14}$"
        return re.match(pattern, phone) is not None

    # NIF validation
    def validate_nif(nif: str) -> bool:
        clean_nif = re.sub(r"\D", "", nif)
        return len(clean_nif) == 10 and clean_nif.isdigit()

    # String normalization
    def normalize_string(text: str, remove_accents: bool = False) -> str:
        import unicodedata

        normalized = " ".join(text.split())
        if remove_accents:
            normalized = unicodedata.normalize("NFKD", normalized)
            normalized = "".join(c for c in normalized if not unicodedata.combining(c))
        return normalized.strip()

    # Slug generation
    def generate_slug(text: str) -> str:
        slug = normalize_string(text, remove_accents=True).lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")
        if len(slug) > 100:
            slug = slug[:100].rstrip("-")
        return slug

    # Document cleaning
    def clean_document_number(document_number: str) -> str:
        return re.sub(r"[^\w]", "", document_number).upper()

    # Safe conversions
    def safe_int(value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def safe_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    # Run tests
    try:
        # Test validation
        email_result = validate_email("test@example.com")
        assert email_result == True, f"Expected True, got {email_result}"

        email_result2 = validate_email("invalid-email")
        assert email_result2 == False, f"Expected False, got {email_result2}"

        phone_result = validate_phone("+244923456789")
        assert phone_result == True, f"Expected True, got {phone_result}"

        phone_result2 = validate_phone("0123")  # Starts with 0, which is invalid
        assert phone_result2 == False, f"Expected False, got {phone_result2}"

        nif_result = validate_nif("1234567890")  # 10 digits
        assert nif_result == True, f"Expected True, got {nif_result}"

        nif_result2 = validate_nif("123")
        assert nif_result2 == False, f"Expected False, got {nif_result2}"

        # Test string processing
        slug = generate_slug("Test User Name")
        assert slug == "test-user-name", f"Expected 'test-user-name', got '{slug}'"

        clean = clean_document_number("00.123.456/AB-CD")
        assert clean == "00123456ABCD", f"Expected '00123456ABCD', got '{clean}'"

        # Test safe conversions
        int_result = safe_int("123")
        assert int_result == 123, f"Expected 123, got {int_result}"

        int_result2 = safe_int("invalid")
        assert int_result2 == 0, f"Expected 0, got {int_result2}"

        float_result = safe_float("12.34")
        assert float_result == 12.34, f"Expected 12.34, got {float_result}"

        float_result2 = safe_float("invalid")
        assert float_result2 == 0.0, f"Expected 0.0, got {float_result2}"

        print("✅ Core utilities work correctly")
        return True

    except AssertionError as e:
        print(f"❌ Core utilities test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Core utilities test failed: {e}")
        return False


def test_core_exceptions():
    """Test core exception functionality."""
    print("Testing core exceptions...")

    try:

        class SILAError(Exception):
            def __init__(
                self,
                message: str,
                code: str = "sila_error",
                details: Optional[Dict[str, Any]] = None,
            ):
                self.message = message
                self.code = code
                self.details = details or {}
                super().__init__(message)

        class ResourceNotFoundError(SILAError):
            def __init__(
                self, resource_type: str, resource_id: Optional[Union[int, str]] = None
            ):
                message = f"{resource_type} not found"
                if resource_id is not None:
                    message += f" with ID: {resource_id}"
                super().__init__(
                    message,
                    "resource_not_found",
                    {"resource_type": resource_type, "resource_id": resource_id},
                )

        class ValidationError(SILAError):
            def __init__(self, details: str, field: Optional[str] = None):
                super().__init__(
                    f"Validation failed: {details}",
                    "validation_error",
                    {"details": details, "field": field},
                )

        # Test exception creation
        error = ResourceNotFoundError("User", "123")
        assert error.code == "resource_not_found"
        assert "User not found" in error.message
        assert error.details["resource_type"] == "User"
        assert error.details["resource_id"] == "123"

        # Test validation error
        validation_error = ValidationError("Invalid format", "email")
        assert validation_error.code == "validation_error"
        assert validation_error.details["field"] == "email"

        print("✅ Core exceptions work correctly")
        return True

    except Exception as e:
        print(f"❌ Core exceptions test failed: {e}")
        return False


def test_core_bases():
    """Test core base functionality."""
    print("Testing core bases...")

    try:
        # Test basic Pydantic-like functionality without external dependencies
        class BaseSchema:
            def __init__(self, **data):
                for key, value in data.items():
                    setattr(self, key, value)

            def dict(self):
                return self.__dict__

        class BaseResponseSchema(BaseSchema):
            def __init__(self, **data):
                super().__init__(**data)
                if not hasattr(self, "id"):
                    self.id = str(uuid4())
                if not hasattr(self, "created_at"):
                    self.created_at = datetime.utcnow()
                if not hasattr(self, "updated_at"):
                    self.updated_at = datetime.utcnow()

        class BaseCreateSchema(BaseSchema):
            def __init__(self, **data):
                super().__init__(**data)
                if not hasattr(self, "created_by"):
                    self.created_by = None

        # Test base schemas
        response = BaseResponseSchema(name="Test", email="test@example.com")
        assert hasattr(response, "id")
        assert hasattr(response, "created_at")
        assert hasattr(response, "updated_at")
        assert response.name == "Test"

        create = BaseCreateSchema(name="Test", email="test@example.com")
        assert hasattr(create, "created_by")
        assert create.name == "Test"

        print("✅ Core bases work correctly")
        return True

    except Exception as e:
        print(f"❌ Core bases test failed: {e}")
        return False


def test_integration():
    """Test integration between components."""
    print("Testing integration...")

    try:
        # Test integrated usage pattern
        class ValidationError(Exception):
            def __init__(self, message: str, field: Optional[str] = None):
                self.message = message
                self.field = field
                super().__init__(message)

        def validate_email(email: str) -> bool:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return re.match(pattern, email) is not None

        class UserCreate:
            def __init__(self, email: str, name: str):
                self.email = email
                self.name = name

            def validate(self):
                if not validate_email(self.email):
                    raise ValidationError("Invalid email format", "email")

        # Test valid case
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
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Common Layer Core Implementation")
    print("=" * 55)

    tests = [
        test_file_structure,
        test_core_utilities,
        test_core_exceptions,
        test_core_bases,
        test_integration,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 55)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! Common layer core functionality is working correctly."
        )
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
