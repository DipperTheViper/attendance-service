# Variables
PYTHON := poetry run
POETRY := poetry
PRE_COMMIT := poetry run pre-commit
PROJECT_NAME := tether-gate-back
PYTHON_FILES := $(PROJECT_NAME) tests scripts

# Colors for terminal output
BLUE := \033[1;34m
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo 'Usage:'
	@echo "${BLUE}make${NC} ${GREEN}<target>${NC}"
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\-_0-9]+:.*?## / {printf "  ${BLUE}%-20s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Setup project pre-requisites
	@echo "${BLUE}Setup project pre-requisites...${NC}"
	@echo "${GREEN}Installing poetry (may need your sudo password)...${NC}"
	sudo apt install pipx
	pipx install poetry
	poetry completions bash >> ~/.bash_completion

.PHONY: install
install: ## Install project dependencies
	@echo "${BLUE}Installing project dependencies...${NC}"
	$(POETRY) install
	$(PRE_COMMIT) install

.PHONY: update
update: ## Update dependencies to their latest versions
	@echo "${BLUE}Updating dependencies...${NC}"
	$(POETRY) update

.PHONY: clean
clean: ## Remove build artifacts and cache directories
	@echo "${BLUE}Cleaning project...${NC}"
	rm -rf dist/
	rm -rf build/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: format
format: ## Format code using black and isort
	@echo "${BLUE}Formatting code...${NC}"
	$(PYTHON) black --config pyproject.toml $(PYTHON_FILES)
	$(PYTHON) isort $(PYTHON_FILES)

.PHONY: lint
lint: ## Run all linters
	@echo "${BLUE}Running linters...${NC}"
	$(PYTHON) black --config pyproject.toml --check $(PYTHON_FILES)
	$(PYTHON) isort --check-only $(PYTHON_FILES)
	$(PYTHON) autoflake --config pyproject.toml  $(PYTHON_FILES)
	$(PYTHON) ruff check --config pyproject.toml  $(PYTHON_FILES)
	$(PYTHON) mypy --config-file pyproject.toml $(PYTHON_FILES)
	$(PYTHON) bandit -r $(PROJECT_NAME)

.PHONY: test
test: ## Run tests with pytest
	@echo "${BLUE}Running tests...${NC}"
	$(PYTHON) behave

.PHONY: version
version: ## Display current version
	@echo "${BLUE}Current version:${NC}"
	@$(POETRY) version
	@echo "${YELLOW}Current tag (Fetching...):${NC}"
	@git fetch && git describe --tags --abbrev=0

.PHONY: bump-patch
bump-patch: ## Bump patch version (use env=dev/test for environment suffix)
	@echo "${BLUE}Bumping patch version...${NC}"
	@if [ -n "$(message)" ]; then \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py patch -m "$(message)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py patch -m "$(message)"; \
		fi \
	else \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py patch -m "$$(git log -1 --pretty=%s)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py patch -m "$$(git log -1 --pretty=%s)"; \
		fi \
	fi

.PHONY: bump-minor
bump-minor: ## Bump minor version (use env=dev/test for environment suffix)
	@echo "${BLUE}Bumping minor version...${NC}"
	@if [ -n "$(message)" ]; then \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py minor -m "$(message)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py minor -m "$(message)"; \
		fi \
	else \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py minor -m "$$(git log -1 --pretty=%s)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py minor -m "$$(git log -1 --pretty=%s)"; \
		fi \
	fi

.PHONY: bump-major
bump-major: ## Bump major version (use env=dev/test for environment suffix)
	@echo "${BLUE}Bumping major version...${NC}"
	@if [ -n "$(message)" ]; then \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py major -m "$(message)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py major -m "$(message)"; \
		fi \
	else \
		if [ -n "$(env)" ]; then \
			$(PYTHON) python scripts/bump_version.py major -m "$$(git log -1 --pretty=%s)" --suffix "$(env)"; \
		else \
			$(PYTHON) python scripts/bump_version.py major -m "$$(git log -1 --pretty=%s)"; \
		fi \
	fi

.PHONY: bump-suffix
bump-suffix: ## Change only the version suffix (use env=dev/test)
	@if [ -z "$(env)" ]; then \
		echo "${RED}Error: env variable must be set (e.g., env=dev or env=test)${NC}"; \
		exit 1; \
	fi
	@echo "${BLUE}Changing version suffix to $(env)...${NC}"
	@if [ -n "$(message)" ]; then \
		$(PYTHON) python scripts/bump_version.py suffix -m "$(message)" --suffix "$(env)"; \
	else \
		$(PYTHON) python scripts/bump_version.py suffix -m "$$(git log -1 --pretty=%s)" --suffix "$(env)"; \
	fi

.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "${BLUE}Building Docker image...${NC}"
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run: ## Run Docker container
	@echo "${BLUE}Running Docker container...${NC}"
	docker run -it --rm $(PROJECT_NAME)

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	@echo "${BLUE}Running pre-commit hooks...${NC}"
	$(PRE_COMMIT) run --all-files

.PHONY: check
check: lint test ## Run all checks (linting and tests)

.PHONY: ci
ci: ## Run CI pipeline locally
	@echo "${BLUE}Running CI pipeline...${NC}"
	$(MAKE) clean
	$(MAKE) install
	$(MAKE) lint
	$(MAKE) test

.DEFAULT_GOAL := help
