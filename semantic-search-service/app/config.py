from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_HOST: str
    QDRANT_PORT: int
    COLLECTION_NAME: str
    MODEL_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()