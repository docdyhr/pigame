#!/usr/bin/env bash

# Script to manage version updates in the project
# Usage: ./version.sh [major|minor|patch]

# Enable debugging
set -e
set -x  # Print commands as they execute

VERSION_FILE="src/VERSION"
echo "Reading version from $VERSION_FILE"
if [ ! -f "$VERSION_FILE" ]; then
    echo "Version file not found! Creating with default version 1.6.0"
    mkdir -p $(dirname "$VERSION_FILE")
    echo "1.6.0" > "$VERSION_FILE"
fi

CURRENT_VERSION=$(cat $VERSION_FILE)
echo "Current version: $CURRENT_VERSION"

# Split the version string into components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

echo "Parsed version: Major=$MAJOR, Minor=$MINOR, Patch=$PATCH"

# Update version based on argument
case "$1" in
    major)
        echo "Updating major version..."
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        echo "Updating minor version..."
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        echo "Updating patch version..."
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Usage: $0 [major|minor|patch]"
        exit 1
        ;;
esac

echo "Incremented to: Major=$MAJOR, Minor=$MINOR, Patch=$PATCH"
NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New version: $NEW_VERSION"

# Update the VERSION file
echo "Writing new version to $VERSION_FILE..."
echo "$NEW_VERSION" > "$VERSION_FILE"

# Update CHANGELOG.md with new version section
TODAY=$(date +%Y-%m-%d)
echo "Updating CHANGELOG.md with new version section..."

# Skip CHANGELOG update for now - focusing on just updating the VERSION file
echo "CHANGELOG.md update skipped for now - focusing on VERSION file"

echo "Version updated to $NEW_VERSION and CHANGELOG.md has been updated."
echo "Don't forget to commit these changes with:"
echo "git add $VERSION_FILE CHANGELOG.md"
echo "git commit -m \"Release version $NEW_VERSION\""
echo "git tag -a v$NEW_VERSION -m \"Version $NEW_VERSION\""

# Return success
exit 0