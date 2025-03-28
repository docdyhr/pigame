#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the version from the VERSION file
def read_version():
    version_file = os.path.join(
        os.path.dirname(__file__), 'src', 'VERSION'
    )
    try:
        with open(version_file, 'r') as f:
            return f.read().strip()
    except:
        return '1.6.0'  # Default version

setup(
    name="pigame",
    version=read_version(),
    description="How many decimals of π can you remember?",
    author="Thomas J. Dyhr",
    author_email="thomas@dyhr.com",
    url="https://github.com/docdyhr/pigame",
    packages=find_packages(),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=["python.pigame"],
    entry_points={
        'console_scripts': [
            'pigame-py=python.pigame:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
    ],
    python_requires=">=3.6",
)