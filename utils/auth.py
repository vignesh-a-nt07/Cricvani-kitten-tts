from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    if not settings.enable_auth:
        return None
        
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "message": "API Key is missing"},
        )
    if api_key_header != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "message": "Invalid API Key"},
        )
    return api_key_header
