.DEFAULT_GOAL := help
PYTHON ?= python3
WORKSPACE ?= $(CURDIR)
INSTALL_HOME ?= $(HOME)
CODEX_DIR ?= $(if $(CODEX_HOME),$(CODEX_HOME),$(INSTALL_HOME)/.codex)
EVAL_DIR ?= /tmp/codex-workflow-evaluation
CODEX_BIN ?= codex
UPSTREAM_CHECKOUT ?=
TICKET ?=
INSTRUCTIONS ?=
override TICKET := $(value TICKET)
override INSTRUCTIONS := $(value INSTRUCTIONS)
export PYTHON WORKSPACE INSTALL_HOME CODEX_DIR EVAL_DIR CODEX_BIN UPSTREAM_CHECKOUT TICKET INSTRUCTIONS

.PHONY: help install update install-global update-global test check smoke fixtures diff-upstream run
help:
	@echo 'make install [WORKSPACE="/path with spaces"]  Install at a workspace root'
	@echo 'make update [WORKSPACE="/path"]              Reinstall authoritative kit files'
	@echo 'make install-global                         Install for your user'
	@echo 'make update-global                          Reinstall global kit files'
	@echo 'make test                                   Run installer integration tests'
	@echo 'make check                                  Test and validate all kit sources'
	@echo 'make smoke                                  Check installed Codex discovery in isolation'
	@echo 'make fixtures [EVAL_DIR="/tmp/path"]         Prepare disposable workflow scenarios'
	@echo 'make diff-upstream                          Show every fork change against pinned upstream'
	@echo 'make run TICKET="URL-or-ID"                 Open Codex with the development loop'
	@echo 'Edit kit/agents, kit/skills and manifest.json; run make update to apply changes.'

install update:
	@sh scripts/install.sh --workspace "$$WORKSPACE"

install-global update-global:
	@sh scripts/install.sh --global --home "$$INSTALL_HOME" --codex-home "$$CODEX_DIR"

test:
	@"$$PYTHON" -m unittest discover -s tests -v

check: test
	@"$$PYTHON" scripts/validate.py

smoke:
	@"$$PYTHON" scripts/smoke.py

fixtures:
	@"$$PYTHON" scripts/fixtures.py "$$EVAL_DIR"

diff-upstream:
	@if [ -n "$$UPSTREAM_CHECKOUT" ]; then "$$PYTHON" scripts/diff_upstream.py --checkout "$$UPSTREAM_CHECKOUT"; else "$$PYTHON" scripts/diff_upstream.py; fi

run:
	@test -n "$$TICKET" || { echo 'Provide TICKET="URL-or-ID" and optional INSTRUCTIONS="...".' >&2; exit 1; }
	@"$$CODEX_BIN" -C "$$WORKSPACE" "\$$development-loop $$TICKET $$INSTRUCTIONS"
