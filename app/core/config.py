from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Doctor Appointment System"
    DEBUG: bool = True

    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Security
    SECRET_KEY: str = "change_this"
    ALGORITHM: str = "HS256"

    # ✅ THIS is the correct way in Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

if __name__ == "__main__":
    settings = Settings() # type: ignore
    print(settings.model_dump()) 

@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
