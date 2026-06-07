import sentry_sdk

from apps.backend.core.config import settings


def init_sentry():
    """Initialize Sentry SDK for error tracking"""
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN if hasattr(settings, "SENTRY_DSN") else None,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=(settings.ENVIRONMENT if hasattr(settings, "ENVIRONMENT") else "development"),
    )
