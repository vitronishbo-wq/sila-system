"""
Examples demonstrating the usage of common layer components.

This file shows how to use the shared exceptions, base models, and utilities
across different modules in the SILA system.
"""

from datetime import datetime

from modules.common.bases import (
    BaseCreateSchema,
    BaseListResponse,
    BaseResponseSchema,
    BaseSearchSchema,
    SILABase,
)
from modules.common.exceptions import (
    ResourceNotFoundError,
    ValidationError,
    handle_sila_error,
)
from modules.common.utils import (
    clean_document_number,
    format_datetime_iso,
    generate_slug,
    hash_password,
    validate_email,
    validate_nif,
)


# Example: Using common exceptions
class UserService:
    """Example service using common exceptions."""

    def get_user(self, user_id: str):
        """Get user by ID with proper error handling."""
        if not user_id:
            raise ValidationError("User ID is required", "user_id")

        # Simulate user not found
        if user_id == "nonexistent":
            raise ResourceNotFoundError("User", user_id)

        return {"id": user_id, "name": "John Doe"}

    def handle_user_request(self, user_id: str):
        """Example of handling exceptions and converting to HTTP responses."""
        try:
            return self.get_user(user_id)
        except ResourceNotFoundError as e:
            # Convert to HTTP exception
            http_exception = handle_sila_error(e)
            return {
                "error": http_exception.detail,
                "status_code": http_exception.status_code,
            }


# Example: Using base schemas
class UserCreateSchema(BaseCreateSchema):
    """Example user creation schema using common base."""

    email: str
    name: str
    nif: str
    password: str

    def validate_email_format(self):
        """Validate email using common utility."""
        if not validate_email(self.email):
            raise ValidationError("Invalid email format", "email")

    def validate_nif_format(self):
        """Validate NIF using common utility."""
        if not validate_nif(self.nif):
            raise ValidationError("Invalid NIF format", "nif")

    def hash_user_password(self):
        """Hash password using common utility."""
        self.password = hash_password(self.password)


class UserResponseSchema(BaseResponseSchema):
    """Example user response schema using common base."""

    email: str
    name: str
    nif: str
    slug: str

    @classmethod
    def from_user_data(cls, user_data: dict) -> "UserResponseSchema":
        """Create response from user data with common utilities."""
        return cls(
            **user_data,
            slug=generate_slug(user_data["name"]),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )


# Example: Using common utilities in a service
class DocumentService:
    """Example service using common utilities."""

    def process_document(self, document_number: str, document_type: str):
        """Process document using common utilities."""
        # Clean document number
        clean_number = clean_document_number(document_number)

        # Generate slug for document type
        type_slug = generate_slug(document_type)

        # Format timestamps
        now = datetime.utcnow()
        formatted_time = format_datetime_iso(now)

        return {
            "clean_number": clean_number,
            "type_slug": type_slug,
            "processed_at": formatted_time,
        }

    def search_documents(self, query: str, page: int = 1, size: int = 20):
        """Search documents using common search schema."""
        search_params = BaseSearchSchema(query=query, page=page, size=size)

        # Simulate search results
        documents = [
            {"id": "1", "title": "Document 1"},
            {"id": "2", "title": "Document 2"},
        ]

        # Create paginated response
        response = BaseListResponse.create(
            items=documents,
            total=len(documents),
            page=search_params.page,
            size=search_params.size,
        )

        return response


# Example: Using SQLAlchemy base model
class UserModel(SILABase):
    """Example user model using common SQLAlchemy base."""

    __tablename__ = "common_users"

    email = Column("email", String(255), unique=True, nullable=False)
    name = Column("name", String(255), nullable=False)
    nif = Column("nif", String(20), unique=True, nullable=False)
    password_hash = Column("password_hash", String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


# Example usage function
def demonstrate_common_usage():
    """Demonstrate how to use common layer components."""

    # 1. Using exceptions
    user_service = UserService()

    try:
        result = user_service.get_user("nonexistent")
    except ResourceNotFoundError as e:
        print(f"Caught exception: {e.message} (Code: {e.code})")

    # 2. Using base schemas
    user_data = {
        "email": "john.doe@example.com",
        "name": "John Doe",
        "nif": "12345678901",
        "password": "securepassword123",
    }

    user_schema = UserCreateSchema(**user_data)
    user_schema.validate_email_format()
    user_schema.validate_nif_format()
    user_schema.hash_user_password()

    print(f"Validated user: {user_schema.email}")
    print(f"Hashed password: {user_schema.password[:20]}...")

    # 3. Using utilities
    doc_service = DocumentService()
    doc_result = doc_service.process_document("00.123.456/ABC", "Birth Certificate")
    print(f"Processed document: {doc_result}")

    # 4. Using search and pagination
    search_result = doc_service.search_documents("certificate", page=1, size=10)
    print(f"Search results: {search_result.total} items found")


if __name__ == "__main__":
    demonstrate_common_usage()
