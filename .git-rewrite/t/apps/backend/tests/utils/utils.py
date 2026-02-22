"""Test utility helper functions used across the test suite."""

import random
import string


def random_lower_string(length: int = 12) -> str:
    """Generate a random lowercase ASCII string of a given length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    """Generate a random email address for testing purposes."""
    user = random_lower_string(10)
    domain = random.choice(["example.com", "test.com", "mail.com"])
    return f"{user}@{domain}"
