# CricVani Kitten TTS Server

A production-quality standalone TTS Server designed to replace cloud providers (Google, ElevenLabs, Sarvam) during local development to reduce costs. It exposes standard REST APIs that emulate cloud TTS providers.

## Technology Stack
- **Framework**: Python, FastAPI, Uvicorn
- **Engine**: Kitten TTS (via ONNX Runtime)
- **Containerization**: Docker, Docker Compose
- **Configuration**: Python Dotenv, Pydantic

## Architecture
- Loads the Kitten TTS model **only once** on startup.
- Never reloads the model per request.
- Uses `BackgroundTasks` to automatically clean up temporary `.wav` files and prevent memory/storage leaks.
- Employs robust dependency injection for API key validation (can be disabled for local dev).

## Prerequisites
- Python 3.10+
- Docker and Docker Compose

## Installation

### Local (Python)

python3 -m venv venv

source venv/bin/activate


1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Run the server:
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8001
   ```

### Docker
1. Start the server using Docker Compose:
   ```bash
   docker compose up -d
   ```
2. The server will run on `http://localhost:8001`.

## Configuration
Edit the `.env` file to customize the server:
```env
HOST=0.0.0.0
PORT=8001
ENABLE_AUTH=false
API_KEY=cricvani-dev
MODEL_PATH=models/kitten-tts.onnx
DEFAULT_VOICE=expr-voice-2-m
LOG_LEVEL=INFO
OUTPUT_DIRECTORY=generated
```

## API Endpoints

### 1. Root Endpoint (Unauthenticated)
```http
GET /
```
**Response (200 OK):**
```json
{
    "service": "CricVani Kitten TTS Server",
    "provider": "Kitten TTS",
    "version": "1.0.0"
}
```

### 2. Health Check (Unauthenticated)
```http
GET /health
```
**Response (200 OK):**
```json
{
    "status": "healthy",
    "provider": "Kitten TTS",
    "loaded": true,
    "model": "kitten-tts"
}
```

### 3. List Voices
```http
GET /voices
x-api-key: cricvani-dev
```
**Response (200 OK):**
```json
{
    "voices": [
        "expr-voice-2-m",
        "expr-voice-2-f",
        "kitten-en-us-1",
        "kitten-en-gb-1"
    ]
}
```

### 4. Generate TTS
```http
POST /tts
x-api-key: cricvani-dev
Content-Type: application/json

{
    "text": "Virat Kohli drives through covers for four.",
    "voice": "expr-voice-2-m",
    "speed": 1.0,
    "format": "wav"
}
```
**Response (200 OK):**
Returns `audio/wav` file.

**Error Response (400 Bad Request):**
```json
{
    "success": false,
    "message": "Voice 'invalid-voice' not found."
}
```

## LAN Usage
The server listens on `0.0.0.0` by default. This allows any device on the same local network (Wi-Fi) to connect to it.

To connect from CricVani:
1. Find your local IP address (e.g., `192.168.1.50`).
2. Point your CricVani TTS provider configuration to `http://192.168.1.50:8001/tts`.
3. Set `ENABLE_AUTH=false` in the server's `.env` so CricVani doesn't need API keys, OR configure CricVani to send the API key `cricvani-dev`.

## Troubleshooting
- **API Key Rejected**: Ensure you are passing the header `x-api-key`.
- **Audio Files Accumulating**: Background tasks ensure files are deleted after response delivery. If files remain, check `logs/server.log` for file access permission issues.
- **Model Loading Failed**: Ensure your `.onnx` model is present in `models/`. The server gracefully defaults to a dummy file generator for testing if the model is absent.
- **Voice Installation**: Download Kitten TTS `.onnx` models into the `models/` directory.

## Swagger Documentation
Once the server is running, visit:
- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)
# Cricvani-kitten-tts
