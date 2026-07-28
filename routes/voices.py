from fastapi import APIRouter, Depends
from services.tts_service import tts_service
from utils.auth import verify_api_key

router = APIRouter()

@router.get("/voices", dependencies=[Depends(verify_api_key)], tags=["Voices"])
async def get_voices():
    from services.voice_mapper import voice_mapper
    provider = tts_service.get_provider()
    return {
        "aliases": voice_mapper.get_aliases(),
        "voices": provider.get_supported_voices() if provider else []
    }
