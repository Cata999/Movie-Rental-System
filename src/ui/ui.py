

from faker import Faker
from datetime import date, timedelta


from src.services.undo_service import UndoService
from src.exceptions.exceptions import MovieRentalException, ClientError, MovieError, RentalError, UndoRedoError
from src.services.services import ClientServices, MovieServices, RentalServices
from src.domain.domain import Client, Movie, Rental
from src.repository.repository import ClientRepository, MovieRepository, RentalRepository
from src.repository.file_repository import (
    FileClientRepository, FileMovieRepository, FileRentalRepository,
    BinaryClientRepository, BinaryMovieRepository, BinaryRentalRepository)



class UI:
    def __init__(self, client_services, movie_services, rental_services, undo_service):
        self.client_services = client_services
        self.movie_services = movie_services
        self.rental_services = rental_services
        self.undo_service = undo_service


    def print_menu(self):
        print("""
        ~~~~~~~~Menu~~~~~~~
        1. Manage clients
        2. Manage movies
        3. Manage rentals
        4. Search for clients or movies
        5. Undo/Redo
        6. Show statistics
        0.Exit
        """)

    def print_manage_clients(self):
        print("""
        --- Manage clients ---
1. Add client
2. Remove client
3. Update client name
4. List clients
0. Back
""")

    def print_manage_movies(self):
        print("""
        --- Manage movies ---
1. Add movie
2. Remove movie
3. Update movie name/title/description/genre
4. List movies
0. Back
""")

    def print_movie_update_options(self):
        print("""
        --- Movie update ---
1. Title
2. Description
3. Genre
0. Back
""")

    def print_rent_or_return(self):
        print("""
        --- Rent or Return ---

1. Rent
2. Return a movie
3. List rentals
0. Back
""")

    def print_search_options(self):
        print("""
        --- Search ---
1. Search Clients
2. Search Movies
0. Back
""")

    def print_undo_redo_menu(self):
        print("""
        --- Undo/Redo ---
1. Undo last operation
2. Redo last undone operation
0. Back
""")
    def print_statistics_menu(self):
        print("""
        --- Statistics ---
1. Display most rented movies
2. Display most active clients
3. Display late rentals
0. Back 
        """)
    def search_menu(self):
        while True:
            self.print_search_options()
            choice = input("Enter your search choice: ")

            if choice == "1":
                search_term = input("Enter search term (ID or Name): ")
                results = self.client_services.search_client(search_term)
                self.display_results("Clients", results)
            elif choice == "2":
                search_term = input("Enter search term (ID, Title, Description, or Genre): ")
                results = self.movie_services.search_movie(search_term)
                self.display_results("Movies", results)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def display_results(self, entity_type, results):
        """Helper function to print search results."""
        if not results:
            print(f"\n--- No matching {entity_type} found. ---\n")
            return

        print(f"\n--- {entity_type} Search Results ({len(results)} found) ---")
        for item in results:
            print(item)
        print("----------------------------------------\n")

    def undo_redo_menu(self):
        while True:
            self.print_undo_redo_menu()
            choice = input("Enter choice: ")

            try:
                if choice == "1":
                    self.undo_service.undo()
                    print("\nOperation Undone successfully.")
                elif choice == "2":
                    self.undo_service.redo()
                    print("\nOperation Redone successfully.")
                elif choice == "0":
                    break
                else:
                    raise ValueError("Invalid choice")
            except UndoRedoError as e:
                print(f"\nUNDO/REDO ERROR: {e}\n")
            except Exception as e:
                print(f"\nUNEXPECTED SYSTEM ERROR during undo/redo: {e}\n")

    def statistics_menu(self):
        while True:
                self.print_statistics_menu()
                choice = input("Enter choice: ")
                try:
                    if choice == "1":
                        results = self.rental_services.get_most_rented_movies()
                        self.display_statistics_results("Most Rented Movies (by days)", results, "days rented")
                    elif choice == "2":
                        results = self.rental_services.get_most_active_clients()
                        self.display_statistics_results("Most Active Clients (by rental days)", results, "rental days")
                    elif choice == "3":
                        results = self.rental_services.get_late_rentals()
                        self.display_late_rentals_results(results)
                    elif choice == "0":
                        break
                    else:
                        raise ValueError("Invalid choice")
                except Exception as e:
                    print(f"\nSTATISTICS ERROR: Failed to generate report: {e}\n")

    def display_statistics_results(self, title, results, unit):
        """Helper for displaying simple sorted lists (Movies/Clients)."""
        print(f"\n--- {title} ---")
        if not results:
            print("No data available.")
            return

        # Results are (Entity object, value)
        for entity, value in results:
            print(f"{entity} - {value} {unit}")
        print("--------------------------------\n")

    def display_late_rentals_results(self, results):
        """Helper for displaying late rentals with full context."""
        print(f"\n--- Late Rentals (Sorted by Days of Delay) ---")
        if not results:
            print("No overdue rentals found.")
            return

        for rental, movie, client, delay_days in results:
            print(
                f"Delay: {delay_days} days | Movie: {movie.title} (ID: {movie.id}) | Client: {client.name} (ID: {client.id}) | Due: {rental.due_date.isoformat()}")
        print("--------------------------------------------------\n")

    def run(self):
        while True:
            try:
                self.print_menu()
                choice = input("Enter your choice: ")
                if choice == "1":
                    while True:
                        self.print_manage_clients()
                        choice_2 = input("Enter your choice: ")
                        if choice_2 == "1":
                            client_id = int(input("Enter client id: "))
                            client_name = input("Enter client name: ")
                            self.client_services.add(client_id, client_name)
                            print("Added client.")
                        elif choice_2 == "2":
                            client_id = int(input("Enter client id to remove: "))
                            self.client_services.remove(client_id)
                            print("Removed client.")
                        elif choice_2 == "3":
                            client_id = int(input("Enter client id to update: "))
                            new_name = input("Enter new client name: ")
                            self.client_services.update_client_name(client_id, new_name)
                            print("Updated client.")
                        elif choice_2 == "4":
                            for elem in self.client_services.list_clients():
                                print(elem)
                        elif choice_2 == "0":
                            print("\n")
                            break
                        else:
                            raise MovieRentalException("Invalid choice in Client Menu.")

                elif choice == "2":
                    while True:
                        self.print_manage_movies()
                        choice_3 = input("Enter your choice: ")
                        if choice_3 == "1":
                            movie_id = int(input("Enter movie id: "))
                            movie_name = input("Enter movie name: ")
                            movie_description = input("Enter movie description: ")
                            movie_genre = input("Enter movie genre: ")
                            self.movie_services.add(movie_id, movie_name, movie_description, movie_genre)
                            print("Added movie.")
                        elif choice_3 == "2":
                            movie_id = int(input("Enter movie id to remove: "))
                            self.movie_services.remove(movie_id)
                            print("Removed movie.")
                        elif choice_3 == "3":
                            movie_id = int(input("Enter movie id to update: "))
                            self.print_movie_update_options()
                            update_choice = input("Enter your choice: ")
                            if update_choice == "1":
                                new_name = input("Enter new movie name: ")
                                self.movie_services.update_movie_title(movie_id, new_name)
                            elif update_choice == "2":
                                new_description = input("Enter new movie description: ")
                                self.movie_services.update_movie_description(movie_id, new_description)
                            elif update_choice == "3":
                                new_genre = input("Enter new movie genre: ")
                                self.movie_services.update_movie_genre(movie_id, new_genre)
                            elif update_choice == "0":
                                print("\nReturning to Manage Movies menu...")
                                break
                            else:
                                raise MovieRentalException("Invalid choice in Movie Update Menu.")
                        elif choice_3 == "4":
                            for elem in self.movie_services.list_movies():
                                print(elem)
                        elif choice_3 == "0":
                            print("\nReturning to main menu...")
                            break
                        else:
                            raise MovieRentalException("Invalid choice in Movie Menu.")

                elif choice == "3":
                    self.print_rent_or_return()
                    choice_4 = input("Enter your choice: ")
                    if choice_4 == "1":
                        rental_id = int(input("Enter rental id: "))
                        client_id = int(input("Enter client id: "))
                        movie_id = int(input("Enter movie id: "))
                        rented_date = date.today()
                        rental_duration = timedelta(days=14)
                        due_date = rented_date + rental_duration
                        return_date = None
                        self.rental_services.rent_movie(rental_id, movie_id, client_id, rented_date, due_date,
                                                        return_date)
                        print("Movie successfully rented.")
                    elif choice_4 == "2":
                        rental_id = int(input("Enter the rental id to return: "))

                        tokens = input("Enter return date (YYYY MM DD): ").split()
                        if len(tokens) != 3:
                            raise MovieRentalException(
                                "Date input must contain exactly three values: Year, Month, Day.")

                        year = int(tokens[0])
                        month = int(tokens[1])
                        day = int(tokens[2])

                        return_date = date(year, month, day)
                        self.rental_services.return_movie(rental_id, return_date)
                        print("Movie successfully returned.")

                    elif choice_4 == "3":
                        for elem in self.rental_services.list_rentals():
                            print(elem)
                    elif choice_4 == "0":
                        pass
                    else:
                        raise MovieRentalException("Invalid choice in Rental Menu.")

                elif choice == "4":
                    self.search_menu()
                elif choice == "5":
                    self.undo_redo_menu()
                elif choice == "6":
                    self.statistics_menu()
                elif choice == "0":
                    print("\nExiting application...")
                    break
                else:
                    raise MovieRentalException("Invalid choice in Main Menu.")

            # 1. CATCH CUSTOM APPLICATION ERRORS
            except MovieRentalException as e:
                print(f"\nAPPLICATION ERROR: {e}\n")

            # 2. CATCH VALUE ERRORS (for failed int() or date() conversions)
            except ValueError as e:
                print(f"\nINPUT ERROR: Please enter valid numeric data or a valid date.\nDetail: {e}\n")

            # 3. CATCH UNEXPECTED SYSTEM ERRORS (for robustness)
            except Exception as e:
                print(f"\nUNEXPECTED SYSTEM ERROR: An unhandled error occurred: {e}\n")


if __name__ == "__main__":
    import random

    try:
        from src.settings.settings import Settings

        settings = Settings()
    except Exception as e:
        print(f"ERROR: Could not load settings.properties or Settings class. Detail: {e}. Using default inmemory.")


        class MockSettings:
            def get_repo_type(self): return "inmemory"

            def get_file_path(self, entity): return f"{entity}.txt"


        settings = MockSettings()

    repo_type = settings.get_repo_type().lower()


    if repo_type == "inmemory":
        client_repo = ClientRepository()
        movie_repo = MovieRepository()
        rental_repo = RentalRepository()

    elif repo_type == "textfiles":
        client_repo = FileClientRepository(settings.get_file_path("clients"))
        movie_repo = FileMovieRepository(settings.get_file_path("movies"))
        rental_repo = FileRentalRepository(settings.get_file_path("rentals"))

    elif repo_type == "binaryfiles":
        client_repo = BinaryClientRepository(settings.get_file_path("clients"))
        movie_repo = BinaryMovieRepository(settings.get_file_path("movies"))
        rental_repo = BinaryRentalRepository(settings.get_file_path("rentals"))

    else:
        print(f"Invalid repository type '{repo_type}' specified in settings. Using inmemory.")
        client_repo = ClientRepository()
        movie_repo = MovieRepository()
        rental_repo = RentalRepository()

    test_movie = Movie(1, "Fight Club", "The family guy spinoff", " Action")
    test_client = Client(1, "John Pork")

    test_rental = Rental(1, test_movie.id, test_client.id, date(2025, 12, 15), date(2025, 12, 29), None)
    if not movie_repo.get_all():
        movie_repo.add(test_movie)
    if not client_repo.get_all():
        client_repo.add(test_client)
    if not rental_repo.get_all():
        rental_repo.add(test_rental)

    fake = Faker()
    if len(client_repo.get_all()) == 1:
        for _ in range(25):
            name = fake.name()
            client_id = random.randint(1000, 6000)
            client = Client(client_id, name)
            client_repo.add(client)

    if len(movie_repo.get_all()) == 1:
        for _ in range(25):
            title = fake.name()
            movie_id = random.randint(1000, 6000)
            movie_description = fake.paragraph(nb_sentences=2)
            movie_genre = random.choice(["Action", "Comedy", "Drama", "Sci-Fi", "Horror"])
            movie = Movie(movie_id, title, movie_description, movie_genre)
            movie_repo.add(movie)

    # Generate 25 Rentals
    client_list = client_repo.get_all()
    movie_list = movie_repo.get_all()

    if len(client_list) > 0 and len(movie_list) > 0 and len(rental_repo.get_all()) == 1:
        for _ in range(25):
            rental_id = random.randint(1000, 6000)

            client_id = random.choice(client_list).id
            movie_id = random.choice(movie_list).id

            rented_date = fake.date_object()
            due_date = rented_date + timedelta(days=random.randint(7, 14))  # 1-2 week rental period
            returned_date = None


            if random.random() < 0.3:  # 30% of movies are returned initially
                returned_date = due_date + timedelta(days=random.randint(-5, 5))

            rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
            rental_repo.add(rental)
    undo_service = UndoService()
    client_services = ClientServices(client_repo, undo_service)
    movie_services = MovieServices(movie_repo, undo_service)
    rental_services = RentalServices(rental_repo, client_repo, movie_repo, undo_service)



    ui = UI(client_services, movie_services, rental_services, undo_service)
    ui.run()