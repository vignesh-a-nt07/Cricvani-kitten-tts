from config import settings
from services.tts_service import tts_service
from utils.logger import logger

class VoiceMapper:
    def __init__(self):
        # Build the alias dictionary from settings
        self.aliases = {
            "male_1": settings.voice_alias_male_1,
            "female_1": settings.voice_alias_female_1,
            "male_2": settings.voice_alias_male_2,
            "female_2": settings.voice_alias_female_2,
            "male_3": settings.voice_alias_male_3,
            "female_3": settings.voice_alias_female_3,
            "default": settings.voice_alias_default
        }

    def get_aliases(self) -> dict:
        return self.aliases

    def map_voice(self, requested_voice: str) -> str:
        provider = tts_service.get_provider()
        supported_voices = provider.get_supported_voices() if provider else []

        # If it's a natively supported voice, do nothing
        if requested_voice in supported_voices:
            logger.info(f"Voice Mapping | Requested: {requested_voice} | Mapped: (Native) | Final: {requested_voice}")
            return requested_voice

        # Check if it's in our alias dictionary
        mapped_voice = self.aliases.get(requested_voice.lower())

        # If completely unknown, fallback to DEFAULT_VOICE
        if not mapped_voice:
            final_voice = settings.default_voice
            logger.warning(f"Voice Mapping | Requested: {requested_voice} | Mapped: (Unknown) | Final: {final_voice} (Fallback)")
            return final_voice

        # We found a mapped voice
        # Ensure the mapped voice is actually supported, otherwise fallback
        if mapped_voice not in supported_voices:
            final_voice = settings.default_voice
            logger.warning(f"Voice Mapping | Requested: {requested_voice} | Mapped: {mapped_voice} (Unsupported) | Final: {final_voice} (Fallback)")
            return final_voice

        logger.info(f"Voice Mapping | Requested: {requested_voice} | Mapped: {mapped_voice} | Final: {mapped_voice}")
        return mapped_voice

voice_mapper = VoiceMapper()
