from sqlalchemy import select
from app.models.doctor import Doctor

class DoctorRepo:
    def __init__(self, db):
        self.db = db

    async def get_all_doctors(self):
        result = await self.db.execute(select(Doctor))
        return result.scalars().all()