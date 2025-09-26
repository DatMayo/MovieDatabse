#!/usr/bin/env python3
"""
==============================
My Movies Database Application
==============================

This is the main entry point for the My Movies Database application.

It initializes the necessary components and runs the main application loop.
The core logic is delegated to the MovieManager and UserInterface classes
to maintain a clean and organized structure.
"""

import signal
import sys

import movie_storage
from movie_manager import MovieManager, REQUESTS_AVAILABLE
from ui import Colors, UserInterface


class App:
    """The main application class that orchestrates the UI and movie management."""

    def __init__(self):
        """Initializes the App."""
        api_key_exists = bool(movie_storage.get_api_key())
        self.ui = UserInterface(REQUESTS_AVAILABLE, api_key_exists)
        self.manager = MovieManager()

    def run(self):
        """Run the main application loop."""
        signal.signal(signal.SIGINT, self._signal_handler)

        while True:
            self.ui.display_main_menu()
            choice = self.ui.get_input("Enter choice: ")

            if choice == "0":
                self.ui.print_message("\nGoodbye!", Colors.GREEN)
                break
            elif choice == "1":
                self._handle_display_movies_menu()
            elif choice == "2":
                self._handle_edit_movies_menu()
            elif choice == "3":
                self._handle_stats_menu()
            elif choice == "4" and REQUESTS_AVAILABLE:
                self._handle_settings_menu()
            else:
                self.ui.print_message("Invalid choice.", Colors.ERROR)
                self.ui.press_enter_to_continue()

    def _signal_handler(self, sig, frame):
        """Handle keyboard interrupt (Ctrl+C) gracefully."""
        self.ui.print_message("\n\nOperation cancelled by user.", Colors.WARNING)
        self.ui.print_message("Goodbye!", Colors.GREEN)
        sys.exit(0)

    def _handle_display_movies_menu(self):
        """Handle the display movies submenu."""
        while True:
            self.ui.display_movies_menu()
            choice = self.ui.get_input("Enter choice: ")
            if choice == "0":
                break
            elif choice == "1":
                self.ui.display_movie_list(self.manager.get_all_movies())
            elif choice == "2":
                self._search_movie()
            elif choice == "3":
                self._filter_movies()
            elif choice == "4":
                sorted_movies = self.manager.sort_movies("rating")
                self.ui.display_movie_list(dict(sorted_movies))
            elif choice == "5":
                self._sort_by_year()
            else:
                self.ui.print_message("Invalid choice.", Colors.ERROR)
            if choice != "1":  # Pagination handles its own continuation
                self.ui.press_enter_to_continue()

    def _handle_edit_movies_menu(self):
        """Handle the edit movies submenu."""
        while True:
            self.ui.display_edit_menu()
            choice = self.ui.get_input("Enter choice: ")
            if choice == "0":
                break
            elif choice == "1":
                self._add_movie_manually()
            elif choice == "2" and REQUESTS_AVAILABLE and movie_storage.get_api_key():
                self._add_movie_from_omdb()
            elif choice == "3":
                self._update_movie()
            elif choice == "4":
                self._delete_movie()
            else:
                self.ui.print_message("Invalid choice.", Colors.ERROR)
            self.ui.press_enter_to_continue()

    def _handle_stats_menu(self):
        """Handle the statistics submenu."""
        while True:
            self.ui.display_stats_menu()
            choice = self.ui.get_input("Enter choice: ")
            if choice == "0":
                break
            elif choice == "1":
                self._show_stats()
            elif choice == "2":
                self._random_movie()
            else:
                self.ui.print_message("Invalid choice.", Colors.ERROR)
            self.ui.press_enter_to_continue()

    def _handle_settings_menu(self):
        """Handle the settings submenu."""
        while True:
            self.ui.display_settings_menu()
            choice = self.ui.get_input("Enter choice: ")
            if choice == "0":
                break
            elif choice == "1":
                api_key = self.ui.get_input("Enter your OMDb API key: ")
                movie_storage.save_api_key(api_key)
                self.ui.print_message("API key saved.", Colors.SUCCESS)
            elif choice == "2":
                api_key = movie_storage.get_api_key()
                if api_key:
                    self.ui.print_message(f"Current API Key: {api_key}")
                else:
                    self.ui.print_message("No API key set.", Colors.WARNING)
            else:
                self.ui.print_message("Invalid choice.", Colors.ERROR)
            self.ui.press_enter_to_continue()

    def _add_movie_manually(self):
        """Add a movie to the database manually."""
        try:
            title = self.ui.get_input("Enter movie title: ")
            if not title:
                self.ui.print_message("Movie title cannot be empty.", Colors.ERROR)
                return
            rating = self.ui.get_rating_input("Enter movie rating (0-10): ")
            year = self.ui.get_year_input("Enter movie year: ")
            success, message = self.manager.add_movie_manually(title, rating, year)
            color = Colors.SUCCESS if success else Colors.ERROR
            self.ui.print_message(message, color)
        except KeyboardInterrupt:
            self.ui.print_message("\nMovie addition cancelled.", Colors.WARNING)

    def _add_movie_from_omdb(self):
        """Add a movie using data from OMDb."""
        query = self.ui.get_input("Enter movie title to search online: ")
        if not query:
            self.ui.print_message("Please enter a search term.", Colors.ERROR)
            return

        movie_data, error = self.manager.search_movie_online(query)
        if error:
            self.ui.print_message(error, Colors.ERROR)
            return

        title = movie_data.get("Title")
        success, message = self.manager.add_movie_from_omdb(title, movie_data)
        color = Colors.SUCCESS if success else Colors.ERROR
        self.ui.print_message(message, color)

    def _delete_movie(self):
        """Delete a movie from the database."""
        title = self.ui.get_input("Enter movie title to delete: ")
        success, message = self.manager.delete_movie(title)
        color = Colors.SUCCESS if success else Colors.ERROR
        self.ui.print_message(message, color)

    def _update_movie(self):
        """Update a movie's details."""
        title = self.ui.get_input("Enter movie title to update: ")
        if title not in self.manager.get_all_movies():
            self.ui.print_message(f"Movie '{title}' not found!", Colors.ERROR)
            return

        field = self.ui.get_input("Enter field to update (year, rating): ").lower()
        if field == "year":
            value = self.ui.get_year_input("Enter new year: ")
        elif field == "rating":
            value = self.ui.get_rating_input("Enter new rating: ")
        else:
            self.ui.print_message("Invalid field.", Colors.ERROR)
            return

        success, message = self.manager.update_movie_field(title, field, value)
        self.ui.print_message(message, Colors.SUCCESS)

    def _show_stats(self):
        """Display movie statistics."""
        stats = self.manager.get_stats()
        if not stats:
            self.ui.print_message("No movies in the database.", Colors.ERROR)
            return

        self.ui.print_message("Movie Statistics:", Colors.CYAN)
        self.ui.print_message(f"Total movies: {stats['total_movies']}")
        self.ui.print_message(f"Average rating: {stats['avg_rating']:.1f}")
        self.ui.print_message(f"Median rating: {stats['median_rating']:.1f}")

        best_titles, max_rating = stats["best_movies"]
        worst_titles, min_rating = stats["worst_movies"]
        self.ui.print_message(
            f"Best movie(s): {', '.join(best_titles)} ({max_rating:.1f})"
        )
        self.ui.print_message(
            f"Worst movie(s): {', '.join(worst_titles)} ({min_rating:.1f})"
        )

    def _random_movie(self):
        """Display a random movie."""
        title, data = self.manager.get_random_movie()
        if not title:
            self.ui.print_message("No movies in the database.", Colors.ERROR)
            return

        self.ui.print_message("Your random movie is:", Colors.GREEN)
        self.ui.display_movie_card(1, title, data)

    def _search_movie(self):
        """Search for movies by a query."""
        query = self.ui.get_input("Enter search term (e.g., 'a:Tom Hanks'): ")
        if not query:
            self.ui.print_message("Please enter a search term.", Colors.ERROR)
            return

        results = self.manager.search_movies(query)
        if results is None:
            self.ui.print_message("Invalid search format.", Colors.ERROR)
        elif not results:
            self.ui.print_message("No movies found.", Colors.WARNING)
        else:
            self.ui.display_movie_list(dict(results))

    def _filter_movies(self):
        """Filter movies by rating and year."""
        min_rating_str = self.ui.get_input("Min rating (optional): ")
        start_year_str = self.ui.get_input("Start year (optional): ")
        end_year_str = self.ui.get_input("End year (optional): ")

        min_rating = float(min_rating_str) if min_rating_str else None
        start_year = int(start_year_str) if start_year_str else None
        end_year = int(end_year_str) if end_year_str else None

        results = self.manager.filter_movies(min_rating, start_year, end_year)
        self.ui.display_movie_list(results)

    def _sort_by_year(self):
        """Sort movies by year."""
        order = self.ui.get_input("Sort by latest or oldest first? (l/o): ").lower()
        reverse = order == "l"
        sorted_movies = self.manager.sort_movies("year", reverse)
        self.ui.display_movie_list(dict(sorted_movies))


if __name__ == "__main__":
    app = App()
    app.run()
