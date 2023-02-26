RUSTUP_TOOLCHAIN ?= nightly
OUTPUT_DIR ?= dist

# internal values
RED='\033[0;31m'
YEL='\033[1;33m'
NO_COL='\033[0m'

# cool colors!
STARFYRE="${YEL}star${RED}fyre${NO_COL}"


default: help


.PHONY: dep-check
dep-check: # Checks that you have the pre-requisite environment

	@[ $(shell which python3.10) ] || (echo "python3.10 is not available. To get started, see: https://realpython.com/installing-python/"; exit 1)
	@[ $(shell which rustup) ] || (echo "rustup is not available. To get started, see: https://doc.rust-lang.org/cargo/getting-started/installation.html"; exit 1)
	@[ $(shell which cargo) ] || (echo "rustup is not available. To get started, see: https://doc.rust-lang.org/cargo/getting-started/installation.html"; exit 1)
# we (maturin?) needs `emcc` at some stage in the compilation.
# will not error for now...
	@[ $(shell which emcc) ] || echo "${STARFYRE}: WARNING! emcc is not available. To get started, see: https://emscripten.org/docs/getting_started/downloads.html"


.PHONY: preinstall
preinstall: # Sets up build environment
	@$(MAKE) dep-check
	@$(MAKE) clean
	@echo "${STARFYRE}: preparing python virtual environment (venv)"
	@python3.10 -m venv .venv
	@echo "${STARFYRE}: preinstall environment ready"


.PHONY: install
install: # Prepares the build environment, calls preinstall if you have not*
	@[ -e .venv/bin/python ] || $(MAKE) preinstall
	@echo "${STARFYRE}: installing dev dependencies"
	@.venv/bin/python -m pip install -r requirements-dev.txt
	@echo "${STARFYRE}: dev environment prepared"


.PHONY: build
build: # Builds the application to `OUTPUT_DIR`, using `RUSTUP_TOOLCHAIN`
	@$(MAKE) dep-check
	@[ -e .venv/bin/python ] || $(MAKE) install
	@echo "${STARFYRE}: building to ${OUTPUT_DIR}"
	@mkdir -p ${OUTPUT_DIR}
	@RUSTUP_TOOLCHAIN=${RUSTUP_TOOLCHAIN} .venv/bin/maturin build --target wasm32-unknown-emscripten -i python3.10 --out ${OUTPUT_DIR}
	@echo "${STARFYRE}: build available @ ${OUTPUT_DIR}/"


.PHONY: dev
dev: # Runs `test-application` built with the current `OUTPUT_DIR` starfyre
# FIXME - this works because of a hack in how ./test-application/public/index.html 
# `micro-pip` installs the .whl's, version mismatches will lead to unexpected result.
	@echo "${STARFYRE}: packaging dev-starfyre @ ${OUTPUT_DIR}/ into ./test-application"
	@mkdir -p ./test-application/starfyre-dist
	@cp -R ${OUTPUT_DIR}/* ./test-application/starfyre-dist/
	@cd test-application && $(MAKE) dev


.PHONY: in-dev
in-dev: # Builds `starfyre` and injects into a running `test-application`
# similar to `dev`, but builds first
	@$(MAKE) build
	@$(MAKE) dev


.PHONY: clean
clean: # Removes the preinstall environment
	@echo "${STARFYRE}: removing preinstall environment"
	@rm -rf .venv/
	@echo "${STARFYRE}: Done. please run make install now"


.PHONY: dep-check-ci
dep-check-ci:
	@[ $(shell which tox) ] || (echo "tox is not available. run python3.10 -m pip install tox"; exit 1)


.PHONY: format
format: # Formats source code
	@echo "${STARFYRE}: Formatting source code"
	@$(MAKE) dep-check-ci
# format python code
	@tox -e format


.PHONY: ruff
ruff: # ruff source code
	@$(MAKE) dep-check-ci
	@tox -e ruff


.PHONY: lint
lint: # lint source code
	@echo "${STARFYRE}: Performing lint check against source code"
	@$(MAKE) dep-check-ci
# lint python code
	@$(MAKE) ruff


.PHONY: help
help: # Shows `make` help commands and ARGS
	@echo "Welcome to ${STARFYRE}!"
	@echo "make [command]"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	@echo "make [command] ARGS"
	@grep -E '^[a-zA-Z0-9 _-]+[?].*'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d'?')\033[00m:$$(echo $$l | cut -f 2- -d'?')\n"; done
