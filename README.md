# My Movies Database

A comprehensive and feature-rich command-line application for managing a personal movie database.

## Description

This application provides a robust and user-friendly interface to create, manage, and explore a collection of movies. It leverages a JSON file for data persistence and can integrate with the OMDb API to automatically fetch movie details, making data entry quick and accurate.

## Features

-   **Data Persistence**: All movie data is saved to `movies.json`, and configuration settings (like the API key) are stored in `config.json`.
-   **Interactive CLI**: A colorful, menu-driven interface that is easy to navigate.
-   **OMDb API Integration**:
    -   Automatically fetch detailed movie information (year, rating, plot, actors) by searching for a title online.
    -   This feature is optional and can be enabled by setting an OMDb API key in the Settings menu.
-   **Advanced Search & Filtering**:
    -   A powerful search function that supports "bang" commands to target specific fields (e.g., `a:Tom Hanks`, `y:2022`).
    -   Flexible filtering to find movies within a specific rating and/or year range.
-   **Comprehensive Movie Management**: Add, update, and delete movies with ease.
-   **Rich Display Options**:
    -   Pagination for easy browsing of large movie lists.
    -   Clean, card-like format for displaying movie details.
    -   Sorting by rating or release year.
-   **Statistics & Fun**:
    -   View aggregate statistics like average/median ratings.
    -   Get a random movie recommendation from your database.
-   **Robustness**: Gracefully handles user interrupts (Ctrl+C) and missing optional dependencies.

## Setup and Installation

1.  **Prerequisites**: Ensure you have Python 3 installed on your system.
2.  **Clone the repository** (or download the files to a local directory).
3.  **Install dependencies**: Open a terminal in the project directory and run the following command to install the required `requests` library:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the application, run the following command in your terminal from the project's root directory:

```bash
python movies.py
```

You will be greeted with the main menu, from which you can navigate to all the application's features.

## Configuration

### OMDb API Key

To use the online search functionality ("Add movie from OMDb"), you need a free API key from the **OMDb API**.

1.  Get your free key here: [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
2.  Run the application.
3.  Navigate to `4. Settings` -> `1. Set OMDb API Key`.
4.  Enter your API key when prompted.

The key will be saved in `config.json` and used for all future online searches.
