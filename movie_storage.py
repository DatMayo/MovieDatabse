"""This module provides functionality for storing and retrieving movie data."""

import json
import os

# Construct an absolute path to the movies.json file
# This ensures the file is found regardless of the script's working directory
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(_CURRENT_DIR, "movies.json")
CONFIG_FILE = os.path.join(_CURRENT_DIR, "config.json")


def get_api_key():
    """Retrieve the OMDb API key from the config file.

    Returns:
        str: The API key if found, None otherwise.
    """
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("api_key")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_api_key(api_key):
    """Save the OMDb API key to the config file.

    Args:
        api_key (str): The API key to save.
    """
    with open(CONFIG_FILE, "w") as file:
        json.dump({"api_key": api_key}, file, indent=4)


def get_movies():
    """Retrieve all movies from the database.

    Returns:
        dict: A dictionary containing movie data, or an empty dict if no data exists.
    """
    try:
        with open(MOVIES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_movies(movies):
    """Save movies data to the JSON file.

    Args:
        movies (dict): Dictionary containing movie data to be saved.
    """
    with open(MOVIES_FILE, "w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    """Add a movie to the database.

    Args:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The movie's rating.
    """
    movies = get_movies()
    movies[title] = {"rating": rating, "year": year}
    save_movies(movies)


def delete_movie(title):
    """Delete a movie from the database.

    Args:
        title (str): The title of the movie to delete.
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, field, value):
    """Update a specific field of a movie in the database.

    Args:
        title (str): The current title of the movie.
        field (str): The field to update ('title', 'year', 'rating', etc.).
        value (any): The new value for the specified field.
    """
    movies = get_movies()
    if title in movies:
        if field == "title":
            movies[value] = movies.pop(title)
        else:
            movies[title][field] = value
        save_movies(movies)
