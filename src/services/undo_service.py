# File: src/undo_redo/undo_redo.py

from src.exceptions.exceptions import MovieRentalException, ClientError, MovieError, RentalError


class UndoRedoError(MovieRentalException):
    """Raised when there are no more undo or redo operations available."""
    pass


class FunctionCall:
    def __init__(self, func_name, *func_parameters):
        self._func_name = func_name
        self._func_parameters = func_parameters

    def call(self):
        """Executes the stored function with its parameters."""
        self._func_name(*self._func_parameters)

    # Note: __call__ is commented out as requested in the template
    # def __call__(self, *args, **kwargs):
    #     self.call()


class Operation:
    def __init__(self, undo_function: FunctionCall, redo_function: FunctionCall):
        self.__undo = undo_function
        self.__redo = redo_function

    def undo(self):
        self.__undo.call()

    def redo(self):
        self.__redo.call()


class UndoService:
    """
    Keeps a history of all undoable/redoable operations.
    """

    def __init__(self):
        self.__history = []
        self.__index = 0

    def add_operation(self, operation: Operation):
        """
        Adds a new operation to the history, invalidating all future redos.
        """
        # Invalidate all redos
        self.__history = self.__history[:self.__index]
        self.__history.append(operation)
        self.__index = len(self.__history)

    def undo(self):
        """
        Performs the undo action of the current operation and moves the index back.
        """
        if self.__index == 0:
            raise UndoRedoError("No more undo operations.")

        self.__index -= 1
        oper = self.__history[self.__index]
        oper.undo()

    def redo(self):
        """
        Performs the redo action of the next operation and moves the index forward.
        """
        if self.__index == len(self.__history):
            raise UndoRedoError("No more redo operations.")

        oper = self.__history[self.__index]
        oper.redo()
        self.__index += 1