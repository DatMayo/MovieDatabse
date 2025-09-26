# 🎬 Movie Database

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive and feature-rich command-line application for managing a personal movie database with OMDb API integration.

## ✨ Features

- **Interactive CLI** with colorful, menu-driven interface
- **OMDb API Integration** for automatic movie data fetching
- **Advanced Search** with field-specific queries (e.g., `a:Tom Hanks`, `y:2022`)
- **Filtering** by rating and release year
- **Statistics** including average/median ratings
- **Random Movie** picker
- **Data Persistence** using JSON storage
- **Pagination** for easy browsing
- **Sorting** by rating or release year

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install moviedatabase
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/DatMayo/MovieDatabse.git
   cd MovieDatabse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

### Basic Usage

```bash
# Run the application
python -m moviedatabase

# Or if installed via pip
moviedb
```

### Command Line Options

```bash
python -m moviedatabase --help
```

## 🔧 Configuration

### OMDb API Key

To use the online search functionality ("Add movie from OMDb"), you need a free API key from the **OMDb API**.

1.  Get your free key here: [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
2.  Run the application.
3.  Navigate to `4. Settings` -> `1. Set OMDb API Key`.
4.  Enter your API key when prompted.

The key will be saved in `config.json` and used for all future online searches.
