RUSTUP_TOOLCHAIN ?= nightly
OUTPUT_DIR ?= dist

# internal values
RED='\033[0;31m'
YEL='\033[1;33m'
NO_COL='\033[0m'

# cool colors!
STARFYRE="${YEL}star${RED}fyre${NO_COL}"

default: help

# TODO
# preinstall: # Sets up build environment.
# install: # Prepares the build evironment, calls preinstall if you have not*.
# clean: # Removes the preinstall environment

.PHONY: build
build: # Builds the application to `OUTPUT_DIR`, using `RUSTUP_TOOLCHAIN`
	@echo "${STARFYRE}: building to ${OUTPUT_DIR}"
	@mkdir -p ${OUTPUT_DIR}
	RUSTUP_TOOLCHAIN=${RUSTUP_TOOLCHAIN} maturin build --target wasm32-unknown-emscripten -i python3.10 --out ${OUTPUT_DIR}
	@echo "${STARFYRE}: build available @ ${OUTPUT_DIR}/"


.PHONY: dev
dev: # Runs `test-application` built with the current `OUTPUT_DIR` starfyre
# FIXME - this works because of a hack in how ./test-application/public/index.html 
# `micro-pip` installs the .whl's, version mismatches will lead to unexpected result.
	@echo "${STARFYRE}: packaging dev-starfyre @ ${OUTPUT_DIR}/ into ./test-application"
	@cp -R ${OUTPUT_DIR}/* ./test-application/starfyre-dist/
	@cd test-application && $(MAKE) dev


.PHONY: in-dev
in-dev: # Builds `starfyre` and injects into a running `test-application`
# similar to `dev`, but builds first
	@$(MAKE) build
	@$(MAKE) dev


.PHONY: help
help: # Shows `make` help commands and ARGS
	@echo "Welcome to ${STARFYRE}!"
	@echo "make [command]"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	@echo "make [command] ARGS"
	@grep -E '^[a-zA-Z0-9 _-]+[?].*'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d'?')\033[00m:$$(echo $$l | cut -f 2- -d'?')\n"; done
