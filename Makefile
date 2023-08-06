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

MKFILE_PATH := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
include $(MKFILE_PATH)/mk/Makefile.defs

virtualenv:
	@echo "Generating virtual environment..."
	$(Q)python3 -m virtualenv $(QUIET) $(VENV_DIR)
	@echo "Virtual environement generated !"
	@echo "  -> activate venv  : source $(VENV_DIR)/bin/activate"
	@echo "  -> deactivate venv: deactivate"

setup:
	$(Q)pip install $(QUIET) -r requirements-dev.txt

test:
	$(Q)poetry install
	$(Q)poetry run tox

clean:
	@echo "Cleanup..."
	$(Q)git clean -xdf
	$(Q)rm -rf $(VENV_DIR)

all: test \
	clean

