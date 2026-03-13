try:
    from ..models.document import DocumentNumber
except Exception:

    class DocumentNumber:

        def __init__(self, value: str):
            self.value = value
__all__ = ['DocumentNumber']