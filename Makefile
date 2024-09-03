
ifdef VERBOSE
	ifneq ($(VERBOSE),0)
		Q =
		QUIET =
	else
		Q = @
		QUIET = --quiet
	endif
else
	Q = @
	QUIET = --quiet
endif

VENV_DIR = $(CURDIR)/venv

.PHONY: virtualenv test build clean help

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

venv: ## Create a virtual env and install requirements
	@echo "Generating virtual environment..."
	$(Q)python3 -m virtualenv $(QUIET) $(VENV_DIR)
	@echo "Virtual environement generated !"
	@echo "  -> activate venv  : source $(VENV_DIR)/bin/activate"
	@echo "  -> deactivate venv: deactivate"

test: ## Test the code with pytest
	$(Q)poetry install
	$(Q)poetry run tox

build: ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

clean: ## Remove files not in source control
	@echo "🚀 Cleanup..."
	$(Q)git clean -xdf
	$(Q)rm -rf $(VENV_DIR)
