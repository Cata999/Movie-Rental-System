from random import *
import faker

from src.domain.domain import Movie

"""Write an application for movie rentals. The application will store:
- **Movie**: `movie_id`, `title`, `description`, `genre`
- **Client**: `client_id`, `name`
- **Rental**: `rental_id`, `movie_id`, `client_id`, `rented_date`, `due_date`, `returned_date`

Create an application which allows to:
1. Manage clients and movies. The user can add, remove, update, and list both clients and movies.
2. Rent or return a movie. A client can rent a movie until a given date, as long as they have no rented movies that passed their due date for return. A client can return a rented movie at any time.
3. Search for clients or movies using any one of their fields (e.g. movies can be searched for using id, title, description or genre). The search must work using case-insensitive, partial string matching, and must return all matching items.
"""
class ClientRepository:
    def __init__(self):
        self._clients = []

    def add(self, client):
        """
        Add a client to the repository.
        :param client:
        :return:
        """
        self._clients.append(client)

    def remove(self, client):
        """
        Remove a client from the repository.
        :param client:
        :return:
        """
        self._clients.remove(client)

    def get_all(self):
        """
        Return a list of all clients.
        :return: list of clients
        """
        return list(self._clients)

    def set_all(self, data_list):
        """
        Sets the list of clients.
        :param data_list: new list of clients
        :return: None
        """
        self._clients = data_list

    def find(self, client_id: int) :
        """
        Return the Client with the given id, if it exists. Otherwise,
        return None
        """
        for client in self._clients:
            if int(client.id) == int(client_id):
                return client
        return None

    def __iter__(self):
        return iter(self._clients)

class MovieRepository:
    def __init__(self):
        self._movies = []

    def add(self, movie):
        """
        Add a movie to the repository.
        :param movie:
        :return:
        """
        self._movies.append(movie)

    def remove(self, movie):
        """
        Removes a movie from the repository.
        :param movie: The movie to be removed
        :return:
        """
        self._movies.remove(movie)

    def get_all(self):
        return self._movies

    def set_all(self, data_list):
        self._movies = data_list

    def find(self, movie_id):
        for movie in self._movies:
            if int(movie.id) == int(movie_id):
                return movie
        return None

class RentalRepository:

    def __init__(self):
        self._rentals = []

    def add(self, rental):
        self._rentals.append(rental)

    def remove(self, rental):
        self._rentals.remove(rental)

    def get_all(self):
        return self._rentals

    def set_all(self, data_list):
        self._rentals = data_list

    def find(self, rental_id):
        for rental in self._rentals:
            if int(rental.id) ==int(rental_id):
                return rental
        return None
    def get_by_client_id(self, client_id):
        for rental in self._rentals:
            if rental.client_id == client_id:
                return rental
        return None
    def __iter__(self):
        return iter(self._rentals)

