"""Write an application for movie rentals. The application will store:'
- **Movie**: `movie_id`, `title`, `description`, `genre`
- **Client**: `client_id`, `name`
- **Rental**: `rental_id`, `movie_id`, `client_id`, `rented_date`, `due_date`, `returned_date`

Create an application which allows to:
1. Manage clients and movies. The user can add, remove, update, and list both clients and movies.
2. Rent or return a movie. A client can rent a movie until a given date, as long as they have no rented movies that passed their due date for return. A client can return a rented movie at any time.
3. Search for clients or movies using any one of their fields (e.g. movies can be searched for using id, title, description or genre). The search must work using case-insensitive, partial string matching, and must return all matching items.
"""
from datetime import date

from src.domain.domain import Movie, Client, Rental
from src.exceptions.exceptions import ClientError, MovieError, RentalError
from src.services.undo_service import FunctionCall, Operation

# Helper function to convert input ID string to int safely
def _safe_int_conversion(id_str, entity_name):
    try:
        if not id_str:
            raise ValueError()
        return int(id_str)
    except ValueError:
        if entity_name == "Client":
            raise ClientError(f"{entity_name} ID must be a numeric integer.")
        elif entity_name == "Movie":
            raise MovieError(f"{entity_name} ID must be a numeric integer.")
        elif entity_name == "Rental":
            raise RentalError(f"{entity_name} ID must be a numeric integer.")
        else:
            raise ValueError(f"ID for {entity_name} must be numeric.")

class ClientServices:
    def __init__(self, repo, undo_service):
        self.repo = repo
        self.__undo_service = undo_service

    def add(self, client_id, name):
        existing_client = self.repo.find(client_id)
        if existing_client is not None:
            raise ClientError(f"Client with ID {client_id} already exists.")
        client = Client(client_id, name)
        self.repo.add(client)

        undo_call = FunctionCall(self.repo.remove, client)
        redo_call = FunctionCall(self.repo.add, client)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def remove(self, client_id):
        client_id = _safe_int_conversion(client_id, "Client")
        # get the actual stored instance, then remove it
        client = self.repo.find(client_id)
        if client is None:
            raise ClientError(f"Client with id {client_id} does not exist")
        self.repo.remove(client)

        undo_call = FunctionCall(self.repo.add, client)
        redo_call = FunctionCall(self.repo.remove, client)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def update_client_name(self, client_id, new_name):
        client = self.repo.find(client_id)
        if client is None:
            raise ClientError("Could not find client with id {}".format(client_id))

        old_name = client.name
        client.set_name(new_name)

        undo_call = FunctionCall(client.set_name, old_name)
        redo_call = FunctionCall(client.set_name, new_name)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def list_clients(self):
        return self.repo.get_all()

    def search_client(self, search_term):
        """
        Searches clients by ID or Name (case-insensitive, partial matching).
        """
        if not search_term:
            return self.repo.get_all()

        search_term = str(search_term).lower()
        results = []

        for client in self.repo.get_all():
            # Check Client ID (must handle both string search term and integer ID)
            if search_term in str(client.id):
                results.append(client)
                continue

            # Check Client Name
            if search_term in client.name.lower():
                results.append(client)
                continue

        return results

class MovieServices:
    def __init__(self, repo, undo_service):
        self.repo = repo
        self.__undo_service = undo_service

    def add(self, movie_id, title, description, genre):
        movie_id = _safe_int_conversion(movie_id, "Movie")

        existing_movie = self.repo.find(movie_id)
        if existing_movie is not None:
            raise MovieError(f"Movie with ID {movie_id} already exists.")
        movie = Movie(movie_id, title, description, genre)

        self.repo.add(movie)

        # UNDO/REDO Logic for ADD
        undo_call = FunctionCall(self.repo.remove, movie)
        redo_call = FunctionCall(self.repo.add, movie)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def remove(self, movie_id_str):
        movie_id = _safe_int_conversion(movie_id_str, "Movie")

        movie = self.repo.find(movie_id)
        if movie is None:
            raise MovieError(f"Movie with ID {movie_id} does not exist")

        self.repo.remove(movie)

        # UNDO/REDO Logic for REMOVE
        undo_call = FunctionCall(self.repo.add, movie)
        redo_call = FunctionCall(self.repo.remove, movie)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def update_movie_title(self, movie_id, name):
        movie_id = _safe_int_conversion(movie_id, "Movie")
        movie = self.repo.find(movie_id)
        if movie is None:
            raise MovieError(f"Movie with ID {movie_id} does not exist")

        old_title = movie.title
        movie.set_title(name)

        # UNDO/REDO Logic for UPDATE
        undo_call = FunctionCall(movie.set_title, old_title)
        redo_call = FunctionCall(movie.set_title, name)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def update_movie_description(self, movie_id, description):
        movie_id = _safe_int_conversion(movie_id, "Movie")
        movie = self.repo.find(movie_id)
        if movie_id is None:
            raise MovieError(f"Movie with ID {movie_id} does not exist")

        old_description = movie.description
        movie.set_description(description)

        undo_call = FunctionCall(movie.set_description, old_description)
        redo_call = FunctionCall(movie.set_description, description)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def update_movie_genre(self, movie_id, genre):
        movie_id = _safe_int_conversion(movie_id, "Movie")
        movie = self.repo.find(movie_id)
        if movie_id is None:
            raise MovieError(f"Movie with ID {movie_id} does not exist")
        old_genre = movie.genre
        movie.set_genre(genre)

        undo_call = FunctionCall(movie.set_genre, old_genre)
        redo_call = FunctionCall(movie.set_genre, genre)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def list_movies(self):
        return self.repo.get_all()

    def search_movie(self, search_term):
        """
                Searches movies by ID, Title, Description, or Genre
                (case-insensitive, partial matching).
                """
        if not search_term:
            return self.repo.get_all()

        search_term = str(search_term).lower()
        results = []

        for movie in self.repo.get_all():
            # Check Movie ID
            if search_term in str(movie.id):
                results.append(movie)
                continue

            # Check Title
            if search_term in movie.title.lower():
                results.append(movie)
                continue

            # Check Description
            if search_term in movie.description.lower():
                results.append(movie)
                continue

            # Check Genre
            if search_term in movie.genre.lower():
                results.append(movie)
                continue

        return results


class RentalServices:
    def __init__(self, repo, client_repo, movie_repo, undo_service):
        self.repo = repo
        self.client_repo = client_repo
        self.movie_repo = movie_repo
        self.__undo_service = undo_service

    def rent_movie(self, rental_id_str, movie_id_str, client_id_str, rented_date, due_date, returned_date):
        rental_id = _safe_int_conversion(rental_id_str, "Rental")
        movie_id = _safe_int_conversion(movie_id_str, "Movie")
        client_id = _safe_int_conversion(client_id_str, "Client")

        # ... (Validation remains the same) ...
        existing_rental = self.repo.find(rental_id)
        if existing_rental is not None:
            raise RentalError(f"Rental with ID {rental_id} already exists.")
        if self.client_repo.find(client_id) is None:
            raise RentalError(f"Client with ID {client_id} does not exist.")
        if self.movie_repo.find(movie_id) is None:
            raise RentalError(f"Movie with ID {movie_id} does not exist.")
        for rental in self.repo.get_all():
            if rental.client_id == client_id and rental.returned_date is None:
                if rental.due_date < date.today():
                    raise RentalError(f"Client with ID {client_id} has an overdue movie and cannot rent another.")
        for rental in self.repo.get_all():
            if rental.movie_id == movie_id and rental.returned_date is None:
                raise RentalError(f"Movie with ID {movie_id} is currently rented.")

        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        self.repo.add(rental)

        # UNDO/REDO Logic for RENT
        undo_call = FunctionCall(self.repo.remove, rental)
        redo_call = FunctionCall(self.repo.add, rental)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def return_movie(self, rental_id_str, returned_date):
        rental_id = _safe_int_conversion(rental_id_str, "Rental")

        existing_rental = self.repo.find(rental_id)
        if existing_rental is None:
            raise RentalError(f"Rental with ID {rental_id} doesn't exist.")
        if existing_rental.returned_date is not None:
            raise RentalError(
                f"Rental with ID {rental_id} has already been returned on {existing_rental.returned_date}.")

        old_return_date = existing_rental.returned_date
        existing_rental.set_return_date(returned_date)

        # UNDO/REDO Logic for RETURN
        # NOTE: set_return_date is an object method, not a repository method
        undo_call = FunctionCall(existing_rental.set_return_date, old_return_date)  # sets back to None
        redo_call = FunctionCall(existing_rental.set_return_date, returned_date)
        operation = Operation(undo_call, redo_call)
        self.__undo_service.add_operation(operation)

    def list_rentals(self):
        return self.repo.get_all()

    # =======================================================
    # New Statistics Methods
    # =======================================================

    def get_most_rented_movies(self):
        """
        Provides the list of movies, sorted in descending order of the number of days they were rented.
        Returns a list of tuples: (Movie object, total_days_rented).
        """
        movie_rental_days = {}
        # NOTE: Using a fixed date for stable reporting
        today = date.today()

        for rental in self.repo.get_all():
            movie_id = rental.movie_id

            if rental.returned_date is not None:
                duration = (rental.returned_date - rental.rented_date).days
            else:
                # Movie is currently rented (days from rented date to today)
                duration = (today - rental.rented_date).days
                if duration < 0: duration = 0

            movie_rental_days[movie_id] = movie_rental_days.get(movie_id, 0) + duration

        # Map IDs to Movie objects and format the results
        results = []
        for movie_id, days in movie_rental_days.items():
            movie = self.movie_repo.find(movie_id)
            if movie:
                results.append((movie, days))

        # Sort descending by days
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_most_active_clients(self):
        """
        Provides the list of clients, sorted in descending order of the number of movie rental days they have.
        Returns a list of tuples: (Client object, total_rental_days).
        """
        client_rental_days = {}
        # NOTE: Using a fixed date for stable reporting
        today = date(2025, 12, 16)

        for rental in self.repo.get_all():
            client_id = rental.client_id

            if rental.returned_date is not None:
                duration = (rental.returned_date - rental.rented_date).days
            else:
                # Movie is currently rented
                duration = (today - rental.rented_date).days
                if duration < 0: duration = 0

            client_rental_days[client_id] = client_rental_days.get(client_id, 0) + duration

        # Map IDs to Client objects and format the results
        results = []
        for client_id, days in client_rental_days.items():
            client = self.client_repo.find(client_id)
            if client:
                results.append((client, days))

        # Sort descending by days
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_late_rentals(self):
        """
        Provides all currently rented movies that are overdue, sorted by days of delay.
        Returns a list of tuples: (Rental object, Movie object, Client object, days_of_delay).
        """
        late_rentals = []
        # NOTE: Using a fixed date for stable reporting
        today = date(2025, 12, 16)

        for rental in self.repo.get_all():
            # Check 1: Is it currently rented AND overdue?
            if rental.returned_date is None and rental.due_date < today:
                delay_days = (today - rental.due_date).days

                movie = self.movie_repo.find(rental.movie_id)
                client = self.client_repo.find(rental.client_id)

                if movie and client:
                    # Store Rental, Movie, Client, and Delay Days
                    late_rentals.append((rental, movie, client, delay_days))

        # Sort descending by days of delay (the last element in the tuple)
        late_rentals.sort(key=lambda x: x[3], reverse=True)
        return late_rentals
