# Value object placeholder: re-export existing helpers if present
try:
    from ..models.document import DocumentNumber  # type: ignore
except Exception:
    # Fallback placeholder
    class DocumentNumber:
        def __init__(self, value: str):
            self.value = value

__all__ = ["DocumentNumber"]
