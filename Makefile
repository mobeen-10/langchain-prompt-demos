.PHONY: deps deps-upgrade deps-compile compile-root compile-root-upgrade sync-root ensure-in-root pip-tools

# Absolute paths to virtual environments
ROOT_VENV=/Users/mobeenashraf/Desktop/ai-training/env

# Tool binaries (no need to activate venvs)
ROOT_PIP_COMPILE=$(ROOT_VENV)/bin/pip-compile
ROOT_PIP_SYNC=$(ROOT_VENV)/bin/pip-sync

# Optional: ensure pip-tools are installed in both envs
pip-tools:
	$(ROOT_VENV)/bin/python -m pip install --upgrade pip pip-tools

# Ensure .in files exist (created from current .txt if missing)
ensure-in-root:
	@test -f requirements.in || cp requirements.txt requirements.in

# Compile locked requirements (no version bump)
compile-root: ensure-in-root
	$(ROOT_PIP_COMPILE) --generate-hashes --resolver=backtracking --strip-extras \
	  -o requirements.txt requirements.in

# Compile and upgrade to latest allowed by resolvers
compile-root-upgrade: ensure-in-root
	$(ROOT_PIP_COMPILE) --upgrade --generate-hashes --resolver=backtracking --strip-extras \
	  -o requirements.txt requirements.in

# Sync environments exactly to compiled requirements
sync-root:
	$(ROOT_PIP_SYNC) requirements.txt

# High-level tasks
deps: sync-root

deps-compile: compile-root

deps-upgrade: compile-root-upgrade sync-root


