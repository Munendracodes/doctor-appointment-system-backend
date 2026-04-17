from sqlalchemy import select
from app.models.user import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def get_user_by_phone(self, phone: str):
        result = await self.db.execute(
            select(User).where(User.mobile_number == phone)
        )
        return result.scalar_one_or_none()

    async def create_user(self, phone: str):
        new_user = User(mobile_number=phone)

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user