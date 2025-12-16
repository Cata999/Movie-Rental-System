

# 1. Base Application Exception
class MovieRentalException(Exception):
    """Base class for all custom exceptions in the Movie Rental application."""
    pass

# 2. Domain-Specific Exceptions
class RepositoryError(MovieRentalException):
    """Raised for errors during data access (e.g., ID not found)."""
    pass

class ClientError(MovieRentalException):
    """Raised for Client-related business logic errors (e.g., invalid name)."""
    pass

class MovieError(MovieRentalException):
    """Raised for Movie-related business logic errors (e.g., movie already exists)."""
    pass

class RentalError(MovieRentalException):
    """Raised for Rental-related errors (e.g., movie is currently rented)."""
    pass

class UndoRedoError(MovieRentalException):
    """Raised when there are no more undo or redo operations available."""
    pass