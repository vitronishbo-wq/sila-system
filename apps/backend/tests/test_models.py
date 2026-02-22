"""Tests for models."""

import pytest

from modules.citizenship.models.citizen import Citizen


def test_citizen_model():
    """Test the Citizen model definition."""
    # Check that the model has the expected attributes
    expected_attributes = [
        "id",
        "name",
        "email",
        "phone",
        "address",
        "is_active",
        "created_at",
        "updated_at",
    ]

    for attr in expected_attributes:
        assert hasattr(Citizen, attr), f"Citizen is missing attribute: {attr}"

    # Check table name
    assert Citizen.__tablename__ == "citizens"
