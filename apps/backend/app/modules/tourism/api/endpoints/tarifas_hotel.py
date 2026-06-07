from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/tarifas-hotel", tags=["Turismo - TarifasHotel"])


@router.get("/")
async def listar_tarifas_hotel() -> list[dict[str, str]]:
    return []
