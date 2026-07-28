from abc import ABC, abstractmethod

class BaseTTSProvider(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def generate_audio(self, text: str, voice: str, speed: float) -> str:
        pass
        
    @abstractmethod
    def get_supported_voices(self) -> list:
        pass
