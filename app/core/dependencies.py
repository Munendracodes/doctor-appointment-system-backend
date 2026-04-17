from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.core.security import decode_token
from app.services.doctor_service import DoctorService
from app.repositories.doctor_repo import DoctorRepo
from app.repositories.slot_repo import SlotRepo
from app.services.slot_service import SlotService

security = HTTPBearer()


def get_user_service(db=Depends(get_db)):
    return UserService(UserRepository(db))

def get_doctor_service(db=Depends(get_db)):
    return DoctorService(DoctorRepo(db))

def get_slot_service(db=Depends(get_db)):
    return SlotService(SlotRepo(db))




async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload