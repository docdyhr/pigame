#!/usr/bin/env bash

# Script to manage version updates in the project
# Usage: ./version.sh [major|minor|patch]

# Enable error handling
set -e

# Define files
VERSION_FILE="src/VERSION"
README="README.md"
CHANGELOG="CHANGELOG.md"

# Colors for output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${YELLOW}Reading version from $VERSION_FILE${RESET}"
if [ ! -f "$VERSION_FILE" ]; then
    echo -e "${RED}Version file not found! Creating with default version 1.0.0${RESET}"
    mkdir -p "$(dirname "$VERSION_FILE")"
    echo "1.0.0" >"$VERSION_FILE"
fi

CURRENT_VERSION=$(cat $VERSION_FILE)
echo -e "${GREEN}Current version: $CURRENT_VERSION${RESET}"

# Validate current version follows semantic versioning
if ! [[ $CURRENT_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Current version '$CURRENT_VERSION' does not follow semantic versioning (X.Y.Z)${RESET}"
    exit 1
fi

# Split the version string into components
IFS='.' read -r -a VERSION_PARTS <<<"$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

echo -e "${YELLOW}Parsed version: Major=$MAJOR, Minor=$MINOR, Patch=$PATCH${RESET}"

# Validate numeric parts
if ! [[ "$MAJOR" =~ ^[0-9]+$ ]] || ! [[ "$MINOR" =~ ^[0-9]+$ ]] || ! [[ "$PATCH" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}Error: Version components must be numeric integers${RESET}"
    exit 1
fi

# Update version based on argument
case "$1" in
major)
    echo -e "${GREEN}Updating major version...${RESET}"
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
minor)
    echo -e "${GREEN}Updating minor version...${RESET}"
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
patch)
    echo -e "${GREEN}Updating patch version...${RESET}"
    PATCH=$((PATCH + 1))
    ;;
*)
    echo -e "${YELLOW}Usage: $0 [major|minor|patch]${RESET}"
    exit 1
    ;;
esac

echo -e "${GREEN}Incremented to: Major=$MAJOR, Minor=$MINOR, Patch=$PATCH${RESET}"
NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo -e "${GREEN}New version: $NEW_VERSION${RESET}"

# Validate the new version
if [[ "$NEW_VERSION" == "$CURRENT_VERSION" ]]; then
    echo -e "${RED}Error: New version is identical to current version${RESET}"
    exit 1
fi

# Update the VERSION file
echo -e "${YELLOW}Writing new version to $VERSION_FILE...${RESET}"
echo "$NEW_VERSION" >"$VERSION_FILE"
echo -e "${GREEN}Version file updated successfully${RESET}"

# Update CHANGELOG.md with new version section
TODAY=$(date +%Y-%m-%d)
echo -e "${YELLOW}Updating CHANGELOG.md with new version section...${RESET}"

# Check if CHANGELOG.md exists
if [ ! -f "$CHANGELOG" ]; then
    echo -e "${RED}Error: CHANGELOG.md not found!${RESET}"
    exit 1
fi

# For macOS/Linux compatibility
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${YELLOW}Running on macOS, using compatible sed syntax${RESET}"
    # macOS requires an extension with -i
    sed -i "" "s/## \[Unreleased\]/## [Unreleased]\n\n### Added\n- TBD\n\n## [$NEW_VERSION] - $TODAY/" CHANGELOG.md
    sed -i "" "s/\[Unreleased\]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v[0-9][0-9.]*\.\.\.HEAD/[Unreleased]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$NEW_VERSION...HEAD\n[$NEW_VERSION]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$CURRENT_VERSION...v$NEW_VERSION/" CHANGELOG.md
else
    # Linux version
    sed -i "s/## \[Unreleased\]/## [Unreleased]\n\n### Added\n- TBD\n\n## [$NEW_VERSION] - $TODAY/" CHANGELOG.md
    sed -i "s/\[Unreleased\]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v[0-9][0-9.]*\.\.\.HEAD/[Unreleased]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$NEW_VERSION...HEAD\n[$NEW_VERSION]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$CURRENT_VERSION...v$NEW_VERSION/" CHANGELOG.md
fi

echo -e "${GREEN}Version updated to $NEW_VERSION and CHANGELOG.md has been updated.${RESET}"
echo -e "${YELLOW}Don't forget to commit these changes with:${RESET}"
echo -e "git add $VERSION_FILE CHANGELOG.md"
echo -e "git commit -m \"Release version $NEW_VERSION\""
echo -e "git tag -a v$NEW_VERSION -m \"Version $NEW_VERSION\""

# Update README.md with new version
echo -e "${YELLOW}Updating README.md with new version...${RESET}"

# Check if README.md exists
if [ ! -f "$README" ]; then
    echo -e "${RED}Error: README.md not found!${RESET}"
    exit 1
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS sed
    sed -i "" -E "s|(\[!\[Version\]\(https://img.shields.io/badge/version-)[0-9]+\.[0-9]+\.[0-9]+(-blue\)\]\(https://github.com/docdyhr/pigame/blob/master/src/VERSION\))|\1$NEW_VERSION\2|" "$README"
    sed -i "" -E "s|(\* Version: )[0-9]+\.[0-9]+\.[0-9]+|\1$NEW_VERSION|" "$README"
else
    # Linux sed
    sed -i -E "s|(\[!\[Version\]\(https://img.shields.io/badge/version-)[0-9]+\.[0-9]+\.[0-9]+(-blue\)\]\(https://github.com/docdyhr/pigame/blob/master/src/VERSION\))|\1$NEW_VERSION\2|" "$README"
    sed -i -E "s|(\* Version: )[0-9]+\.[0-9]+\.[0-9]+|\1$NEW_VERSION|" "$README"
fi

echo -e "${GREEN}README.md version badge and references updated to $NEW_VERSION.${RESET}"

# Create a summary of changes
echo -e "\n${GREEN}============== Version Update Summary ==============${RESET}"
echo -e "Previous version: ${YELLOW}$CURRENT_VERSION${RESET}"
echo -e "New version:      ${GREEN}$NEW_VERSION${RESET}"
echo -e "Updated files:"
echo -e "  - ${YELLOW}$VERSION_FILE${RESET}"
echo -e "  - ${YELLOW}$README${RESET}"
echo -e "  - ${YELLOW}$CHANGELOG${RESET}"
echo -e "${GREEN}=================================================${RESET}\n"

# Return success
exit 0
