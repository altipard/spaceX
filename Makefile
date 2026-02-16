.DEFAULT_GOAL := help

# --- Project Setup ---

.PHONY: install
install: ## Install all dependencies (including dev)
	uv sync

.PHONY: lock
lock: ## Regenerate uv.lock from pyproject.toml
	uv lock

.PHONY: upgrade
upgrade: ## Upgrade all dependencies
	uv lock --upgrade && uv sync

# --- Development ---

.PHONY: run
run: ## Start dev server with auto-reload
	uv run uvicorn app.main:app --reload

# --- Testing ---

.PHONY: test
test: ## Run all tests
	uv run pytest

.PHONY: test-v
test-v: ## Run tests with verbose output
	uv run pytest -v

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	uv run pytest --cov=app --cov-report=term-missing

# --- Linting & Formatting ---

.PHONY: lint
lint: ## Run ruff linter
	uv run ruff check .

.PHONY: format
format: ## Format code with ruff
	uv run ruff format .

.PHONY: fix
fix: ## Auto-fix lint issues and format
	uv run ruff check . --fix && uv run ruff format .

# --- Helpers ---

.PHONY: clean
clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
