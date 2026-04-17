from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user, get_slot_service
from app.services.slot_service import SlotService


router = APIRouter(prefix="/slots", tags=["slots"])



@router.get("/available-dates/{doctor_id}")
async def get_available_dates(
    doctor_id: int,
    current_user: dict = Depends(get_current_user),
    slot_service: SlotService = Depends(get_slot_service)
):
    available_dates = await slot_service.get_available_dates(doctor_id)
    return {"available_dates": available_dates}

@router.get("/available-slots/{doctor_id}/{date}")
async def get_available_slots(
    doctor_id: int,
    date: str,
    current_user: dict = Depends(get_current_user),
    slot_service: SlotService = Depends(get_slot_service)
):
    available_slots = await slot_service.get_available_slots(doctor_id, date)
    return {"available_slots": available_slots}

@router.post("/reserve")
async def reserve_slot(request: dict,
    current_user: dict = Depends(get_current_user),
    slot_service: SlotService = Depends(get_slot_service)
):
    
    return {"message": "Slot reserved successfully"}

@router.post("/confirm")
async def confirm_reservation(request: dict,
    current_user: dict = Depends(get_current_user),
    slot_service: SlotService = Depends(get_slot_service)
):
    
    return {"message": "Slot reservation confirmed"}