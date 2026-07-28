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

    voice_alias_male_1: str = "expr-voice-2-m"
    voice_alias_female_1: str = "expr-voice-2-f"
    voice_alias_male_2: str = "expr-voice-3-m"
    voice_alias_female_2: str = "expr-voice-3-f"
    voice_alias_male_3: str = "expr-voice-4-m"
    voice_alias_female_3: str = "expr-voice-4-f"
    voice_alias_default: str = "expr-voice-2-m"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure necessary directories exist
os.makedirs(settings.output_directory, exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("models", exist_ok=True)
