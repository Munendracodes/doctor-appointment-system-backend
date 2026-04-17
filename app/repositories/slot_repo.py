from app.models.slot import Slot
from sqlalchemy import select, func, distinct, and_
from datetime import datetime, timedelta



class SlotRepo:
    def __init__(self, db):
        self.db = db

    async def get_available_dates(self, doctor_id: int):
        result = await self.db.execute(
            select(distinct(Slot.slot_date))
            .where(
                Slot.doctor_id == doctor_id,
                Slot.status == "AVAILABLE",
                Slot.slot_date.in_([func.current_date(), func.current_date() + 1])
            )
            .order_by(Slot.slot_date)
        )
        return result.scalars().all()
    


    async def get_available_slots(self, doctor_id: int, date: str):
        buffer_minutes = 10
        current_time = datetime.utcnow() + timedelta(minutes=buffer_minutes)

        result = await self.db.execute(
            select(Slot)
            .where(
                Slot.doctor_id == doctor_id,
                Slot.slot_date == date,
                Slot.status == "AVAILABLE",
                Slot.start_time > current_time.time()
            )
            .order_by(Slot.start_time)
        )
        return result.scalars().all()