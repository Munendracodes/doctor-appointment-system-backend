from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user, get_doctor_service
from app.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.services.doctor_service import DoctorService
from app.core.dependencies import get_doctor_service

router = APIRouter(prefix="/doctors", tags=["doctors"])



@router.get("/")
async def get_doctors(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    doctor_service: DoctorService = Depends(get_doctor_service)
):
    doctors = await doctor_service.get_all_doctors()
    return {"doctors": doctors}