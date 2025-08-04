# HCGateway Dashboard - Ruff-Optimized Quality Control
# Leverages Ruff for maximum performance and consistency

.PHONY: help install test lint format security type-check clean quality-gate

help: ## Show available commands
	@echo "� HCGateway Dashboard - Ruff-Optimized Quality Control"
	@echo "======================================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies and setup pre-commit
	@echo "🔧 Installing dependencies..."
	uv sync --all-extras
	uv run pre-commit install
	@echo "✅ Installation complete"

# Core quality targets using Ruff
format: ## Format code with Ruff (replaces black, isort)
	@echo "🎨 Formatting code with Ruff..."
	uv run ruff format .
	uv run ruff check . --fix --exit-zero
	@echo "✅ Code formatted"

lint: ## Lint code with Ruff (replaces flake8, pydocstyle, etc.)
	@echo "🔍 Linting with Ruff..."
	uv run ruff check . --exit-zero
	@echo "✅ Linting complete"

type-check: ## Type checking with MyPy
	@echo "🔍 Type checking..."
	uv run mypy src
	@echo "✅ Type checking passed"

security: ## Security scanning with Bandit
	@echo "🛡️ Security scanning..."
	uv run bandit -r src/ -c pyproject.toml
	uv run detect-secrets scan --baseline .secrets.baseline
	@echo "✅ Security scan complete"

test: ## Run tests with coverage
	@echo "🧪 Running tests..."
	uv run pytest
	@echo "✅ Tests passed"

# Comprehensive quality gate
quality-gate: format lint type-check security test ## Run all quality checks
	@echo ""
	@echo "🎉 QUALITY GATE PASSED! 🎉"
	@echo "Your code meets perfection standards!"

# Pre-commit integration
pre-commit: ## Run pre-commit hooks
	@echo "🚀 Running pre-commit hooks..."
	uv run pre-commit run --all-files

# Development helpers
clean: ## Clean generated files
	@echo "🧹 Cleaning..."
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

dev: install ## Setup development environment
	@echo "🚀 Development environment ready!"

# CI/CD targets
ci: ## CI pipeline (format check, lint, type check, test)
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy src
	uv run pytest --cov=hcgateway_dashboard

# Documentation
docs: ## Generate documentation
	@echo "📚 Documentation available in README.md and PRE_COMMIT_GUIDE.md"

# Emergency override (use with extreme caution)
emergency-commit: ## EMERGENCY: Bypass pre-commit hooks (USE ONLY IN DIRE SITUATIONS)
	@echo "⚠️  EMERGENCY COMMIT - BYPASSING QUALITY GATES ⚠️"
	@echo "This action may compromise code quality!"
	@read -p "Are you absolutely sure? (type 'I ACCEPT THE RISK'): " confirm; \
	if [ "$$confirm" = "I ACCEPT THE RISK" ]; then \
		git commit --no-verify; \
		echo "💥 Emergency commit completed - REVIEW AND FIX IMMEDIATELY"; \
	else \
		echo "❌ Emergency commit cancelled - Good choice!"; \
	fi
