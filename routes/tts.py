import time
from fastapi import APIRouter, Depends, BackgroundTasks, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from services.tts_service import tts_service
from utils.auth import verify_api_key
from utils.cleanup import delete_temp_file
from utils.logger import logger

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: str
    speed: float = 1.0
    format: str = "wav"

@router.post("/tts", dependencies=[Depends(verify_api_key)], tags=["TTS"])
async def generate_tts(request: Request, tts_req: TTSRequest, background_tasks: BackgroundTasks):
    from services.voice_mapper import voice_mapper
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    provider = tts_service.get_provider()
    
    try:
        # Map alias if necessary
        final_voice = voice_mapper.map_voice(tts_req.voice)
        
        # Generate audio file
        file_path = provider.generate_audio(
            text=tts_req.text,
            voice=final_voice,
            speed=tts_req.speed
        )
        
        # Calculate processing time
        generation_time = time.time() - start_time
        char_count = len(tts_req.text)
        
        # Log success
        logger.info(
            f"TTS Success | IP: {client_ip} | Voice: {tts_req.voice} | "
            f"Chars: {char_count} | Time: {generation_time:.3f}s"
        )
        
        # Schedule cleanup
        background_tasks.add_task(delete_temp_file, file_path)
        
        # Return audio file
        return FileResponse(
            path=file_path, 
            media_type="audio/wav", 
            filename=f"tts_{tts_req.voice}.wav"
        )
        
    except ValueError as e:
        logger.warning(f"TTS Validation Error | IP: {client_ip} | Voice: {tts_req.voice} | Error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(e)}
        )
    except Exception as e:
        logger.error(f"TTS Generation Error | IP: {client_ip} | Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error during audio generation."}
        )
