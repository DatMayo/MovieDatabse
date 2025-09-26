"""This module provides the user interface for the movie database application."""

import os
import textwrap


class Colors:
    """ANSI color codes for terminal text formatting."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    INPUT = "\033[94m"  # Blue for user input
    MENU = "\033[95m"  # Purple for menu
    ERROR = "\033[91m"  # Red for errors
    SUCCESS = "\033[92m"  # Green for success messages


class UserInterface:
    """Handle all user interface elements, including menus and input/output."""

    def __init__(self, requests_available, api_key_exists):
        """Initialize the UserInterface."""
        self.requests_available = requests_available
        self.api_key_exists = api_key_exists

    def clear_screen(self):
        """Clear the screen using the appropriate command for the OS."""
        os.system("cls" if os.name == "nt" else "clear")

    def display_main_menu(self):
        """Display the main menu options."""
        self.clear_screen()
        print(
            f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********"
            f"{Colors.ENDC}"
        )
        print(f"\n{Colors.MENU}Main Menu:{Colors.ENDC}")
        print(f"{Colors.MENU}1.{Colors.ENDC} Display Movies")
        print(f"{Colors.MENU}2.{Colors.ENDC} Edit Movies")
        print(f"{Colors.MENU}3.{Colors.ENDC} Statistics & Fun")
        if self.requests_available:
            print(f"{Colors.MENU}4.{Colors.ENDC} Settings")
        print(f"{Colors.MENU}0.{Colors.ENDC} Exit")

    def display_movies_menu(self):
        """Display the movies submenu options."""
        self.clear_screen()
        print(
            f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********"
            f"{Colors.ENDC}"
        )
        print(f"\n{Colors.MENU}Display Movies Menu:{Colors.ENDC}")
        print(f"{Colors.MENU}1.{Colors.ENDC} List all movies")
        print(f"{Colors.MENU}2.{Colors.ENDC} Search movie")
        print(f"{Colors.MENU}3.{Colors.ENDC} Filter movies")
        print(f"{Colors.MENU}4.{Colors.ENDC} Sort by rating")
        print(f"{Colors.MENU}5.{Colors.ENDC} Sort by year")
        print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

    def display_edit_menu(self):
        """Display the edit submenu options."""
        self.clear_screen()
        print(
            f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********"
            f"{Colors.ENDC}"
        )
        print(f"\n{Colors.MENU}Edit Movies Menu:{Colors.ENDC}")
        print(f"{Colors.MENU}1.{Colors.ENDC} Add movie manually")
        if self.requests_available and self.api_key_exists:
            print(f"{Colors.MENU}2.{Colors.ENDC} Add movie from OMDb")
        print(f"{Colors.MENU}3.{Colors.ENDC} Update movie")
        print(f"{Colors.MENU}4.{Colors.ENDC} Delete movie")
        print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

    def display_settings_menu(self):
        """Display the settings submenu options."""
        self.clear_screen()
        print(
            f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********"
            f"{Colors.ENDC}"
        )
        print(f"\n{Colors.MENU}Settings Menu:{Colors.ENDC}")
        print(f"{Colors.MENU}1.{Colors.ENDC} Set OMDb API Key")
        print(f"{Colors.MENU}2.{Colors.ENDC} View OMDb API Key")
        print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

    def display_stats_menu(self):
        """Display the statistics submenu options."""
        self.clear_screen()
        print(
            f"\n{Colors.HEADER}{Colors.BOLD}********** My Movies Database **********"
            f"{Colors.ENDC}"
        )
        print(f"\n{Colors.MENU}Statistics & Fun Menu:{Colors.ENDC}")
        print(f"{Colors.MENU}1.{Colors.ENDC} Show stats")
        print(f"{Colors.MENU}2.{Colors.ENDC} Random movie")
        print(f"{Colors.MENU}0.{Colors.ENDC} Back to main menu")

    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        return input(f"{Colors.INPUT}{prompt}{Colors.ENDC}").strip()

    def get_year_input(self, prompt: str) -> int:
        """Get and validate a movie release year from user input."""
        while True:
            try:
                year = int(self.get_input(prompt))
                if year > 0:
                    return year
                self.print_message(
                    "Year must be a positive number.", Colors.WARNING
                )
            except ValueError:
                self.print_message("Please enter a valid year.", Colors.ERROR)
            except KeyboardInterrupt:
                print()  # Move to new line after Ctrl+C
                raise

    def get_rating_input(self, prompt: str) -> float:
        """Get and validate a movie rating from user input."""
        while True:
            try:
                rating = float(self.get_input(prompt))
                if 0 <= rating <= 10:
                    return rating
                self.print_message(
                    "Rating must be between 0 and 10.", Colors.WARNING
                )
            except ValueError:
                self.print_message(
                    "Please enter a valid number.", Colors.ERROR
                )
            except KeyboardInterrupt:
                print()  # Move to new line after Ctrl+C
                raise

    def print_message(self, message: str, color: str = Colors.ENDC):
        """Print a message to the console with a given color."""
        print(f"{color}{message}{Colors.ENDC}")

    def press_enter_to_continue(self):
        """Prompt the user to press Enter to continue."""
        self.get_input("\nPress Enter to continue...")

    def display_movie_card(self, index: int, title: str, data: dict):
        """Display a single movie in a card-like format."""
        print(f"\n{Colors.HEADER}{index}. {title}{Colors.ENDC}")
        print(f"   {Colors.BOLD}Year:{Colors.ENDC} {data.get('year', 'N/A')}")
        print(
            f"   {Colors.BOLD}Rating:{Colors.ENDC} {data.get('rating', 'N/A'):.1f}"
        )
        if "description" in data:
            wrapped_description = textwrap.wrap(data["description"], width=70)
            print(f"   {Colors.BOLD}Description:{Colors.ENDC}")
            for line in wrapped_description:
                print(f"     {line}")
        if "actors" in data:
            print(
                f"   {Colors.BOLD}Actors:{Colors.ENDC} {', '.join(data['actors'])}"
            )

    def display_movie_list(self, movies: dict):
        """Display a list of movies with pagination."""
        if not movies:
            self.print_message("No movies to display.", Colors.WARNING)
            return

        movie_list = list(movies.items())
        total_movies = len(movie_list)
        page_size = 10
        num_pages = (total_movies + page_size - 1) // page_size
        current_page = 0

        while True:
            self.clear_screen()
            self.print_message(
                f"List of all movies (Page {current_page + 1}/{num_pages}):",
                Colors.CYAN,
            )
            start_index = current_page * page_size
            end_index = start_index + page_size
            for i, (title, data) in enumerate(
                movie_list[start_index:end_index], start=start_index + 1
            ):
                self.display_movie_card(i, title, data)

            print("\n'n' for next page, 'p' for previous, 'q' to quit")
            choice = self.get_input("Enter choice: ").lower()

            if choice == "n":
                if current_page < num_pages - 1:
                    current_page += 1
                else:
                    self.print_message(
                        "You are on the last page.", Colors.WARNING
                    )
                    self.press_enter_to_continue()
            elif choice == "p":
                if current_page > 0:
                    current_page -= 1
                else:
                    self.print_message(
                        "You are on the first page.", Colors.WARNING
                    )
                    self.press_enter_to_continue()
            elif choice == "q":
                break
            else:
                self.print_message("Invalid choice.", Colors.ERROR)
                self.press_enter_to_continue()
