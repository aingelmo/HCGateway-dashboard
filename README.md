# HCGateway Dashboard

A modern, enterprise-grade Streamlit dashboard for visualizing HCGateway steps data with **Ruff-optimized quality control** and Docker deployment.

## 🏗️ Architecture

Clean, scalable Python package structure:

```
src/hcgateway_dashboard/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── api_client.py        # HCGateway API client with token management
├── config.py            # Configuration management
├── dashboard.py         # Streamlit dashboard interface
└── models/              # Pydantic data models
    ├── __init__.py
    └── steps.py         # Steps data validation
```

## ⚡ Ruff-Powered Quality Control

This project leverages **Ruff** as the primary tool for code quality, replacing multiple tools:

- **Ruff Format** → replaces Black
- **Ruff Lint** → replaces flake8, isort, pydocstyle, bandit (partially)
- **MyPy** → type checking
- **Bandit** → security scanning
- **Pre-commit hooks** → automatic quality gates

### 🚀 Quick Quality Commands

```bash
# Format and fix code (primary workflow)
make format

# Check code quality
make lint

# Run complete quality gate
make quality-gate

# Show all commands
make help
```

## 🔧 Installation & Setup

### Option 1: Development Setup (Recommended)

```bash
# Clone and setup
git clone https://github.com/aingelmo/HCGateway-dashboard.git
cd HCGateway-dashboard

# Install everything (dependencies + pre-commit hooks)
make install

# Run the application
uv run hcgateway-dashboard
# or
hcgateway-dashboard  # if installed globally
```

### Option 2: Package Installation Only

```bash
# Install as package
pip install -e .

# Run
hcgateway-dashboard
```

### Option 3: Docker Deployment

```bash
# Create environment file
cp .env.example .env
# Edit .env with your credentials

# Run with Docker Compose
docker-compose up --build

# Access: http://localhost:8501
```

## 🛡️ Quality Control System

### Pre-commit Hooks (Automatic)

Every `git commit` automatically runs:

1. **File hygiene** - trailing whitespace, file endings
2. **Ruff format** - code formatting
3. **Ruff lint** - comprehensive linting
4. **MyPy** - type checking (src/ only)
5. **Bandit** - security scanning
6. **Detect-secrets** - credential leak prevention

### Manual Quality Control

```bash
# Essential workflow
make format     # Auto-fix formatting and style issues
make lint       # Check remaining issues
make test       # Run test suite
make security   # Security scan

# Complete pipeline
make quality-gate  # Run everything

# Development helpers
make clean      # Clean generated files
make dev        # Setup development environment
```

### Ruff Configuration Highlights

**Comprehensive rule coverage:**

- Code style (pycodestyle)
- Import sorting (isort)
- Documentation (pydocstyle)
- Security basics (bandit subset)
- Complexity (mccabe)
- Best practices (bugbear)
- Modern Python (pyupgrade)

**Smart ignores for different contexts:**

- Tests: Allow asserts, magic values, private access
- Init files: Allow unused imports
- App entry: Allow print statements

## 📦 Features

- 🔐 **Secure Authentication** with token refresh
- 📊 **Data Validation** using Pydantic models
- 🎨 **Interactive UI** with Streamlit
- 🐳 **Docker Ready** with multi-stage builds
- 📝 **Structured Logging** with configurable levels
- 🧪 **Comprehensive Tests** with pytest
- 🔧 **Full Type Safety** with strict MyPy
- ⚡ **Lightning-fast Quality** with Ruff
- 🛡️ **Security Scanning** with Bandit + detect-secrets

## 🔧 Configuration

Configure via environment variables or `.env` file:

| Variable             | Description                | Default    |
| -------------------- | -------------------------- | ---------- |
| `HCGATEWAY_USERNAME` | API username               | _Required_ |
| `HCGATEWAY_PASSWORD` | API password               | _Required_ |
| `LOGGING_LEVEL`      | Log level (DEBUG/INFO/etc) | `INFO`     |

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage details
uv run pytest --cov=hcgateway_dashboard --cov-report=html

# Run specific tests
uv run pytest tests/test_api_client.py -v
```

## � Docker

### Production Container

```bash
# Multi-stage optimized build
docker build -t hcgateway-dashboard .
docker run -p 8501:8501 --env-file .env hcgateway-dashboard
```

### Development Container

```bash
# With hot reload and dev tools
docker-compose --profile dev up --build
# Access: http://localhost:8502
```

## 🔄 CI/CD Integration

Optimized for modern CI/CD pipelines:

```yaml
# GitHub Actions example
name: Quality Gate
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: make ci
```

The `make ci` command runs:

- Format checking (no changes)
- Ruff linting
- Type checking
- Test suite with coverage

## � Usage

1. **Start the app**: `hcgateway-dashboard` or `docker-compose up`
2. **Authenticate**: Enter credentials or set environment variables
3. **Select dates**: Choose your analysis period
4. **Explore data**: Interactive charts and tables

## 🏢 Production Features

### Security

- Non-root container execution
- Environment-based secrets
- Token-based authentication with refresh
- Input validation via Pydantic
- Security vulnerability scanning

### Performance

- Multi-stage Docker builds
- Efficient dependency caching
- Minimal base image (python:3.13-slim)
- Lightning-fast quality checks with Ruff

### Monitoring

- Structured logging with correlation IDs
- Health check endpoints
- Comprehensive error handling
- Performance-ready metrics

## 🤝 Development Workflow

```bash
# 1. Setup (once)
make install

# 2. Development cycle
make format     # Auto-fix issues
make lint       # Check remaining issues
make test       # Verify functionality

# 3. Before commit
make quality-gate  # Final validation

# 4. Commit (hooks run automatically)
git add .
git commit -m "feat: add awesome feature"
```

## 🎯 Quality Standards

This project follows **perfection-driven development**:

- ✅ **Zero tolerance** for security vulnerabilities
- ✅ **Strict type checking** on all source code
- ✅ **Comprehensive linting** with 50+ rule categories
- ✅ **Automatic formatting** for consistency
- ✅ **High test coverage** (80%+ required)
- ✅ **Documentation standards** enforced
- ✅ **Pre-commit validation** prevents bad commits

## 🆘 Troubleshooting

### Pre-commit Issues

```bash
# Reinstall hooks
uv run pre-commit uninstall
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

### Quality Gate Failures

```bash
# Auto-fix most issues
make format

# Check what remains
make lint

# Fix manually, then rerun
make quality-gate
```

### Docker Issues

```bash
# Rebuild from scratch
docker-compose down
docker system prune -f
docker-compose up --build
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Follow the quality standards (`make quality-gate`)
4. Commit changes (`git commit -m 'feat: description'`)
5. Push branch (`git push origin feature/name`)
6. Open Pull Request

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/aingelmo/HCGateway-dashboard/issues)
- **Email**: aingelmo@gmail.com

---

**Built with ⚡ Ruff optimization and 🛡️ enterprise-grade quality control**

# Copy environment template

cp .env.example .env

# Edit .env with your credentials

# Build and run with Docker Compose

docker-compose up --build

# Access the application

open http://localhost:8501

````

### Option 3: Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run development container with hot reload
docker-compose --profile dev up --build

# Access development server
open http://localhost:8502
````

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

For support, email aingelmo@gmail.com or create an issue on GitHub.

---

Built with ❤️ for the HCGateway community
