from fastapi import APIRouter

from .health import router as health_router

router = APIRouter(prefix="/procurement", tags=["procurement"])
router.include_router(health_router)


@router.post("/tender")
def create_tender():
    return {"status": "accepted"}


@router.post("/supplier")
def register_supplier():
    return {"status": "accepted"}


@router.post("/bid")
def submit_bid():
    return {"status": "accepted"}


@router.post("/evaluate/{tender_id}")
def evaluate_tender(tender_id: str):
    return {"status": "accepted", "tender_id": tender_id}
