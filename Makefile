# Makefile for pigame project

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm -lgmp
PREFIX ?= /usr/local

all: build

build: build-c

build-c:
	$(CC) $(CFLAGS) -o src/c/pigame src/c/pigame.c $(LDFLAGS)

test: test-bash test-c test-python test-all

test-bash:
	@echo "Testing Bash implementation..."
	@chmod +x src/bash/pigame.sh
	@chmod +x tests/test_bash.sh
	@tests/test_bash.sh

test-c: build-c
	@echo "Testing C implementation..."
	@chmod +x tests/test_c.sh
	@tests/test_c.sh

test-python:
	@echo "Testing Python implementation..."
	@chmod +x src/python/pigame.py
	@chmod +x tests/test_python.sh
	@tests/test_python.sh

test-python-unit:
	@echo "Running Python unit tests..."
	@python3 tests/test_python_unit.py -v
	
test-pytest:
	@echo "Running pytest tests..."
	@.venv/bin/pytest

test-all:
	@echo "Running all tests..."
	@chmod +x tests/run_tests.sh
	@tests/run_tests.sh

lint-bash:
	@echo "Linting Bash implementation..."
	shellcheck src/bash/pigame.sh

setup-python: requirements.txt
	@echo "Setting up Python environment..."
	@.venv/bin/pip install -r requirements.txt
	@.venv/bin/pip install -e .

lint-python:
	@echo "Linting Python implementation..."
	@.venv/bin/pylint src/python/pigame.py tests/test_pytest.py || true
	@echo "Running flake8..."
	@.venv/bin/flake8 src/python/pigame.py tests/test_pytest.py || true
	@echo "Running mypy..."
	@.venv/bin/mypy src/python/pigame.py tests/test_pytest.py || true

lint: lint-bash lint-python

install:
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@cp pigame $(DESTDIR)$(PREFIX)/bin/
	@mkdir -p $(DESTDIR)$(PREFIX)/share/pigame
	@cp -r src $(DESTDIR)$(PREFIX)/share/pigame/
	@chmod +x $(DESTDIR)$(PREFIX)/bin/pigame
	@mkdir -p $(DESTDIR)$(PREFIX)/share/man/man1
	@cp man/pigame.1 $(DESTDIR)$(PREFIX)/share/man/man1/
	@echo "Installation complete. Run 'pigame' to start the game."

uninstall:
	@rm -f $(DESTDIR)$(PREFIX)/bin/pigame
	@rm -rf $(DESTDIR)$(PREFIX)/share/pigame
	@rm -f $(DESTDIR)$(PREFIX)/share/man/man1/pigame.1
	@echo "Uninstallation complete."

clean:
	@rm -f src/c/pigame
	@echo "Cleaned build files."

# Version management targets
version-major:
	@./version.sh major

version-minor:
	@./version.sh minor

version-patch:
	@./version.sh patch

release: version-patch
	@VERSION=$$(cat src/VERSION); \
	echo "Preparing release for version $$VERSION"; \
	git add src/VERSION CHANGELOG.md; \
	git commit -m "Release version $$VERSION"; \
	git tag -a v$$VERSION -m "Version $$VERSION"; \
	echo "Version $$VERSION prepared for release. Push with: git push && git push --tags"

.PHONY: all build build-c test test-bash test-c test-python lint lint-bash lint-python install uninstall clean