#!/usr/bin/env bash

# Script to test the release process locally
# Usage: ./test-release.sh

set -e

echo "Testing release process..."

# Create a temporary directory for testing
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Created temp directory: $TEMP_DIR"

# Create release artifacts
mkdir -p "$TEMP_DIR/dist"
echo "Creating tarball..."
tar -czf "$TEMP_DIR/dist/pigame-test.tar.gz" --exclude='.git' --exclude='dist' .
echo "Creating zip file..."
zip -r "$TEMP_DIR/dist/pigame-test.zip" . -x "*.git*" "dist/*" >/dev/null

# Extract and test tarball
echo "Testing tarball extraction..."
mkdir -p "$TEMP_DIR/tarball-test"
tar -xzf "$TEMP_DIR/dist/pigame-test.tar.gz" -C "$TEMP_DIR/tarball-test"

# Test basic functionality
echo "Testing basic functionality from tarball..."
(cd "$TEMP_DIR/tarball-test" && make build)
(cd "$TEMP_DIR/tarball-test" && ./pigame -V)

# Extract and test zip
echo "Testing zip extraction..."
mkdir -p "$TEMP_DIR/zip-test"
unzip -q "$TEMP_DIR/dist/pigame-test.zip" -d "$TEMP_DIR/zip-test"

# Test basic functionality
echo "Testing basic functionality from zip..."
(cd "$TEMP_DIR/zip-test" && make build)
(cd "$TEMP_DIR/zip-test" && ./pigame -V)

echo "All tests passed!"
echo "Release artifacts look good!"
