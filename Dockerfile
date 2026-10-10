# Hotel Reviews Sentiment Analysis — Docker Image
# Serves the FastAPI REST API + Gradio demo

FROM python:3.10-slim

# ── Metadata ──────────────────────────────────────────────────────────────────
LABEL maintainer="Dr. Lalit <lalitjindal79@github>"
LABEL description="Hotel Reviews Sentiment Analysis API — BERT, GPT-2, Ollama"
LABEL version="1.0.0"

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Python dependencies (cached layer) ───────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        torch==2.1.0+cpu \
        torchvision==0.16.0+cpu \
        --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi==0.104.1 uvicorn[standard]==0.24.0

# ── Download NLTK resources ───────────────────────────────────────────────────
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# ── Copy project files ────────────────────────────────────────────────────────
COPY src/       ./src/
COPY api/       ./api/
COPY results/   ./results/
COPY models/    ./models/
COPY app.py     .

# ── Environment ───────────────────────────────────────────────────────────────
ENV PYTHONPATH="/app/src"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# ── Health check ──────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# ── Expose ports ──────────────────────────────────────────────────────────────
EXPOSE 8000   
# FastAPI
EXPOSE 7860   
# Gradio

# ── Default command — FastAPI ─────────────────────────────────────────────────
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
