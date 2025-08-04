# HCGateway Dashboard - Simple Quality Control

.PHONY: help install test lint format clean check

help: ## Show available commands
	@echo "🚀 HCGateway Dashboard"
	@echo "===================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "🔧 Installing dependencies..."
	uv sync
	@echo "✅ Installation complete"

format: ## Format and fix code issues
	@echo "🎨 Formatting code..."
	uv run ruff format .
	uv run ruff check . --fix
	@echo "✅ Code formatted"

lint: ## Check code quality
	@echo "🔍 Checking code..."
	uv run ruff check .
	@echo "✅ Code checked"

test: ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest
	@echo "✅ Tests passed"

clean: ## Clean generated files
	@echo "🧹 Cleaning..."
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

# Simple quality check for beta
check: format lint test ## Run basic quality checks
	@echo "✅ Quality checks passed!"
