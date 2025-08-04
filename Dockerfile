# Use Python 3.13 slim image for smaller size and security
FROM python:3.13-slim as base

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash hcgateway

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install uv && \
    uv sync --no-dev

# Copy application code
COPY src/ ./src/
COPY README.md ./

# Install the package
RUN pip install -e .

# Switch to non-root user
USER hcgateway

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set default command
CMD ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0", "src/hcgateway_dashboard/__main__.py"]

# Development stage
FROM base as development

# Switch back to root to install dev dependencies
USER root

# Install development dependencies
RUN uv sync

# Install additional dev tools
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to non-root user
USER hcgateway

# Production stage
FROM base as production

# Production optimizations
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=false \
    STREAMLIT_BROWSER_GATHER_STATS=false \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
