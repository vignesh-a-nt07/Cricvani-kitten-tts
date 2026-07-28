from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import health, voices, tts
from config import settings
from utils.logger import logger

app = FastAPI(
    title="CricVani Kitten TTS Server",
    description="Standalone lightweight TTS provider using Kitten TTS for local development.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler to prevent Python stack traces from leaking
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "An unexpected error occurred."}
    )

# Register routes
app.include_router(health.router)
app.include_router(voices.router)
app.include_router(tts.router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting CricVani Kitten TTS Server on {settings.host}:{settings.port}")
    logger.info("Initializing TTS Service and loading model...")
    # The TTS service is initialized globally in services/tts_service.py
    # but we can import it here to ensure it loads during startup
    from services.tts_service import tts_service
    # Just accessing the instance ensures the model is loaded once
    _ = tts_service.get_provider()
    logger.info("Startup complete. Ready to serve requests.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down CricVani Kitten TTS Server...")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app", 
        host=settings.host, 
        port=settings.port, 
        reload=False
    )
