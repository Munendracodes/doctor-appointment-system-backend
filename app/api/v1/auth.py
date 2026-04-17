from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.services.otp_service import send_otp, validate_otp
from app.core.dependencies import get_user_service
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-otp")
async def send_otp_api(phone: str):
    result = await send_otp(phone)
    return JSONResponse(content=result, status_code=result["status"])


@router.post("/validate-otp")
async def validate_otp_api(
    phone: str,
    otp: str,
    user_service: UserService = Depends(get_user_service)
):
    result = await validate_otp(phone, otp, user_service)
    return JSONResponse(content=result, status_code=result["status"])