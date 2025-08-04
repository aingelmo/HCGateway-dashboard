FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY src/ ./src/
COPY README.md ./
COPY app.py app.py
COPY pyproject.toml uv.lock ./

RUN uv sync

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
