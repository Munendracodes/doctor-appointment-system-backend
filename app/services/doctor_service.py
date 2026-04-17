class DoctorService:
    def __init__(self, doctor_repo):
        self.doctor_repo = doctor_repo

    async def get_all_doctors(self):
        return await self.doctor_repo.get_all_doctors()