from providers.kitten_provider import KittenProvider

class TTSService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def __init__(self):
        # Initialize provider (loads model automatically)
        self.provider = KittenProvider()
        
    def get_provider(self):
        return self.provider

# Singleton pattern to ensure model is only loaded once
tts_service = TTSService.get_instance()
