# Makefile for pigame project

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm
PREFIX ?= /usr/local

all: build

build: build-c

build-c:
	$(CC) $(CFLAGS) -o src/c/pigame src/c/pigame.c $(LDFLAGS)

test: test-bash test-c test-python

test-bash:
	@echo "Testing Bash implementation..."
	@chmod +x src/bash/pigame.sh
	@./src/bash/pigame.sh -V
	@./src/bash/pigame.sh -v 3.14
	@echo "Bash tests passed"

test-c: build-c
	@echo "Testing C implementation..."
	@./src/c/pigame -V
	@./src/c/pigame -v 3.14
	@echo "C tests passed"

test-python:
	@echo "Testing Python implementation..."
	@chmod +x src/python/pigame.py
	@./src/python/pigame.py -V
	@./src/python/pigame.py -v 3.14
	@echo "Python tests passed"

lint-bash:
	@echo "Linting Bash implementation..."
	shellcheck src/bash/pigame.sh

lint-python:
	@echo "Linting Python implementation..."
	@if command -v pylint >/dev/null; then \
		pylint src/python/pigame.py; \
	else \
		echo "pylint not installed, skipping"; \
	fi

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

.PHONY: all build build-c test test-bash test-c test-python lint lint-bash lint-python install uninstall clean