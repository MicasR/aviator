from pydantic import BaseSettings


class Settings(BaseSettings):
    # login
    user_name: str
    password: str

    class Config:
        env_file = ".env"


settings = Settings()