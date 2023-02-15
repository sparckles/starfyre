# internal values
RED='\033[0;31m'
YEL='\033[1;33m'
WHITE='\033[0;37m'
NO_COL='\033[0m'

# cool colors!
STARFYRE="${YEL}star${RED}fyre${NO_COL}"

default: help


.PHONY: preinstall
preinstall: # Sets up python virtual environment
	@echo "create-${STARFYRE}-app: preparing python virtual environment (venv)"
	@python3.10 -m venv .venv
	@echo "create-${STARFYRE}-app: preinstall environment ready"


.PHONY: install
install: # Prepares the build environment, calls preinstall if you have not*
	@[ -e .venv/bin/python ] || $(MAKE) preinstall
	@echo "create-${STARFYRE}-app: installing dev dependencies"
	@.venv/bin/python -m pip install -r requirements-dev.txt
	@echo "create-${STARFYRE}-app: dev environment prepared"

.PHONY: build
build: # Builds the test-application
	@echo "create-${STARFYRE}-app: building"
	@.venv/bin/python -m poetry build
	@echo "create-${STARFYRE}-app: build complete"


.PHONY: start
start: # Starts the test-application
	@echo  "create-${STARFYRE}-app @ ${WHITE}http://localhost:8000/public/${NO_COL}"
	@.venv/bin/python -m http.server


.PHONY: dev
dev: # Builds and starts the application
	@[ -e .venv/bin/python ] || $(MAKE) install
	@$(MAKE) build
	@$(MAKE) start


.PHONY: clean
clean: # Removes the preinstall environment
	@echo "create-${STARFYRE}-app: removing preinstall environment"
	@rm -rf .venv/
	@echo "create-${STARFYRE}-app: Done. please run make install now"


.PHONY: help
help: # Shows `make` help commands and ARGS
	@echo "Welcome to create-${STARFYRE}-app!"
	@echo "make [command]"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	@echo "make [command] ARGS"
	@grep -E '^[a-zA-Z0-9 _-]+[?].*'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d'?')\033[00m:$$(echo $$l | cut -f 2- -d'?')\n"; done
