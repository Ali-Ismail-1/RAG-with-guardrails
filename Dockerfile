# ---- base image ----
    FROM python:3.11-slim

    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PIP_NO_CACHE_DIR=1
    
    # OS deps (fastapi stack + chroma deps)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl git && \
        rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Copy requirements first for better layer caching
    COPY requirements.txt requirements.txt
    # If you have a dev file, comment it out in prod images
    # COPY requirements-dev.txt requirements-dev.txt
    
    RUN pip install --upgrade pip && \
        pip install -r requirements.txt && \
        pip install gunicorn uvicorn
    
    # Copy code
    COPY . .
    
    # Expose FastAPI port
    EXPOSE 8000
    
    # Gunicorn with Uvicorn workers. In PaaS (Railway/Render), $PORT is provided.
    # Locally, docker-compose will map 8000.
    CMD ["bash", "-lc", "gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 2 --bind 0.0.0.0:${PORT:-8000}"]
    