from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017/taskwise_ia"
    jwt_secret: str = "change_me"
    jwt_expire_minutes: int = 60
    ai_key: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
