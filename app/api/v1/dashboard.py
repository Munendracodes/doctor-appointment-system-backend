from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
async def dashboard(user=Depends(get_current_user)):
    return {
        "message": "Secure endpoint",
        "user": user
    }