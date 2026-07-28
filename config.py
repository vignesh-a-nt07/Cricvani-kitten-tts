import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8001
    enable_auth: bool = False
    api_key: str = "cricvani-dev"
    model_path: str = "models/kitten-tts.onnx"
    default_voice: str = "expr-voice-2-m"
    log_level: str = "INFO"
    output_directory: str = "generated"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure necessary directories exist
os.makedirs(settings.output_directory, exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("models", exist_ok=True)
