from fastapi import APIRouter
from services.tts_service import tts_service

router = APIRouter()

@router.get("/", tags=["Info"])
async def get_root():
    return {
        "service": "CricVani Kitten TTS Server",
        "provider": "Kitten TTS",
        "version": "1.0.0"
    }

@router.get("/health", tags=["Health"])
async def get_health():
    provider = tts_service.get_provider()
    model_loaded = provider.load_model() is not None
    
    return {
        "status": "healthy" if model_loaded else "degraded",
        "provider": "Kitten TTS",
        "loaded": model_loaded,
        "model": "kitten-tts"
    }
