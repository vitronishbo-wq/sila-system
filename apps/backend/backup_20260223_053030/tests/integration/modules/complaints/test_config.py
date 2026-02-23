"""Test configuration for complaints module."""

from fastapi.testclient import TestClient

from app.main import app

# Create test client
client = TestClient(app)

# Test data
TEST_COMPLAINT_DATA = {
    "title": "Test Complaint",
    "description": "This is a test complaint",
    "category": "general",
    "priority": "medium",
    "citizen_id": 1,
}

TEST_USER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User",
}
