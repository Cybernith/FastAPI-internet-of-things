from pydantic import BaseModel
import os


class Settings(BaseModel):
    APP_NAME: str = "FastAPI internet of things"
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:slowj504@localhost:3030/iot_db"
    )

settings = Settings()
