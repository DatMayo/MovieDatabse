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
        self.movies = movie_storage.get_movies()

    def get_all_movies(self):
        return self.movies

    def add_movie_manually(self, title, rating, year):
        """Adds a movie to the database manually."""
        if title in self.movies:
            return False, f"Movie '{title}' already exists!"
        
        self.movies[title] = {"rating": rating, "year": year}
        movie_storage.save_movies(self.movies)
        return True, f"Movie '{title}' added successfully."

    def add_movie_from_omdb(self, title, movie_data):
        """Adds a movie using data fetched from OMDb."""
        if title in self.movies:
            return False, f"Movie '{title}' already exists!"

        try:
            year_str = movie_data.get('Year')
            rating_str = movie_data.get('imdbRating')
            description = movie_data.get('Plot')
            actors_str = movie_data.get('Actors', '')

            year = int(year_str) if year_str and year_str.isdigit() else 0
            rating = float(rating_str) if rating_str and rating_str != 'N/A' else 0.0
            actors = [actor.strip() for actor in actors_str.split(',')]

            self.movies[title] = {
                'rating': rating,
                'year': year,
                'description': description,
                'actors': actors
            }
            movie_storage.save_movies(self.movies)
            return True, f"Movie '{title}' added successfully."
        except (ValueError, TypeError) as e:
            return False, f"Could not parse movie data from OMDb: {e}"

    def delete_movie(self, title):
        """Deletes a movie from the database."""
        if title not in self.movies:
            return False, f"Movie '{title}' not found!"
        
        del self.movies[title]
        movie_storage.save_movies(self.movies)
        return True, f"Movie '{title}' deleted."

    def update_movie_title(self, old_title, new_title):
        if new_title in self.movies:
            return False, "Invalid or duplicate title."
        self.movies[new_title] = self.movies.pop(old_title)
        movie_storage.save_movies(self.movies)
        return True, f"Movie title updated to '{new_title}'."

    def update_movie_field(self, title, field, value):
        self.movies[title][field] = value
        movie_storage.save_movies(self.movies)
        return True, f"{field.capitalize()} updated successfully."

    def get_stats(self):
        """Calculates and returns statistics about the movies."""
        if not self.movies:
            return None

        ratings = [data['rating'] for data in self.movies.values()]
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        
        max_rating = max(ratings)
        min_rating = min(ratings)

        best_titles = sorted([title for title, data in self.movies.items() if data['rating'] == max_rating])
        worst_titles = sorted([title for title, data in self.movies.items() if data['rating'] == min_rating])

        return {
            "total_movies": len(self.movies),
            "avg_rating": avg_rating,
            "median_rating": median_rating,
            "best_movies": (best_titles, max_rating),
            "worst_movies": (worst_titles, min_rating)
        }

    def get_random_movie(self):
        """Returns a random movie from the database."""
        if not self.movies:
            return None, None
        return random.choice(list(self.movies.items()))

    def search_movies(self, query):
        """Searches for movies based on a query string."""
        found_movies = []
        query_lower = query.lower()

        if query_lower.startswith('a:'):
            search_term = query_lower[2:].strip()
            for title, data in self.movies.items():
                if 'actors' in data and any(search_term in actor.lower() for actor in data['actors']):
                    found_movies.append((title, data))
        elif query_lower.startswith('y:'):
            try:
                search_year = int(query_lower[2:].strip())
                for title, data in self.movies.items():
                    if data['year'] == search_year:
                        found_movies.append((title, data))
            except ValueError:
                return None # Indicates a bad query
        elif query_lower.startswith('r:'):
            try:
                search_rating = float(query_lower[2:].strip())
                for title, data in self.movies.items():
                    if data['rating'] == search_rating:
                        found_movies.append((title, data))
            except ValueError:
                return None # Indicates a bad query
        else:
            for title, data in self.movies.items():
                if query_lower in title.lower():
                    found_movies.append((title, data))
        
        return found_movies

    def filter_movies(self, min_rating, start_year, end_year):
        """Filters movies by rating and/or year range."""
        filtered = {}
        for title, data in self.movies.items():
            if (min_rating is None or data['rating'] >= min_rating) and \
               (start_year is None or data['year'] >= start_year) and \
               (end_year is None or data['year'] <= end_year):
                filtered[title] = data
        return filtered

    def sort_movies(self, by, order_desc=True):
        """Sorts movies by a given field ('rating' or 'year')."""
        return sorted(self.movies.items(), key=lambda x: x[1][by], reverse=order_desc)

    def search_movie_online(self, query):
        """Searches for a movie online using the OMDb API."""
        if not REQUESTS_AVAILABLE:
            return None, "The 'requests' library is not installed."

        api_key = movie_storage.get_api_key()
        if not api_key:
            return None, "OMDb API key is not set."

        url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if data.get('Response') == 'True':
                return data, None
            else:
                return None, data.get('Error', 'Movie not found.')
        except requests.exceptions.RequestException as e:
            return None, f"An error occurred while searching online: {e}"
