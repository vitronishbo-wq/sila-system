from fastapi import APIRouter

router = APIRouter()


def module_name() -> str:
    parts = __name__.split(".")
    try:
        return f"{parts[3]}.{parts[4]}"
    except Exception:
        return __name__


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "module": module_name()}
