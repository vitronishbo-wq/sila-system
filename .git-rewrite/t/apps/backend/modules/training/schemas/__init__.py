"""Training schemas exports (minimal for training routes)."""

from .simple import (
    TrainingModuleCreate,
    TrainingModuleRead,
    TrainingSessionCreate,
    TrainingSessionRead,
    TrainingUserCreate,
    TrainingUserRead,
)

__all__ = [
    "TrainingModuleCreate",
    "TrainingModuleRead",
    "TrainingSessionCreate",
    "TrainingSessionRead",
    "TrainingUserCreate",
    "TrainingUserRead",
]
