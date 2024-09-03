
.PHONY: virtualenv
virtualenv: ## Generating virtual environment
	@echo "Generating virtual environment..."
	$(Q)python3 -m virtualenv $(QUIET) $(VENV_DIR)
	@echo "Virtual environement generated !"
	@echo "  -> activate venv  : source $(VENV_DIR)/bin/activate"
	@echo "  -> deactivate venv: deactivate"

setup:
	$(Q)pip install $(QUIET) -r requirements-dev.txt

.PHONY: test
test: ## Test the code with pytest
	$(Q)poetry install
	$(Q)poetry run tox

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean
clean: ## cleanup
	@echo "Cleanup..."
	$(Q)git clean -xdf
	$(Q)rm -rf $(VENV_DIR)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


