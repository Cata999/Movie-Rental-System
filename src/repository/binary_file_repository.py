# File: src/repository/binary_repository.py (NEW FILE)

import os
import pickle
from src.repository.repository import ClientRepository, MovieRepository, RentalRepository
# Import the base class that defines add/remove logic for persistence
from src.repository.file_repository import FileRepositoryBase

class BinaryFileRepository(FileRepositoryBase):
    """
    Base class for all binary (Pickle) repositories.
    It overrides the abstract _load and _save methods to use the pickle library.
    It relies on FileRepositoryBase to trigger _save on add/remove/set_all.
    """
    def __init__(self, file_path):
        # We store the file path and explicitly call _load,
        # but defer domain list initialization to the concrete repository.
        self._filename = file_path
        self._load()

    def _load(self):
        """Loads data from the binary file using pickle."""
        try:
            with open(self._filename, 'rb') as f:
                # The data structure (list of entities) is loaded into self._data
                self._data = pickle.load(f)
        except FileNotFoundError:
            self._data = []
        except EOFError:
            self._data = [] # Handle empty file

    def _save(self):
        """Saves the entire in-memory list to the binary file using pickle."""
        with open(self._filename, 'wb') as f:
            # Dump the entire in-memory list to the file
            pickle.dump(self._data, f)


class BinaryClientRepository(BinaryFileRepository, ClientRepository):
    def __init__(self, file_path):
        ClientRepository.__init__(self) # Initialize ClientRepository's list
        BinaryFileRepository.__init__(self, file_path) # Initialize BinaryFileRepository (calls _load which populates self._data)
        self._clients = self._data # Link the loaded data to the ClientRepository's internal list

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