"""Setup script for the Movie Database package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moviedatabase",
    version="0.1.0",  # Update this with each release
    author="DatMayo",
    author_email="your.email@example.com",  # Update with your email
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
