from  unittest import TestCase
from datetime import date
from src.domain.domain import *
from src.repository.repository import RentalRepository, MovieRepository, ClientRepository
from src.services.services import *

class TestMovie(TestCase):

    def setUp(self):
        """Initializes a fresh repository and service for each test."""
        self.repo = MovieRepository()
        self.service = MovieServices(self.repo)

        # Add a test movie with ID 1 for update operations
        self.initial_movie = Movie(1, "Old Title", "Old Description", "Old Genre")
        self.repo.add(self.initial_movie)
    def test_movie(self):
        movie = Movie(1,"Fight Club", "Interesting", "Action")
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.title, "Fight Club")
        self.assertEqual(movie.description, "Interesting")
        self.assertEqual(movie.genre, "Action")

    def test_add_movie(self):

        self.repo.add(self.initial_movie)
        self.assertEqual(self.repo.get_all()[1], self.initial_movie)

    def test_remove_movie(self):
        self.repo.remove(self.initial_movie)
        self.assertEqual(len(self.repo.get_all()), 0)

    def test_update_movie_title_success(self):
        """Tests successful update of movie title for an existing movie."""
        new_title = "The New Movie Title"
        self.service.update_movie_title(1, new_title)

        # Retrieve the updated movie from the repository
        updated_movie = self.repo.find(1)

        # Assert that the title was changed
        self.assertEqual(updated_movie.title, new_title)
        # Assert that other fields are unchanged
        self.assertEqual(updated_movie.description, "Old Description")

    def test_update_movie_description_success(self):
        """Tests successful update of movie description."""
        new_description = "A gripping story about something new"
        self.service.update_movie_description(1, new_description)

        updated_movie = self.repo.find(1)
        self.assertEqual(updated_movie.description, new_description)
        self.assertEqual(updated_movie.title, "Old Title")

    def test_update_movie_genre_success(self):
        """Tests successful update of movie genre."""
        new_genre = "Sci-Fi Action"
        self.service.update_movie_genre(1, new_genre)

        updated_movie = self.repo.find(1)
        self.assertEqual(updated_movie.genre, new_genre)
        self.assertEqual(updated_movie.description, "Old Description")


class TestClient(TestCase):

    def setUp(self):

        self.client_repo = ClientRepository()
        self.service = ClientServices(self.client_repo)

        self.initial_client = Client(1,"John Pork")
        self.client_repo.add(self.initial_client)

    def test_client(self):
        client = Client(2, "John Pork")
        self.assertEqual(client.id, 2)
        self.assertEqual(client.name, "John Pork")

    def test_add_client(self):
        self.client_repo.add(self.initial_client)
        self.assertEqual(self.client_repo.get_all()[1], self.initial_client)


    def test_remove_client(self):
        self.client_repo.remove(self.initial_client)
        self.assertEqual(len(self.client_repo.get_all()), 0)

    def test_update_client_name(self):
        new_name = "John Cena"
        self.service.update_client_name(1, new_name)
        self.assertEqual(self.client_repo.get_all()[0].name, new_name)


class TestRentalLogic(TestCase):

    def setUp(self):
        """Initializes fresh repositories, services, and base data for each test."""
        # Repositories
        self.rental_repo = RentalRepository()
        self.client_repo = ClientRepository()
        self.movie_repo = MovieRepository()

        # Services (Client and Movie services are dependencies for RentalServices)
        self.client_service = ClientServices(self.client_repo)
        self.movie_service = MovieServices(self.movie_repo)
        self.rental_service = RentalServices(self.rental_repo, self.client_repo, self.movie_repo)

        # Base Data (A client and movie must exist for successful rentals)
        self.client_id = 101
        self.movie_id = 201
        self.client_repo.add(Client(self.client_id, "Test Client"))
        self.movie_repo.add(Movie(self.movie_id, "Test Movie", "Desc", "Action"))

        # Fixed dates for consistent testing
        self.fixed_rented_date = date(2025, 12, 1)
        self.fixed_due_date = date(2025, 12, 15)
        self.future_date = date(2026, 1, 1)

    # -----------------------------------------------------------
    # Test Rent Movie Functionality (rent_movie)
    # -----------------------------------------------------------

    def test_rent_movie_success(self):
        """Tests successful creation of a new rental record."""
        rental_id = 1
        self.rental_service.rent_movie(
            rental_id, self.movie_id, self.client_id,
            self.fixed_rented_date, self.fixed_due_date, None
        )

        # Assert that the rental was added and its status is active
        rental = self.rental_repo.find(rental_id)
        self.assertIsNotNone(rental)
        self.assertIsNone(rental.returned_date)


    # -----------------------------------------------------------
    # Test Return Movie Functionality (return_movie)
    # -----------------------------------------------------------

    def test_return_movie_success(self):
        """Tests successful setting of the returned_date on an active rental."""
        rental_id = 3
        # Setup: An active rental
        self.rental_repo.add(
            Rental(rental_id, self.movie_id, self.client_id, self.fixed_rented_date, self.fixed_due_date, None))

        new_return_date = date(2025, 12, 10)
        self.rental_service.return_movie(rental_id, new_return_date)

        # Assert the returned_date was updated
        updated_rental = self.rental_repo.find(rental_id)
        self.assertEqual(updated_rental.returned_date, new_return_date)
