from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    gemma_model: str = "gemma3:4b"
    max_emails: int = 20
    backend_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()