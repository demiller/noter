# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

# Read README with UTF-8 encoding
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="noter",
    version="1.1.2",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "noter=noter:main",
        ],
    },
    author="Doug Miller",
    description="A tool for managing Obsidian daily notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demiller/noter",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup",
    ],
)
