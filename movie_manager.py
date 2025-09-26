"""This module provides functionality for managing a movie database."""

import random
import statistics
import movie_storage

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class MovieManager:
    """Handles all business logic for managing movies."""

    def __init__(self):
        """Initialize the MovieManager with movies from storage."""
        self.movies = movie_storage.get_movies()

    def get_all_movies(self):
        """Retrieve all movies from the database.

        Returns:
            dict: A dictionary containing all movies.
        """
        return self.movies

    def add_movie_manually(self, title, rating, year):
        """Add a movie to the database manually.

        Args:
            title (str): The title of the movie.
            rating (float): The movie's rating.
            year (int): The release year of the movie.

        Returns:
            tuple: (success: bool, message: str)
        """
        if title in self.movies:
            return False, f"Movie '{title}' already exists!"

        self.movies[title] = {"rating": rating, "year": year}
        movie_storage.save_movies(self.movies)
        return True, f"Movie '{title}' added successfully."

    def add_movie_from_omdb(self, title, movie_data):
        """Add a movie using data fetched from OMDb.

        Args:
            title (str): The title of the movie.
            movie_data (dict): The movie data from OMDb API.

        Returns:
            tuple: (success: bool, message: str)
        """
        if title in self.movies:
            return False, f"Movie '{title}' already exists!"

        try:
            year_str = movie_data.get("Year")
            rating_str = movie_data.get("imdbRating")
            description = movie_data.get("Plot")
            actors_str = movie_data.get("Actors", "")

            year = int(year_str) if year_str and year_str.isdigit() else 0
            rating = (
                float(rating_str)
                if rating_str and rating_str != "N/A"
                else 0.0
            )
            actors = [actor.strip() for actor in actors_str.split(",")]

            self.movies[title] = {
                "rating": rating,
                "year": year,
                "description": description,
                "actors": actors,
            }
            movie_storage.save_movies(self.movies)
            return True, f"Movie '{title}' added successfully."
        except (ValueError, TypeError) as e:
            return False, f"Could not parse movie data from OMDb: {e}"

    def delete_movie(self, title):
        """Delete a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            tuple: (success: bool, message: str)
        """
        if title not in self.movies:
            return False, f"Movie '{title}' not found!"

        del self.movies[title]
        movie_storage.save_movies(self.movies)
        return True, f"Movie '{title}' deleted."

    def update_movie_title(self, old_title, new_title):
        """Update the movie title if the new title is not already in use."""
        if new_title in self.movies:
            return False, "Invalid or duplicate title."
        self.movies[new_title] = self.movies.pop(old_title)
        movie_storage.save_movies(self.movies)
        return True, f"Movie title updated to '{new_title}'."

    def update_movie_field(self, title, field, value):
        """Update a specific field of a movie."""
        self.movies[title][field] = value
        movie_storage.save_movies(self.movies)
        return True, f"{field.capitalize()} updated successfully."

    def get_stats(self):
        """Calculate and return statistics about the movies.

        Returns:
            dict: A dictionary containing various statistics about the movies.
        """
        if not self.movies:
            return None

        ratings = [data["rating"] for data in self.movies.values()]
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        max_rating = max(ratings)
        min_rating = min(ratings)

        best_titles = sorted(
            [
                title
                for title, data in self.movies.items()
                if data["rating"] == max_rating
            ]
        )
        worst_titles = sorted(
            [
                title
                for title, data in self.movies.items()
                if data["rating"] == min_rating
            ]
        )

        return {
            "total_movies": len(self.movies),
            "avg_rating": avg_rating,
            "median_rating": median_rating,
            "best_movies": (best_titles, max_rating),
            "worst_movies": (worst_titles, min_rating),
        }

    def get_random_movie(self):
        """Return a random movie from the database.

        Returns:
            tuple: A tuple containing (title, movie_data) or (None, None) if no movies exist.
        """
        if not self.movies:
            return None, None
        return random.choice(list(self.movies.items()))

    def search_movies(self, query):
        """Search for movies based on a query string.

        Args:
            query (str): The search query.

        Returns:
            list: A list of tuples containing (title, movie_data) that match the query.
        """
        found_movies = []
        query_lower = query.lower()

        if query_lower.startswith("a:"):
            search_term = query_lower[2:].strip()
            for title, data in self.movies.items():
                if "actors" in data and any(
                    search_term in actor.lower() for actor in data["actors"]
                ):
                    found_movies.append((title, data))
        elif query_lower.startswith("y:"):
            try:
                search_year = int(query_lower[2:].strip())
                for title, data in self.movies.items():
                    if data["year"] == search_year:
                        found_movies.append((title, data))
            except ValueError:
                return None  # Indicates a bad query
        elif query_lower.startswith("r:"):
            try:
                search_rating = float(query_lower[2:].strip())
                for title, data in self.movies.items():
                    if data["rating"] == search_rating:
                        found_movies.append((title, data))
            except ValueError:
                return None  # Indicates a bad query
        else:
            for title, data in self.movies.items():
                if query_lower in title.lower():
                    found_movies.append((title, data))

        return found_movies

    def filter_movies(self, min_rating, start_year, end_year):
        """Filter movies by rating and/or year range.

        Args:
            min_rating (float, optional): Minimum rating threshold.
            start_year (int, optional): Earliest release year.
            end_year (int, optional): Latest release year.

        Returns:
            dict: Filtered dictionary of movies.
        """
        filtered = {}
        for title, data in self.movies.items():
            if (
                (min_rating is None or data["rating"] >= min_rating)
                and (start_year is None or data["year"] >= start_year)
                and (end_year is None or data["year"] <= end_year)
            ):
                filtered[title] = data
        return filtered

    def sort_movies(self, by, order_desc=True):
        """Sort movies by a given field.

        Args:
            by (str): The field to sort by ('rating' or 'year').
            order_desc (bool): Whether to sort in descending order.

        Returns:
            list: A sorted list of (title, movie_data) tuples.
        """
        return sorted(
            self.movies.items(), key=lambda x: x[1][by], reverse=order_desc
        )

    def search_movie_online(self, query):
        """Search for a movie online using the OMDb API.

        Args:
            query (str): The movie title to search for

        Returns:
            tuple: A tuple containing movie data and an error message.
                   If successful, returns (dict, None). On error, returns
                   (None, str).
        """
        if not REQUESTS_AVAILABLE:
            return None, "The 'requests' library is not installed."

        api_key = movie_storage.get_api_key()
        if not api_key:
            return None, "OMDb API key is not set."

        url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
        try:
            response = requests.get(url)
            # Raise an exception for bad status codes
            response.raise_for_status()
            data = response.json()
            if data.get("Response") == "True":
                return data, None
            return None, data.get("Error", "Movie not found.")
        except requests.exceptions.RequestException as e:
            return None, f"An error occurred while searching online: {e}"
