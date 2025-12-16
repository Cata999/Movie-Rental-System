# File: src/repository/file_repository.py (FINAL COMBINED VERSION)

import os
import pickle  # Added pickle import for binary repositories
from datetime import date

from src.domain.domain import Client, Movie, Rental
from src.repository.repository import ClientRepository, MovieRepository, RentalRepository
from src.exceptions.exceptions import RepositoryError


# --- BASE FILE REPOSITORY LOGIC ---
class FileRepositoryBase:

    def _save(self):
        """Abstract method to save in-memory data to file."""
        raise NotImplementedError()

    def add(self, entity):
        super().add(entity)
        self._save()

    def remove(self, entity):
        super().remove(entity)
        self._save()

    def set_all(self, data_list):
        super().set_all(data_list)
        self._save()


# --- TEXT FILE REPOSITORIES ---

class FileClientRepository(FileRepositoryBase, ClientRepository):
    def __init__(self, filename):
        ClientRepository.__init__(self)
        self._filename = filename
        self._load()

    def _load(self):
        self._clients = []
        if not os.path.exists(self._filename):
            return
        with open(self._filename, 'r') as f:
            for line in f:
                try:
                    line = line.strip()
                    if not line: continue
                    # 1. Try to read comma-separated
                    parts = line.split(',', 1)
                    if len(parts) != 2:
                        # 2. If comma fails, try space-separated
                        parts = line.split(' ', 1)
                        if len(parts) != 2: continue

                    client_id, name = parts
                    self._clients.append(Client(int(client_id), name.strip()))
                except ValueError:
                    continue

    def _save(self):
        with open(self._filename, 'w') as f:
            for client in self._clients:
                f.write(f"{client.id},{client.name}\n")


class FileMovieRepository(FileRepositoryBase, MovieRepository):
    def __init__(self, filename):
        MovieRepository.__init__(self)
        self._filename = filename
        self._load()

    def _load(self):
        self._movies = []
        if not os.path.exists(self._filename):
            return
        with open(self._filename, 'r') as f:
            for line in f:
                try:
                    line = line.strip()
                    if not line: continue
                    parts = line.split(',', 3)
                    if len(parts) != 4: continue
                    movie_id, title, description, genre = parts
                    self._movies.append(Movie(int(movie_id), title.strip(), description.strip(), genre.strip()))
                except ValueError:
                    continue

    def _save(self):
        with open(self._filename, "w") as f:
            for e in self._movies:
                f.write(f"{e.id},{e.title},{e.description},{e.genre}\n")


class FileRentalRepository(FileRepositoryBase, RentalRepository):
    def __init__(self, filename):
        RentalRepository.__init__(self)
        self._filename = filename
        self._load()

    def _load(self):
        self._rentals = []
        if not os.path.exists(self._filename):
            return
        with open(self._filename, 'r') as f:
            for line in f:
                try:
                    parts = line.strip().split(',')
                    if len(parts) != 6: continue
                    rental_id, movie_id, client_id, rented_date_str, due_date_str, return_date_str = parts
                    rented_date = date.fromisoformat(rented_date_str)
                    due_date = date.fromisoformat(due_date_str)
                    returned_date = None
                    if return_date_str.lower() != 'none':
                        returned_date = date.fromisoformat(return_date_str)
                    self._rentals.append(
                        Rental(int(rental_id), int(movie_id), int(client_id), rented_date, due_date, returned_date))
                except (ValueError, TypeError):
                    continue

    def _save(self):
        with open(self._filename, "w") as f:
            for e in self._rentals:
                return_date_str = str(e.returned_date.isoformat()) if e.returned_date else 'None'
                f.write(
                    f"{e.id},{e.movie_id},{e.client_id},{e.rented_date.isoformat()},{e.due_date.isoformat()},{return_date_str}\n")

            # --- BINARY FILE REPOSITORIES (Pickle) ---


class BinaryFileRepository(FileRepositoryBase):
    """Base class for Pickle-based repositories."""

    def __init__(self, file_path):
        self._filename = file_path
        self._load()

    def _load(self):
        try:
            with open(self._filename, 'rb') as f:
                self._data = pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # Handle corrupted or empty files gracefully
            self._data = []

    def _save(self):
        with open(self._filename, 'wb') as f:
            # This is the line that triggered the type hint warning,
            # but it is functionally correct Python code.
            pickle.dump(self._data, f)


class BinaryClientRepository(BinaryFileRepository, ClientRepository):
    def __init__(self, file_path):
        ClientRepository.__init__(self)
        BinaryFileRepository.__init__(self, file_path)
        self._clients = self._data


class BinaryMovieRepository(BinaryFileRepository, MovieRepository):
    def __init__(self, file_path):
        MovieRepository.__init__(self)
        BinaryFileRepository.__init__(self, file_path)
        self._movies = self._data


class BinaryRentalRepository(BinaryFileRepository, RentalRepository):
    def __init__(self, file_path):
        RentalRepository.__init__(self)
        BinaryFileRepository.__init__(self, file_path)
        self._rentals = self._data