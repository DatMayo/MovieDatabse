#!/usr/bin/env python3
"""
==============================
My Movies Database Application
==============================

A comprehensive and feature-rich command-line application for managing a
personal movie database.

This application provides a robust and user-friendly interface to create,
manage, and explore a collection of movies. It leverages a JSON file for
data persistence and can integrate with the OMDb API to automatically fetch
movie details, making data entry quick and accurate.

Core Features:
--------------
- **Data Persistence**: All movie data is saved to a movies.json file, and
  configuration settings (like the API key) are stored in config.json.
- **Interactive CLI**: A colorful, menu-driven interface that is easy to
  navigate, with screen clearing for a clean user experience.
- **OMDb API Integration**:
    - Automatically fetch detailed movie information (year, rating, plot, actors)
      by searching for a title online.
    - This feature is optional and can be enabled by setting an OMDb API key
      in the Settings menu.
- **Advanced Search & Filtering**:
    - A powerful search function that supports "bang" commands to target
      specific fields:
        - `a:[actor_name]` to search by actor.
        - `y:[year]` to search by release year.
        - `r:[rating]` to search by rating.
    - A flexible filtering option to find movies within a specific rating
      and/or year range.
- **Comprehensive Movie Management**:
    - **Add Movies**: Manually, or automatically from OMDb.
    - **Update Movies**: A dedicated submenu allows editing any field of an
      existing movie, including its title, year, rating, description, and actors.
    - **Delete Movies**: Easily remove movies from the database.
- **Rich Display Options**:
    - **Pagination**: Long lists of movies are displayed in pages (10 per page)
      for easy browsing.
    - **Card-Like Format**: Movie details are presented in a clean, readable
      card format.
    - **Sorting**: Movies can be sorted by rating (highest first) or by
      release year (latest or oldest first).
- **Statistics & Fun**:
    - View aggregate statistics like average/median ratings and best/worst movies.
    - Get a random movie recommendation from your database.
- **Robustness**:
    - Gracefully handles user interrupts (Ctrl+C).
    - Conditionally enables features based on whether the `requests` library
      is installed.
"""

import random
import statistics
import signal
import sys
import textwrap
import os
from typing import Dict

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

import movie_storage


class Colors:
    """ANSI color codes for terminal text formatting."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INPUT = '\033[94m'  # Blue for user input
    MENU = '\033[95m'   # Purple for menu
    ERROR = '\033[91m'  # Red for errors
    SUCCESS = '\033[92m' # Green for success messages


def clear_screen() -> None:
    """Clear the screen using the appropriate command for the OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def signal_handler(sig: int, frame: object) -> None:
    """Handle keyboard interrupt (Ctrl+C) gracefully."""
    print(f"\n\n{Colors.WARNING}Operation cancelled by user.{Colors.ENDC}")
    print(f"{Colors.GREEN}Goodbye!{Colors.ENDC}")
    sys.exit(0)


def display_main_menu() -> None:
    """Display the main menu options."""
    clear_screen()
    print(f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********{Colors.ENDC}")
    print(f"\n{Colors.MENU}Main Menu:{Colors.ENDC}")
    print(f"{Colors.MENU}1.{Colors.ENDC} Display Movies")
    print(f"{Colors.MENU}2.{Colors.ENDC} Edit Movies")
    print(f"{Colors.MENU}3.{Colors.ENDC} Statistics & Fun")
    if REQUESTS_AVAILABLE:
        print(f"{Colors.MENU}4.{Colors.ENDC} Settings")
    print(f"{Colors.MENU}0.{Colors.ENDC} Exit")

def display_movies_menu() -> None:
    """Display the movies submenu options."""
    clear_screen()
    print(f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********{Colors.ENDC}")
    print(f"\n{Colors.MENU}Display Movies Menu:{Colors.ENDC}")
    print(f"{Colors.MENU}1.{Colors.ENDC} List all movies")
    print(f"{Colors.MENU}2.{Colors.ENDC} Search movie")
    print(f"{Colors.MENU}3.{Colors.ENDC} Filter movies")
    print(f"{Colors.MENU}4.{Colors.ENDC} Sort by rating")
    print(f"{Colors.MENU}5.{Colors.ENDC} Sort by year")
    print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

def display_edit_menu() -> None:
    """Display the edit submenu options."""
    clear_screen()
    print(f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********{Colors.ENDC}")
    print(f"\n{Colors.MENU}Edit Movies Menu:{Colors.ENDC}")
    print(f"{Colors.MENU}1.{Colors.ENDC} Add movie manually")
    if REQUESTS_AVAILABLE and movie_storage.get_api_key():
        print(f"{Colors.MENU}2.{Colors.ENDC} Add movie from OMDb")
    print(f"{Colors.MENU}3.{Colors.ENDC} Update movie")
    print(f"{Colors.MENU}4.{Colors.ENDC} Delete movie")
    print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

def display_settings_menu() -> None:
    """Display the settings submenu options."""
    clear_screen()
    print(f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********{Colors.ENDC}")
    print(f"\n{Colors.MENU}Settings Menu:{Colors.ENDC}")
    print(f"{Colors.MENU}1.{Colors.ENDC} Set OMDb API Key")
    print(f"{Colors.MENU}2.{Colors.ENDC} View OMDb API Key")
    print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

def display_stats_menu() -> None:
    """Display the statistics submenu options."""
    clear_screen()
    print(f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********{Colors.ENDC}")
    print(f"\n{Colors.MENU}Statistics & Fun Menu:{Colors.ENDC}")
    print(f"{Colors.MENU}1.{Colors.ENDC} Show stats")
    print(f"{Colors.MENU}2.{Colors.ENDC} Random movie")
    print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")


def handle_display_movies_menu(movies: Dict[str, Dict]) -> None:
    """Handle the display movies submenu."""
    while True:
        display_movies_menu()
        choice = input(f"\n{Colors.INPUT}Enter choice (0-5): {Colors.ENDC}").strip()
        if choice == '0':
            break
        elif choice == '1':
            list_movies(movies)
        elif choice == '2':
            search_movie(movies)
        elif choice == '3':
            filter_movies(movies)
        elif choice == '4':
            sort_by_rating(movies)
        elif choice == '5':
            sort_by_year(movies)
        else:
            print(f"{Colors.ERROR}Invalid choice. Please enter a number between 0 and 5.{Colors.ENDC}")
        input(f"\n{Colors.INPUT}Press Enter to continue...{Colors.ENDC}")

def handle_edit_movies_menu(movies: Dict[str, Dict]) -> None:
    """Handle the edit movies submenu."""
    while True:
        display_edit_menu()
        choice = input(f"\n{Colors.INPUT}Enter choice: {Colors.ENDC}").strip()
        if choice == '0':
            break
        elif choice == '1':
            add_movie_manually(movies)
        elif choice == '2' and REQUESTS_AVAILABLE and movie_storage.get_api_key():
            add_movie_from_omdb(movies)
        elif choice == '3':
            update_movie(movies)
        elif choice == '4':
            delete_movie(movies)
        else:
            print(f"{Colors.ERROR}Invalid choice.{Colors.ENDC}")
        input(f"\n{Colors.INPUT}Press Enter to continue...{Colors.ENDC}")

def handle_settings_menu() -> None:
    """Handle the settings submenu."""
    while True:
        display_settings_menu()
        choice = input(f"\n{Colors.INPUT}Enter choice (0-2): {Colors.ENDC}").strip()
        if choice == '0':
            break
        elif choice == '1':
            api_key = input(f"{Colors.INPUT}Enter your OMDb API key: {Colors.ENDC}").strip()
            movie_storage.save_api_key(api_key)
            print(f"{Colors.SUCCESS}API key saved.{Colors.ENDC}")
        elif choice == '2':
            api_key = movie_storage.get_api_key()
            if api_key:
                print(f"Current API Key: {api_key}")
            else:
                print(f"{Colors.WARNING}No API key set.{Colors.ENDC}")
        else:
            print(f"{Colors.ERROR}Invalid choice. Please enter a number between 0 and 2.{Colors.ENDC}")
        input(f"\n{Colors.INPUT}Press Enter to continue...{Colors.ENDC}")

def handle_stats_menu(movies: Dict[str, Dict]) -> None:
    """Handle the statistics submenu."""
    while True:
        display_stats_menu()
        choice = input(f"\n{Colors.INPUT}Enter choice (0-2): {Colors.ENDC}").strip()
        if choice == '0':
            break
        elif choice == '1':
            show_stats(movies)
        elif choice == '2':
            random_movie(movies)
        else:
            print(f"{Colors.ERROR}Invalid choice. Please enter a number between 0 and 2.{Colors.ENDC}")
        input(f"\n{Colors.INPUT}Press Enter to continue...{Colors.ENDC}")

def _display_movie_card(index: int, title: str, data: Dict) -> None:
    """Display a single movie in a card-like format."""
    print(f"\n{Colors.HEADER}{index}. {title}{Colors.ENDC}")
    print(f"   {Colors.BOLD}Year:{Colors.ENDC} {data.get('year', 'N/A')}")
    print(f"   {Colors.BOLD}Rating:{Colors.ENDC} {data.get('rating', 'N/A'):.1f}")
    if 'description' in data:
        wrapped_description = textwrap.wrap(data['description'], width=80)
        print(f"   {Colors.BOLD}Description:{Colors.ENDC}")
        for line in wrapped_description:
            print(f"     {line}")
    if 'actors' in data:
        print(f"   {Colors.BOLD}Actors:{Colors.ENDC} {', '.join(data['actors'])}")

def list_movies(movies: Dict[str, Dict]) -> None:
    """Display all movies in the database with pagination."""
    if not movies:
        print(f"{Colors.WARNING}No movies in the database.{Colors.ENDC}")
        return

    movie_list = list(movies.items())
    total_movies = len(movie_list)
    page_size = 10
    num_pages = (total_movies + page_size - 1) // page_size
    current_page = 0

    while True:
        clear_screen()
        print(f"\n{Colors.CYAN}List of all movies (Page {current_page + 1}/{num_pages}):{Colors.ENDC}")
        start_index = current_page * page_size
        end_index = start_index + page_size
        for i, (title, data) in enumerate(movie_list[start_index:end_index], start=start_index + 1):
            _display_movie_card(i, title, data)

        print("\n'n' for next page, 'p' for previous, 'q' to quit")
        choice = input(f"{Colors.INPUT}Enter choice: {Colors.ENDC}").strip().lower()

        if choice == 'n':
            if current_page < num_pages - 1:
                current_page += 1
            else:
                print(f"{Colors.WARNING}You are on the last page.{Colors.ENDC}")
                input("Press Enter to continue...")
        elif choice == 'p':
            if current_page > 0:
                current_page -= 1
            else:
                print(f"{Colors.WARNING}You are on the first page.{Colors.ENDC}")
                input("Press Enter to continue...")
        elif choice == 'q':
            break
        else:
            print(f"{Colors.ERROR}Invalid choice.{Colors.ENDC}")
            input("Press Enter to continue...")


def get_year_input(prompt: str) -> int:
    """Get and validate a movie release year from user input."""
    while True:
        try:
            year = int(input(f"{Colors.INPUT}{prompt}{Colors.ENDC}"))
            if year > 0:
                return year
            print(f"{Colors.WARNING}Year must be a positive number.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.ERROR}Please enter a valid year.{Colors.ENDC}")
        except KeyboardInterrupt:
            print()  # Move to new line after Ctrl+C
            raise


def get_rating_input(prompt: str) -> float:
    """Get and validate a movie rating from user input."""
    while True:
        try:
            rating = float(input(f"{Colors.INPUT}{prompt}{Colors.ENDC}"))
            if 0 <= rating <= 10:
                return rating
            print(f"{Colors.WARNING}Rating must be between 0 and 10.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.ERROR}Please enter a valid number.{Colors.ENDC}")
        except KeyboardInterrupt:
            print()  # Move to new line after Ctrl+C
            raise


def search_movie_online(query: str) -> Dict:
    """Search for a movie online using the OMDb API."""
    api_key = movie_storage.get_api_key()
    if not api_key:
        return {}

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Colors.ERROR}An error occurred while searching online: {e}{Colors.ENDC}")
        return {}

def add_movie_from_omdb(movies: Dict[str, Dict]) -> None:
    """Search for a movie online and add it to the database."""
    query = input(f"{Colors.INPUT}Enter movie title to search online: {Colors.ENDC}").strip()
    if not query:
        print(f"{Colors.ERROR}Please enter a search term.{Colors.ENDC}")
        return

    movie_data = search_movie_online(query)
    if movie_data.get('Response') == 'True':
        title = movie_data.get('Title')
        year_str = movie_data.get('Year')
        rating_str = movie_data.get('imdbRating')
        description = movie_data.get('Plot')
        actors_str = movie_data.get('Actors', '')

        if title in movies:
            print(f"{Colors.ERROR}Movie '{title}' already exists!{Colors.ENDC}")
            return

        try:
            year = int(year_str) if year_str and year_str.isdigit() else 0
            rating = float(rating_str) if rating_str and rating_str != 'N/A' else 0.0
            actors = [actor.strip() for actor in actors_str.split(',')]

            movies[title] = {
                'rating': rating,
                'year': year,
                'description': description,
                'actors': actors
            }
            movie_storage.save_movies(movies)
            print(f"{Colors.SUCCESS}Movie '{title}' added successfully.{Colors.ENDC}")
        except (ValueError, TypeError) as e:
            print(f"{Colors.ERROR}Could not parse movie data from OMDb: {e}{Colors.ENDC}")
    else:
        print(f"{Colors.ERROR}Movie not found online.{Colors.ENDC}")

def add_movie_manually(movies: Dict[str, Dict]) -> None:
    """Add a new movie to the database manually."""
    try:
        title = input(f"{Colors.INPUT}Enter movie title: {Colors.ENDC}").strip()
        if not title:
            print(f"{Colors.ERROR}Movie title cannot be empty.{Colors.ENDC}")
            return

        if title in movies:
            print(f"{Colors.ERROR}Movie '{title}' already exists!{Colors.ENDC}")
            return

        rating = get_rating_input("Enter movie rating (0-10): ")
        year = get_year_input("Enter movie year: ")
        # For manual add, we don't have description or actors
        movies[title] = {"rating": rating, "year": year}
        movie_storage.save_movies(movies) # Save the entire movies dict
        print(f"{Colors.SUCCESS}Movie '{title}' added with rating {rating:.1f} and year {year}.{Colors.ENDC}")

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Movie addition cancelled.{Colors.ENDC}")


def delete_movie(movies: Dict[str, Dict]) -> None:
    """Delete a movie from the database."""
    try:
        title = input(f"{Colors.INPUT}Enter movie title to delete: {Colors.ENDC}").strip()
        if title in movies:
            movie_storage.delete_movie(title)
            del movies[title]
            print(f"{Colors.SUCCESS}Movie '{title}' deleted.{Colors.ENDC}")
        else:
            print(f"{Colors.ERROR}Movie '{title}' not found!{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Movie deletion cancelled.{Colors.ENDC}")


def update_movie(movies: Dict[str, Dict]) -> None:
    """Update a movie's details in the database."""
    try:
        title = input(f"{Colors.INPUT}Enter movie title to update: {Colors.ENDC}").strip()
        if title not in movies:
            print(f"{Colors.ERROR}Movie '{title}' not found!{Colors.ENDC}")
            return

        while True:
            print(f"\n{Colors.MENU}What would you like to update?{Colors.ENDC}")
            print(f"{Colors.MENU}1.{Colors.ENDC} Title")
            print(f"{Colors.MENU}2.{Colors.ENDC} Year")
            print(f"{Colors.MENU}3.{Colors.ENDC} Rating")
            print(f"{Colors.MENU}4.{Colors.ENDC} Description")
            print(f"{Colors.MENU}5.{Colors.ENDC} Actors")
            print(f"{Colors.MENU}0.{Colors.ENDC} Back")

            choice = input(f"\n{Colors.INPUT}Enter choice: {Colors.ENDC}").strip()

            if choice == '0':
                break
            elif choice == '1':
                new_title = input(f"{Colors.INPUT}Enter new title: {Colors.ENDC}").strip()
                if new_title and new_title not in movies:
                    movie_storage.update_movie(title, 'title', new_title)
                    movies[new_title] = movies.pop(title)
                    print(f"{Colors.SUCCESS}Movie title updated to '{new_title}'.{Colors.ENDC}")
                    title = new_title  # Update title for further edits
                else:
                    print(f"{Colors.ERROR}Invalid or duplicate title.{Colors.ENDC}")
            elif choice == '2':
                new_year = get_year_input(f"Enter new year (current: {movies[title]['year']}): ")
                movie_storage.update_movie(title, 'year', new_year)
                movies[title]['year'] = new_year
                print(f"{Colors.SUCCESS}Year updated to {new_year}.{Colors.ENDC}")
            elif choice == '3':
                new_rating = get_rating_input(f"Enter new rating (current: {movies[title]['rating']:.1f}): ")
                movie_storage.update_movie(title, 'rating', new_rating)
                movies[title]['rating'] = new_rating
                print(f"{Colors.SUCCESS}Rating updated to {new_rating:.1f}.{Colors.ENDC}")
            elif choice == '4':
                new_description = input(f"{Colors.INPUT}Enter new description: {Colors.ENDC}").strip()
                movie_storage.update_movie(title, 'description', new_description)
                movies[title]['description'] = new_description
                print(f"{Colors.SUCCESS}Description updated.{Colors.ENDC}")
            elif choice == '5':
                new_actors = input(f"{Colors.INPUT}Enter new actors (comma-separated): {Colors.ENDC}").strip()
                actors_list = [actor.strip() for actor in new_actors.split(',')]
                movie_storage.update_movie(title, 'actors', actors_list)
                movies[title]['actors'] = actors_list
                print(f"{Colors.SUCCESS}Actors updated.{Colors.ENDC}")
            else:
                print(f"{Colors.ERROR}Invalid choice.{Colors.ENDC}")

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Movie update cancelled.{Colors.ENDC}")


def show_stats(movies: Dict[str, Dict]) -> None:
    """Display statistics about the movies in the database."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    # Round ratings to 2 decimals to avoid floating point edge cases when comparing
    rounded = {title: round(data['rating'], 2) for title, data in movies.items()}
    ratings = list(rounded.values())
    avg_rating = sum(ratings) / len(ratings)
    min_rating = min(ratings)
    max_rating = max(ratings)
    median_rating = statistics.median(ratings)

    # Compute all movies that share the best and worst ratings
    best_titles = sorted([title for title, rating in rounded.items() if rating == max_rating])
    worst_titles = sorted([title for title, rating in rounded.items() if rating == min_rating])

    print(f"\n{Colors.CYAN}Movie Statistics:{Colors.ENDC}")
    print(f"Total movies: {len(movies)}")
    print(f"Average rating: {avg_rating:.1f}")
    print(f"Median rating: {median_rating:.1f}")
    print(f"Best movie(s): {', '.join(best_titles)} ({max_rating:.1f})")
    print(f"Worst movie(s): {', '.join(worst_titles)} ({min_rating:.1f})")


def random_movie(movies: Dict[str, Dict]) -> None:
    """Display a random movie from the database."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    title, data = random.choice(list(movies.items()))
    print(f"\n{Colors.GREEN}Your random movie is:{Colors.ENDC}")
    _display_movie_card(1, title, data)


def search_movie(movies: Dict[str, Dict]) -> None:
    """Search for movies by title, actor, rating, or year."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    try:
        print("Search by title, or use 'a:' for actor, 'y:' for year, 'r:' for rating.")
        print("(e.g. 'a:Tom Hanks' or 'y:2000')")
        print()
        query = input(f"{Colors.INPUT}Enter search term: {Colors.ENDC}").strip()
        if not query:
            print(f"{Colors.ERROR}Please enter a search term.{Colors.ENDC}")
            return

        found_movies = []
        query_lower = query.lower()

        if query_lower.startswith('a:'):
            search_term = query_lower[2:].strip()
            for title, data in movies.items():
                if 'actors' in data and any(search_term in actor.lower() for actor in data['actors']):
                    found_movies.append((title, data))
        elif query_lower.startswith('y:'):
            try:
                search_year = int(query_lower[2:].strip())
                for title, data in movies.items():
                    if data['year'] == search_year:
                        found_movies.append((title, data))
            except ValueError:
                print(f"{Colors.ERROR}Invalid year format.{Colors.ENDC}")
                return
        elif query_lower.startswith('r:'):
            try:
                search_rating = float(query_lower[2:].strip())
                for title, data in movies.items():
                    if data['rating'] == search_rating:
                        found_movies.append((title, data))
            except ValueError:
                print(f"{Colors.ERROR}Invalid rating format.{Colors.ENDC}")
                return
        else:
            for title, data in movies.items():
                if query_lower in title.lower() or \
                   ('actors' in data and any(query_lower in actor.lower() for actor in data['actors'])):
                    found_movies.append((title, data))

        if not found_movies:
            print(f"{Colors.WARNING}No movies found matching your search.{Colors.ENDC}")
            return

        print(f"\n{Colors.CYAN}Search results for '{query}':{Colors.ENDC}")
        for i, (title, data) in enumerate(found_movies, 1):
            _display_movie_card(i, title, data)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Search cancelled.{Colors.ENDC}")


def filter_movies(movies: Dict[str, Dict]) -> None:
    """Filter movies by rating and year."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    min_rating_str = input(f"{Colors.INPUT}Enter minimum rating (0-10, leave blank for none): {Colors.ENDC}").strip()
    start_year_str = input(f"{Colors.INPUT}Enter start year (leave blank for none): {Colors.ENDC}").strip()
    end_year_str = input(f"{Colors.INPUT}Enter end year (leave blank for none): {Colors.ENDC}").strip()

    min_rating = float(min_rating_str) if min_rating_str else None
    start_year = int(start_year_str) if start_year_str else None
    end_year = int(end_year_str) if end_year_str else None

    filtered_movies = {}
    for title, data in movies.items():
        if (min_rating is None or data['rating'] >= min_rating) and \
           (start_year is None or data['year'] >= start_year) and \
           (end_year is None or data['year'] <= end_year):
            filtered_movies[title] = data

    if not filtered_movies:
        print(f"{Colors.WARNING}No movies found matching your criteria.{Colors.ENDC}")
        return

    print(f"\n{Colors.CYAN}Filtered movies:{Colors.ENDC}")
    for i, (title, data) in enumerate(filtered_movies.items(), 1):
        _display_movie_card(i, title, data)


def sort_by_year(movies: Dict[str, Dict]) -> None:
    """Display movies sorted by year."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    while True:
        order = input(f"{Colors.INPUT}Sort by latest or oldest first? (l/o): {Colors.ENDC}").strip().lower()
        if order in ['l', 'o']:
            break
        print(f"{Colors.ERROR}Invalid choice. Please enter 'l' for latest or 'o' for oldest.{Colors.ENDC}")

    reverse = order == 'l'
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse)

    print(f"\n{Colors.CYAN}Movies sorted by year ({'latest' if reverse else 'oldest'} first):{Colors.ENDC}")
    for i, (title, data) in enumerate(sorted_movies, 1):
        _display_movie_card(i, title, data)


def sort_by_rating(movies: Dict[str, Dict]) -> None:
    """Display movies sorted by rating (highest first)."""
    if not movies:
        print(f"{Colors.ERROR}No movies in the database.{Colors.ENDC}")
        return

    print(f"\n{Colors.CYAN}Movies sorted by rating (highest first):{Colors.ENDC}")
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for i, (title, data) in enumerate(sorted_movies, 1):
        _display_movie_card(i, title, data)


def main() -> None:
    """Main function to run the movie database application."""
    clear_screen()
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load movies from file
    movies = movie_storage.get_movies()
    
    while True:
        try:
            display_main_menu()
            choice = input(f"\n{Colors.INPUT}Enter choice (0-3): {Colors.ENDC}").strip()

            if choice == '0':
                print(f"\n{Colors.GREEN}Goodbye!{Colors.ENDC}")
                break
            elif choice == '1':
                handle_display_movies_menu(movies)
            elif choice == '2':
                handle_edit_movies_menu(movies)
            elif choice == '3':
                handle_stats_menu(movies)
            elif choice == '4' and REQUESTS_AVAILABLE:
                handle_settings_menu()
            else:
                print(f"{Colors.ERROR}Invalid choice. Please enter a number between 0 and {3 if not REQUESTS_AVAILABLE else 4}.{Colors.ENDC}")

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Operation cancelled.{Colors.ENDC}")
            continue
        except Exception as e:
            print(f"\n{Colors.ERROR}An error occurred: {e}{Colors.ENDC}")
            continue


if __name__ == "__main__":
    main()