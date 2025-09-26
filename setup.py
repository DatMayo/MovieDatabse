"""Setup script for the Movie Database package."""

import re
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moviedatabase",
    version=re.search(r'^__version__\s*=\s*"(.*)"', open('__init__.py').read(), re.M).group(1),
    author="DatMayo",
    author_email="author@example.com",
    description="A movie database management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DatMayo/MovieDatabse",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "moviedb=movies:main",
        ],
    },
)
