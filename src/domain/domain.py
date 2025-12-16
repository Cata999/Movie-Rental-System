"""Write an application for movie rentals. The application will store:'
- **Movie**: `movie_id`, `title`, `description`, `genre`
- **Client**: `client_id`, `name`
- **Rental**: `rental_id`, `movie_id`, `client_id`, `rented_date`, `due_date`, `returned_date`

Create an application which allows to:
1. Manage clients and movies. The user can add, remove, update, and list both clients and movies.
2. Rent or return a movie. A client can rent a movie until a given date, as long as they have no rented movies that passed their due date for return. A client can return a rented movie at any time.
3. Search for clients or movies using any one of their fields (e.g. movies can be searched for using id, title, description or genre). The search must work using case-insensitive, partial string matching, and must return all matching items.
"""
class Id:
    def __init__(self, id):
        self.id = id

    def id(self):
        return self.id
class Movie(Id):

    def __init__(self, movie_id,title, description, genre):
        super().__init__(movie_id)
        self._title = title
        self._description = description
        self._genre = genre

    @property
    def movie_id(self):
        return self.id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def genre(self):
        return self._genre

    def set_title(self, title):
        self._title = title

    def set_description(self, description):
        self._description = description

    def set_genre(self, genre):
        self._genre = genre

    def __str__(self):
        return "ID: " + str(self.movie_id) + ", Title: " + str(self.title) + ", Description: " + str(self.description) + ", Genre: " + str(self.genre)



class Client(Id):
    def __init__(self, id :int, name: str):
        super().__init__(id)
        self._name = name

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def __str__(self):
        return str(self.id) + " " + str(self.name)

class Rental(Id):
    def __init__(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        super().__init__(rental_id)
        self._movie_id = movie_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    @property
    def rental_id(self):
        return self.rental_id

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def rented_date(self):
        return self._rented_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def returned_date(self):
        return self._returned_date

    def set_movie_id(self, movie_id):
        self._movie_id = movie_id

    def set_client_id(self, client_id):
        self._client_id = client_id

    def set_rented_date(self, rented_date):
        self._rented_date = rented_date

    def set_due_date(self, due_date):
        self._due_date = due_date

    def set_return_date(self,return_date):
        self._returned_date = return_date

    def __str__(self):
        if self.returned_date is None:
            return "Rental with ID: " + str(self.id) + ", movie ID " + str(self.movie_id) +", client ID " + str(self.client_id) + ", rented date " + str(self.rented_date) + ", due date " + str(self.due_date)
        else:
            return "Rental with ID: " + str(self.id) + ", movie ID " + str(self.movie_id) + ", client ID " + str(
                self.client_id) + ", rented date " + str(self.rented_date) + ", due date " + str(self.due_date) + ", return date " + str(self.returned_date)