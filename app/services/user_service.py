class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def get_or_create_user(self, phone: str):
        user = await self.user_repo.get_user_by_phone(phone)

        if not user:
            user = await self.user_repo.create_user(phone)

        return user