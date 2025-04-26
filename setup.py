#!/usr/bin/env python3

"""Setup script for pigame package."""

from pathlib import Path

from setuptools import setup


# Read the version from the VERSION file
def read_version() -> str:
    """Read the version number from the VERSION file located in the 'src' directory.

    The function attempts to open and read the version from the specified file using
    UTF-8 encoding. If the file is successfully read, it returns the trimmed content
    as the version string. If an OSError or IOError occurs (e.g., if the file is not
    found), it returns the default version "1.7.0".

    Returns:
        str: The version string obtained from the file or the default version "1.7.0".
    """
    version_file = Path(__file__).parent / "src" / "VERSION"
    try:
        with version_file.open(encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "1.7.0"  # Default version


setup(
    name="pigame",
    version=read_version(),
    description="Test your memory of π using verified digits",
    long_description=(
        "A multi-implementation tool to help memorize π digits, using verified "
        "digits from trusted mathematical sources for perfect accuracy."
    ),
    author="Thomas J. Dyhr",
    author_email="thomas@dyhr.com",
    url="https://github.com/docdyhr/pigame",
    py_modules=["pigame"],
    package_dir={"": "src/python"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pigame-py=python.pigame:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.11",
)
