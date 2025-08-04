# HCGateway Dashboard

A comprehensive Streamlit dashboard for visualizing HCGateway steps data with enterprise-grade architecture, security, and Docker deployment capabilities.

## 🏗️ Architecture

This application follows a clean, modular architecture designed for scalability and maintainability:

```
src/hcgateway_dashboard/
├── __init__.py          # Package initialization and exports
├── __main__.py          # Application entry point
├── api_client.py        # HCGateway API client with token management
├── config.py            # Configuration and environment management
├── dashboard.py         # Main dashboard class and Streamlit UI
└── models/              # Pydantic data models
    ├── __init__.py
    └── steps.py         # Steps data validation models
```

## 🚀 Features

- **🔐 Secure Authentication**: Token-based authentication with automatic refresh
- **📊 Data Validation**: Robust Pydantic models for API response validation
- **🎨 Interactive Visualization**: Clean Streamlit interface with date range selection
- **🐳 Docker Ready**: Multi-stage Docker builds for development and production
- **📝 Comprehensive Logging**: Structured logging with configurable levels
- **🧪 Test Coverage**: Comprehensive test suite with pytest
- **🔧 Type Safety**: Full type annotations with mypy support
- **📦 Modern Packaging**: Uses pyproject.toml with proper dependency management

## 🛠️ Installation

### Option 1: Package Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/aingelmo/HCGateway-dashboard.git
cd HCGateway-dashboard

# Install the package
pip install -e .

# Run the application
hcgateway-dashboard
```

### Option 2: Docker Deployment (Production)

```bash
# Copy environment template
cp .env.example .env
# Edit .env with your credentials

# Build and run with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:8501
```

### Option 3: Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run development container with hot reload
docker-compose --profile dev up --build

# Access development server
open http://localhost:8502
```

## 🔧 Configuration

The application can be configured through environment variables or a `.env` file:

| Variable             | Description                                 | Default  |
| -------------------- | ------------------------------------------- | -------- |
| `HCGATEWAY_USERNAME` | HCGateway API username                      | Required |
| `HCGATEWAY_PASSWORD` | HCGateway API password                      | Required |
| `LOGGING_LEVEL`      | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO`   |

## 🐳 Docker Deployment

### Production Deployment

```bash
# Production build (optimized, secure)
docker-compose up --build

# Or build specific production target
docker build --target production -t hcgateway-dashboard .
docker run -p 8501:8501 --env-file .env hcgateway-dashboard
```

### Development Deployment

```bash
# Development build (with dev tools, hot reload)
docker-compose --profile dev up --build
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=hcgateway_dashboard --cov-report=html

# Run specific test file
pytest tests/test_api_client.py -v
```

## 🔍 Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src tests

# Run all quality checks
ruff check . && mypy src tests && pytest
```

## 📊 Usage

1. **Authentication**: Enter your HCGateway credentials or set them in environment variables
2. **Date Selection**: Choose your desired date range (defaults to last month)
3. **Data Visualization**: View your steps data in interactive charts and tables

## 🏢 Production Considerations

### Security Features

- Non-root container user
- Environment-based secret management
- XSRF protection enabled
- Secure token management with automatic refresh
- Input validation with Pydantic models

### Performance Optimizations

- Multi-stage Docker builds
- Efficient dependency caching
- Minimal base image (python:3.13-slim)
- Health checks for container orchestration

### Monitoring & Observability

- Structured logging with correlation IDs
- Health check endpoints
- Comprehensive error handling
- Performance metrics ready

## 🔄 CI/CD Integration

This package is designed to integrate seamlessly with modern CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Test and Deploy
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.13"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src tests
      - run: pytest --cov=hcgateway_dashboard

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t hcgateway-dashboard .
      - run: docker push your-registry/hcgateway-dashboard
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the coding standards
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@hcgateway.com or create an issue on GitHub.

---

Built with ❤️ for the HCGateway community
