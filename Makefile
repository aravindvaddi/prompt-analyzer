# Prompt Analyzer - Developer Makefile
# Built with ❤️ by Quinn

# Colors for pretty output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

.PHONY: install
install: ## Install all dependencies (backend + frontend)
	@echo "$(YELLOW)Installing backend dependencies with uv...$(NC)"
	cd backend && uv pip install -r requirements.txt
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)✓ All dependencies installed!$(NC)"

.PHONY: dev
dev: ## Start development environment (all services)
	@echo "$(YELLOW)Starting development environment...$(NC)"
	docker-compose up -d redis
	@echo "$(GREEN)✓ Redis started$(NC)"
	@make -j2 dev-backend dev-frontend

.PHONY: dev-backend
dev-backend: ## Start backend with hot reload
	cd backend && uv run uvicorn main:app --reload --port 8000

.PHONY: dev-frontend
dev-frontend: ## Start frontend with hot reload
	cd frontend && npm run dev

.PHONY: format
format: ## Format all code with ruff and prettier
	@echo "$(YELLOW)Formatting Python code with ruff...$(NC)"
	cd backend && ruff format .
	@echo "$(YELLOW)Formatting JavaScript code with prettier...$(NC)"
	cd frontend && npm run format
	@echo "$(GREEN)✓ All code formatted!$(NC)"

.PHONY: lint
lint: ## Lint all code
	@echo "$(YELLOW)Linting Python code with ruff...$(NC)"
	cd backend && ruff check . --fix
	@echo "$(YELLOW)Linting JavaScript code...$(NC)"
	cd frontend && npm run lint
	@echo "$(GREEN)✓ All code linted!$(NC)"

.PHONY: test
test: ## Run all tests
	@echo "$(YELLOW)Running backend tests...$(NC)"
	cd backend && uv run pytest
	@echo "$(YELLOW)Running frontend tests...$(NC)"
	cd frontend && npm test
	@echo "$(GREEN)✓ All tests passed!$(NC)"

.PHONY: analyze
analyze: ## Test the analysis engine from CLI
	@echo "$(YELLOW)Testing prompt analysis...$(NC)"
	@read -p "Enter prompt to analyze: " prompt; \
	cd backend && uv run python -c "from analyzer import analyze_prompt; import asyncio; asyncio.run(analyze_prompt('$$prompt'))"

.PHONY: build
build: ## Build production containers
	@echo "$(YELLOW)Building production containers...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Containers built!$(NC)"

.PHONY: up
up: ## Start production environment
	docker-compose up -d
	@echo "$(GREEN)✓ Production environment started!$(NC)"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"

.PHONY: down
down: ## Stop all services
	docker-compose down
	@echo "$(GREEN)✓ All services stopped!$(NC)"

.PHONY: logs
logs: ## Show logs from all services
	docker-compose logs -f

.PHONY: clean
clean: ## Clean up generated files and caches
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

.PHONY: setup-env
setup-env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ Created .env file. Please add your CLAUDE_API_KEY!$(NC)"; \
	else \
		echo "$(YELLOW).env file already exists$(NC)"; \
	fi

.PHONY: check-env
check-env: ## Verify environment is properly configured
	@echo "$(YELLOW)Checking environment...$(NC)"
	@which uv > /dev/null || (echo "❌ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	@which ruff > /dev/null || (echo "❌ ruff not found. Install with: pip install ruff" && exit 1)
	@which node > /dev/null || (echo "❌ node not found. Install Node.js 18+" && exit 1)
	@which docker > /dev/null || (echo "❌ docker not found. Install Docker" && exit 1)
	@echo "$(GREEN)✓ All tools installed!$(NC)"

# Default target
.DEFAULT_GOAL := help
