.DEFAULT_GOAL := help
PYTHON ?= python3
WORKSPACE ?= $(CURDIR)
INSTALL_HOME ?= $(HOME)
CODEX_DIR ?= $(if $(CODEX_HOME),$(CODEX_HOME),$(INSTALL_HOME)/.codex)
EVAL_DIR ?= /tmp/codex-workflow-evaluation
CODEX_BIN ?= codex
AGENT ?= all
TICKET ?=
INSTRUCTIONS ?=
override TICKET := $(value TICKET)
override INSTRUCTIONS := $(value INSTRUCTIONS)
export PYTHON WORKSPACE INSTALL_HOME CODEX_DIR EVAL_DIR CODEX_BIN AGENT TICKET INSTRUCTIONS

.PHONY: help install update install-global update-global test check smoke fixtures bump run
help:
	@echo 'make install [WORKSPACE="/path"] [AGENT=codex|claude|all]  Install at a workspace root'
	@echo 'make update [WORKSPACE="/path"]              Reinstall authoritative kit files'
	@echo 'make install-global                         Install for your user'
	@echo 'make update-global                          Reinstall global kit files'
	@echo 'make test                                   Run installer integration tests'
	@echo 'make check                                  Test and validate all kit sources'
	@echo 'make smoke                                  Check installed Codex discovery in isolation'
	@echo 'make fixtures [EVAL_DIR="/tmp/path"]         Prepare disposable workflow scenarios'
	@echo 'make bump                                   Pin every upstream source to its latest commit'
	@echo 'make run TICKET="URL-or-ID"                 Open Codex with the dev loop'
	@echo 'Edit kit/agents, kit/skills and sources.json; run make update to apply changes.'

install update:
	@sh scripts/install.sh --workspace "$$WORKSPACE" --agent "$$AGENT"

install-global update-global:
	@sh scripts/install.sh --global --home "$$INSTALL_HOME" --codex-home "$$CODEX_DIR" --agent "$$AGENT"

test:
	@"$$PYTHON" -m unittest discover -s tests -v

check: test
	@"$$PYTHON" scripts/validate.py

smoke:
	@"$$PYTHON" scripts/smoke.py

fixtures:
	@"$$PYTHON" scripts/fixtures.py "$$EVAL_DIR"

bump:
	@"$$PYTHON" scripts/bump.py

run:
	@test -n "$$TICKET" || { echo 'Provide TICKET="URL-or-ID" and optional INSTRUCTIONS="...".' >&2; exit 1; }
	@"$$CODEX_BIN" -C "$$WORKSPACE" "\$$dev-loop $$TICKET $$INSTRUCTIONS"
