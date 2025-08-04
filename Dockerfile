# Simple Python 3.13 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-dev

# Copy application code
COPY src/ ./src/
COPY README.md ./
RUN pip install -e .

# Expose Streamlit port
EXPOSE 8501

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0", "src/hcgateway_dashboard/__main__.py"]
