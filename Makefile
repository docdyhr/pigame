# Makefile for pigame project

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = 
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
		$(CC) $(CFLAGS) -o src/c/pigame src/c/pigame.c; \
	else \
		echo "C compiler not found, skipping C build"; \
	fi

test:
	@./scripts/run_tests.sh

test-bash:
	@./scripts/run_tests.sh --no-c --no-python --no-coverage

test-c: build-c
	@./scripts/run_tests.sh --no-bash --no-python --no-coverage

test-python:
	@./scripts/run_tests.sh --no-bash --no-c --no-coverage

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
	@./scripts/run_tests.sh --no-bash --no-c

test-all:
	@./scripts/run_tests.sh

lint-bash:
	@./scripts/lint.sh

setup-python: requirements.txt
	@./scripts/setup.sh

lint-python:
	@./scripts/lint.sh

lint:
	@./scripts/lint.sh

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

.PHONY: all build build-c test test-bash test-c test-python test-pytest coverage lint lint-bash lint-python install uninstall clean setup-python
