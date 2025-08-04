# HCGateway Dashboard

A modern Streamlit dashboard for visualizing HCGateway steps data with enterprise-grade quality control and secure authentication.

## 🏗️ Architecture

Clean, production-ready Python package structure:

```text
src/hcgateway_dashboard/
├── __init__.py          # Package initialization and exports
├── __main__.py          # CLI entry point
├── api_client.py        # HCGateway API client with token management
├── config.py            # Configuration and environment management
├── dashboard.py         # Streamlit dashboard interface
└── models/              # Pydantic data models
    ├── __init__.py      # Model exports
    └── steps.py         # Steps data validation and schemas
```

## ⚡ Quality Control with Ruff

Lightning-fast code quality powered by **Ruff**:

- **Format** → Automatic code formatting
- **Lint** → Comprehensive linting (50+ rule categories)
- **Pre-commit** → Automatic quality gates on every commit

### 🚀 Essential Commands

```bash
make format     # Format and fix code issues
make lint       # Check code quality
make test       # Run tests with coverage
make install    # Install dependencies
make help       # Show all commands
```

## 🔧 Quick Start

### Option 1: Local Development

```bash
# Clone and setup
git clone https://github.com/aingelmo/HCGateway-dashboard.git
cd HCGateway-dashboard
make install

# Configure credentials
cp .env.example .env
# Edit .env with your HCGateway credentials

# Run the application
hcgateway-dashboard
```

### Option 2: Docker

```bash
# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Run with Docker Compose
docker-compose up --build

# Access: http://localhost:8501
```

## 🚀 Usage

1. **Configure**: Set `HCGATEWAY_USERNAME` and `HCGATEWAY_PASSWORD` in `.env`
2. **Launch**: Run `hcgateway-dashboard` or `docker-compose up`
3. **Authenticate**: Credentials auto-loaded from environment
4. **Select Dates**: Choose your analysis period (defaults to last month)
5. **Explore**: View interactive charts and data tables

## 📊 Features

### Security & Authentication

- 🔐 **JWT Token Management** with automatic refresh
- 🛡️ **Secure API Communication** via HTTPS
- 🔒 **Environment-based Secrets** (no hardcoded credentials)
- ✅ **Input Validation** with Pydantic models

### Data & Visualization

- 📊 **Interactive Charts** with Streamlit
- 📈 **Multi-source Tracking** (multiple apps/devices)
- 📅 **Flexible Date Ranges** (up to 5 years history)
- 🔄 **Real-time Validation** and error handling

### Developer Experience

- ⚡ **Lightning-fast Quality Control** with Ruff
- 🧪 **Comprehensive Testing** with pytest
- 🐳 **Docker Ready** for production deployment
- 📝 **Structured Logging** with configurable levels

## 🔧 Configuration

Configure via environment variables or `.env` file:

| Variable             | Description                | Default | Required |
| -------------------- | -------------------------- | ------- | -------- |
| `HCGATEWAY_USERNAME` | HCGateway API username     | -       | Yes      |
| `HCGATEWAY_PASSWORD` | HCGateway API password     | -       | Yes      |
| `LOGGING_LEVEL`      | Log level (DEBUG/INFO/etc) | `INFO`  | No       |

## 🛠️ Development

### Quality Control Workflow

```bash
# Essential development cycle
make format     # Auto-fix formatting and style issues
make lint       # Check remaining code quality issues
make test       # Run test suite with coverage
```

### Pre-commit Hooks

Automatic quality gates on every commit:

1. **File hygiene** - trailing whitespace, file endings
2. **Ruff format** - code formatting
3. **Ruff lint** - comprehensive linting with auto-fix

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific tests
uv run pytest tests/test_api_client.py -v

# Generate HTML coverage report
uv run pytest --cov=hcgateway_dashboard --cov-report=html
```

## 🐳 Docker

### Production Deployment

```bash
# Build and run
docker-compose up --build

# Health check
curl http://localhost:8501/_stcore/health
```

### Features

- **Lightweight**: Based on `python:3.13-slim`
- **Security**: Non-root container execution
- **Performance**: Multi-stage builds with dependency caching
- **Environment**: Full `.env` file support

## 🏛️ Technical Architecture

### Core Components

- **TokenManager**: JWT lifecycle management with automatic refresh
- **HCGatewayClient**: RESTful API client with robust error handling
- **Dashboard**: Streamlit interface with Pydantic validation
- **Models**: Data validation schemas for steps records

### API Integration

- **Base URL**: `https://api.hcgateway.shuchir.dev/api/v2`
- **Authentication**: JWT Bearer tokens with refresh capability
- **Endpoints**: `/login`, `/refresh`, `/fetch/steps`
- **Queries**: MongoDB-style date range queries
- **Validation**: Comprehensive Pydantic model validation

## 🎯 Quality Standards

Enterprise-grade quality following perfection-driven development:

- ✅ **Zero tolerance** for code quality issues
- ✅ **Strict type checking** with MyPy compatibility
- ✅ **Comprehensive linting** (50+ Ruff rule categories)
- ✅ **Automatic formatting** for consistency
- ✅ **Test coverage** enforcement
- ✅ **Pre-commit validation** prevents bad commits
- ✅ **Security scanning** with built-in rules

## 🆘 Troubleshooting

### Authentication Issues

```bash
# Check credentials
cat .env | grep HCGATEWAY

# Test API connectivity
curl -X POST https://api.hcgateway.shuchir.dev/api/v2/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}'
```

### Quality Check Issues

```bash
# Auto-fix most issues
make format

# Check remaining issues
make lint
```

### Docker Issues

```bash
# Complete rebuild
docker-compose down
docker system prune -f
docker-compose up --build
```

### Debug Mode

```bash
# Enable debug logging
LOGGING_LEVEL=DEBUG hcgateway-dashboard
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/awesome-feature`)
3. **Follow** quality standards (`make format && make lint && make test`)
4. **Commit** changes (`git commit -m 'feat: add awesome feature'`)
5. **Push** to branch (`git push origin feature/awesome-feature`)
6. **Open** Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/aingelmo/HCGateway-dashboard/issues)
- **Email**: <aingelmo@gmail.com>

---

Built with ⚡ Ruff optimization and 🛡️ enterprise-grade quality control
