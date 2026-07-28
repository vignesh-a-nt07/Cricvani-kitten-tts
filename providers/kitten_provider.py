import time
import os
import uuid
import soundfile as sf
from providers.base import BaseTTSProvider
from config import settings
from utils.logger import logger
from kittentts import KittenTTS

class KittenProvider(BaseTTSProvider):
    def __init__(self):
        self.model = None
        self.supported_voices = []
        self._load_model()
        
    def _load_model(self):
        """Load Kitten TTS model once during initialization."""
        logger.info(f"Loading Kitten TTS model from {settings.model_path}...")
        try:
            # We initialize KittenTTS. If settings.model_path is a valid onnx file, we use it.
            # Otherwise we let it auto-download from HF.
            if settings.model_path and settings.model_path.endswith('.onnx') and os.path.exists(settings.model_path):
                voices_path = os.path.join(os.path.dirname(settings.model_path), "voices.npz")
                if os.path.exists(voices_path):
                    self.model = KittenTTS(model_path=settings.model_path, voices_path=voices_path)
                else:
                    self.model = KittenTTS()
            else:
                self.model = KittenTTS()
                
            if self.model:
                self.supported_voices = self.model.available_voices
                logger.info("Successfully loaded Kitten TTS model.")
        except Exception as e:
            logger.error(f"Error loading Kitten TTS model: {str(e)}")
            self.model = None
            
    def load_model(self):
        return self.model
        
    def get_supported_voices(self) -> list[str]:
        return self.supported_voices
        
    def generate_audio(self, text: str, voice: str, speed: float) -> str:
        """Generates audio and returns the path to the generated WAV file."""
        if voice not in self.supported_voices:
            raise ValueError(f"Voice '{voice}' not found.")
            
        if self.model is None:
            raise RuntimeError("TTS Model is not loaded.")
            
        file_id = str(uuid.uuid4())
        output_path = os.path.join(settings.output_directory, f"{file_id}.wav")
        
        # Log generation request
        logger.info(f"Generating TTS | Voice: {voice} | Speed: {speed} | Text: '{text[:20]}...'")
        
        # Generate audio
        audio = self.model.generate(text, voice=voice, speed=speed)
        
        # Write to WAV file
        sf.write(output_path, audio, 24000)
        
        return output_path

