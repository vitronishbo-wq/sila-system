"""Force delete users utility module.

This module provides utilities for safely deleting users from the database.
It includes safety checks to prevent accidental deletion in production.
"""

import os
import sys
from typing import List
from urllib.parse import urlparse


def get_target_emails(emails: str = None) -> List[str]:
    """Get target emails from CLI argument or environment variable.

    Args:
        emails: Comma-separated email string from CLI

    Returns:
        List of email addresses to delete
    """
    if emails:
        return [e.strip() for e in emails.split(",")]

    env_emails = os.getenv("FORCE_DELETE_EMAILS", "")
    if env_emails:
        return [e.strip() for e in env_emails.split(",")]

    # Default admin email
    return ["admin@sila.co.ao"]


def check_safety(db_url: str) -> None:
    """Check if it's safe to perform force delete operation.

    Args:
        db_url: Database connection URL

    Raises:
        SystemExit: If safety check fails
    """
    from core.config import settings

    parsed = urlparse(db_url)
    hostname = parsed.hostname or "localhost"

    # Block remote databases in development
    if settings.ENVIRONMENT == "development":
        if hostname not in ("localhost", "127.0.0.1"):
            print(
                f"❌ Safety check failed: Cannot delete from remote database in development"
            )
            print(f"   Host: {hostname}")
            sys.exit(1)

    # Block all operations in production
    if settings.ENVIRONMENT == "production":
        print(f"❌ Safety check failed: Force delete is disabled in production")
        sys.exit(1)


def force_delete_users(emails: List[str], db_url: str) -> None:
    """Delete users from the database.

    Args:
        emails: List of email addresses to delete
        db_url: Database connection URL
    """
    check_safety(db_url)
    # Implementation would go here
    pass
