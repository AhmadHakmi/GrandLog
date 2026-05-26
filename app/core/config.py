from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "GrandLog"
    database_url: str = "sqlite:///./grandlog.db"

    class Config:
        env_file = ".env"


settings = Settings()
