# Makefile for pigame project

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm
PREFIX ?= /usr/local

all: build

build:
	@if command -v $(CC) >/dev/null 2>&1; then \
		$(MAKE) build-c; \
	else \
		echo "C compiler not found, skipping C build"; \
	fi

build-c:
	@if command -v $(CC) >/dev/null 2>&1; then \
		$(CC) $(CFLAGS) -o src/c/pigame src/c/pigame.c $(LDFLAGS); \
	else \
		echo "C compiler not found, skipping C build"; \
	fi

test: test-bash test-c test-python test-all

test-bash:
	@echo "Testing Bash implementation..."
	@chmod +x src/bash/pigame.sh 2>/dev/null || true
	@chmod +x tests/test_bash.sh 2>/dev/null || true
	@if command -v bash >/dev/null 2>&1; then \
		tests/test_bash.sh; \
	else \
		echo "Bash not found, skipping test"; \
	fi

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
	@if [ -f .venv/bin/python ]; then \
		.venv/bin/python -m pytest; \
	elif [ -f .venv/Scripts/python.exe ]; then \
		.venv/Scripts/python -m pytest; \
	else \
		echo "Virtual environment not found"; \
		exit 1; \
	fi

coverage:
	@echo "Running tests with coverage..."
	@if [ -f .venv/bin/python ]; then \
		.venv/bin/python -m pytest tests/test_pytest.py -v --cov=src/python --cov-report=term-missing --cov-report=html --cov-report=xml; \
	elif [ -f .venv/Scripts/python.exe ]; then \
		.venv/Scripts/python -m pytest tests/test_pytest.py -v --cov=src/python --cov-report=term-missing --cov-report=html --cov-report=xml; \
	else \
		echo "Virtual environment not found"; \
		exit 1; \
	fi

test-all:
	@echo "Running all tests..."
	@chmod +x tests/run_tests.sh
	@tests/run_tests.sh

lint-bash:
	@echo "Linting Bash implementation..."
	shellcheck src/bash/pigame.sh

setup-python: requirements.txt
	@echo "Setting up Python environment..."
	@if [ -f .venv/bin/pip ]; then \
		.venv/bin/pip install -r requirements.txt && \
		.venv/bin/pip install -e .; \
	elif [ -f .venv/Scripts/pip.exe ]; then \
		.venv/Scripts/pip install -r requirements.txt && \
		.venv/Scripts/pip install -e .; \
	else \
		echo "Virtual environment not found"; \
		exit 1; \
	fi

lint-python:
	@echo "Linting Python implementation with Ruff..."
	@ruff check src/python/ tests/

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

.PHONY: all build build-c test test-bash test-c test-python test-pytest coverage lint lint-bash lint-python install uninstall clean
