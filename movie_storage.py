import json
import os

# Construct an absolute path to the movies.json file
# This ensures the file is found regardless of the script's working directory
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(_CURRENT_DIR, "movies.json")
CONFIG_FILE = os.path.join(_CURRENT_DIR, "config.json")

def get_api_key():
    """Returns the OMDb API key from the config file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get('api_key')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_api_key(api_key):
    """Saves the OMDb API key to the config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump({'api_key': api_key}, file, indent=4)

def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.
    """
    try:
        with open(MOVIES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(MOVIES_FILE, "w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {"rating": rating, "year": year}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, field, value):
    """
    Updates a specific field of a movie in the database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        if field == 'title':
            movies[value] = movies.pop(title)
        else:
            movies[title][field] = value
        save_movies(movies)