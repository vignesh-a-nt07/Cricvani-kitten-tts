.PHONY: setup run dev docker-build docker-run

# Install dependencies
setup:
	cp .env.example .env
	pip install -r requirements.txt

# Run FastAPI server
run:
	python -m uvicorn app:app --host 0.0.0.0 --port 8001

# Run with auto-reload (development)
dev:
	python -m uvicorn app:app --host 0.0.0.0 --port 8001 --reload

# Build Docker image
docker-build:
	docker build -t cricvani-kitten-tts .

# Run Docker container
docker-run:
	docker run --rm -p 8001:8001 --env-file .env cricvani-kitten-tts