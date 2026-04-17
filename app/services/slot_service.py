class SlotService:
    def __init__(self, doctor_repo):
        self.doctor_repo = doctor_repo

    async def get_available_dates(self, doctor_id: int):
        return await self.doctor_repo.get_available_dates(doctor_id)
    
    async def get_available_slots(self, doctor_id: int, date: str):
        return await self.doctor_repo.get_available_slots(doctor_id, date)