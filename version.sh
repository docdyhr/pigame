#!/usr/bin/env bash

# Script to manage version updates in the project
# Usage: ./version.sh [major|minor|patch]

set -e

VERSION_FILE="src/VERSION"
CURRENT_VERSION=$(cat $VERSION_FILE)

echo "Current version: $CURRENT_VERSION"

# Split the version string into components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Update version based on argument
case "$1" in
    major)
        ((MAJOR++))
        MINOR=0
        PATCH=0
        ;;
    minor)
        ((MINOR++))
        PATCH=0
        ;;
    patch)
        ((PATCH++))
        ;;
    *)
        echo "Usage: $0 [major|minor|patch]"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New version: $NEW_VERSION"

# Update the VERSION file
echo "$NEW_VERSION" > "$VERSION_FILE"

# Update CHANGELOG.md with new version section
TODAY=$(date +%Y-%m-%d)

# For macOS compatibility
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS, using compatible sed syntax"
    # macOS requires an extension with -i
    sed -i "" -e "s/## \[Unreleased\]/## [Unreleased]\n\n### Added\n- TBD\n\n## [$NEW_VERSION] - $TODAY/" CHANGELOG.md
    sed -i "" -e "s/\[Unreleased\]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v[0-9]*\.[0-9]*\.[0-9]*\.\.\.HEAD/[Unreleased]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$NEW_VERSION...HEAD\n[$NEW_VERSION]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$CURRENT_VERSION...v$NEW_VERSION/" CHANGELOG.md
else
    # Linux version
    sed -i -e "s/## \[Unreleased\]/## [Unreleased]\n\n### Added\n- TBD\n\n## [$NEW_VERSION] - $TODAY/" CHANGELOG.md
    sed -i -e "s/\[Unreleased\]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v[0-9]*\.[0-9]*\.[0-9]*\.\.\.HEAD/[Unreleased]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$NEW_VERSION...HEAD\n[$NEW_VERSION]: https:\/\/github.com\/docdyhr\/pigame\/compare\/v$CURRENT_VERSION...v$NEW_VERSION/" CHANGELOG.md
fi

echo "Version updated to $NEW_VERSION and CHANGELOG.md has been updated."
echo "Don't forget to commit these changes with:"
echo "git add $VERSION_FILE CHANGELOG.md"
echo "git commit -m \"Release version $NEW_VERSION\""
echo "git tag -a v$NEW_VERSION -m \"Version $NEW_VERSION\""

# Return success
exit 0