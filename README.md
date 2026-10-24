# 🎬 Movie Rental Management System

A Python application built using **Layered Architecture** and Object-Oriented Design Principles for managing movie rentals, clients, and catalog inventory. The system features flexible data persistence (In-Memory, Text Files, Binary Pickle), advanced query statistics, and an unlimited Undo/Redo engine utilizing the **Command Design Pattern**.

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Architecture & Design](#-architecture--design)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [Running Unit Tests](#-running-unit-tests)
- [Design Patterns & Principles](#-design-patterns--principles)

---

## 🌟 Project Overview

The **Movie Rental Management System** enables video rental store staff to manage clients, catalog movies, and track active and past movie rentals. It enforces business rules (such as rental deadlines, restrictions on clients with overdue returns, and movie availability checks), provides advanced search and reporting statistics, and supports full transaction reversibility through undo/redo operations.

---

## 🏛 Architecture & Design

The application follows a clean, decoupled **Layered Architecture** consisting of four distinct layers:

```
+---------------------------------------------------------+
|                      UI Layer                           |
|       (src/ui/ui.py - Console Menu System)              |
+---------------------------------------------------------+
                           |
                           v
+---------------------------------------------------------+
|                   Services Layer                        |
|  (Business logic, validation, statistics, undo/redo)    |
+---------------------------------------------------------+
                           |
                           v
+---------------------------------------------------------+
|                  Repository Layer                       |
|   (In-Memory, Plain Text File, Binary Pickle Storage)   |
+---------------------------------------------------------+
                           |
                           v
+---------------------------------------------------------+
|                    Domain Layer                         |
|     (Core entities: Movie, Client, Rental, Id)          |
+---------------------------------------------------------+
```

1. **Domain Layer (`src.domain`)**:
   - Represents the core business models (`Movie`, `Client`, `Rental`, `Id`).
   - Encapsulates entity properties, setters, and string representations.

2. **Repository Layer (`src.repository`)**:
   - Abstract and concrete data repositories managing collections of entities.
   - Provides polymorphism through three interchangeable storage strategies:
     - **In-Memory**: Transient storage in Python lists.
     - **Text Files**: Persisted to delimited text files (`clients.txt`, `movies.txt`, `rentals.txt`).
     - **Binary Files**: Serialized to disk using Python's `pickle` module (`clients.pickle`, `movies.pickle`, `rentals.pickle`).

3. **Services Layer (`src.services`)**:
   - Contains business logic, validation rules, cross-entity constraints, and report generation.
   - Coordinates with `UndoService` to record reversible actions as commands.

4. **UI Layer (`src.ui`)**:
   - Text-based interactive command-line interface.
   - Automatically initializes demo data with `Faker` if repositories are empty for testing and exploration.

5. **Configuration & Cross-Cutting**:
   - `src.settings`: Parses `settings.properties` dynamically to configure repository strategies and file paths.
   - `src.exceptions`: Explicit custom exception hierarchy (`MovieRentalException`, `ClientError`, `MovieError`, `RentalError`, `UndoRedoError`, `RepositoryError`).

---

## ✨ Key Features

### 1. 👥 Client Management
- **Add Client**: Create new client records with a unique ID and name.
- **Update Client**: Modify client details (name) with validation.
- **Remove Client**: Delete clients (cascading actions recorded for undo/redo).
- **List Clients**: Display all registered clients.

### 2. 🎞️ Movie Catalog Management
- **Add Movie**: Register new movies with unique ID, title, description, and genre.
- **Update Movie**: Independently update title, description, or genre.
- **Remove Movie**: Remove a movie from inventory.
- **List Movies**: View all cataloged movies.

### 3. 📅 Rental Management
- **Rent Movie**:
  - Validates that both client and movie exist.
  - Ensures the movie is not currently rented by another customer.
  - **Overdue Check**: Prevents clients with overdue rentals from renting additional movies.
  - Automatically calculates standard 14-day rental due dates.
- **Return Movie**:
  - Records the exact return date and closes the active rental status.
- **List Rentals**: View both active and completed rentals with full timeline details.

### 4. 🔍 Partial & Case-Insensitive Search
- **Search Clients**: Locate clients by matching any substring in their ID or name (case-insensitive).
- **Search Movies**: Search across all movie fields (ID, title, description, or genre).

### 5. 📊 Statistics & Reports
- **Most Rented Movies**:
  - Lists movies sorted in descending order of the total number of days they have been rented.
- **Most Active Clients**:
  - Lists clients sorted in descending order of cumulative movie rental days.
- **Late Rentals**:
  - Highlights all currently overdue rentals, sorted in descending order of days overdue, detailing movie title, client name, and due date.

### 6. 🔄 Unlimited Undo / Redo
- Built using the **Command Design Pattern**.
- Every state-modifying action (`add`, `remove`, `update`, `rent`, `return`) registers reversible function calls (`undo` and `redo`).
- Supports infinite traversal across operations with history invalidation upon branching new changes.

---

## 📁 Project Structure

```
.
├── README.md                          # Project documentation
├── settings.properties                # Application configuration file
└── src
    ├── domain                         # Domain entities
    │   ├── __init__.py
    │   └── domain.py                  # Id, Movie, Client, Rental definitions
    ├── exceptions                     # Custom exception classes
    │   ├── __init__.py
    │   └── exceptions.py              # Domain and application exceptions
    ├── repository                     # Data access layer
    │   ├── __init__.py
    │   ├── repository.py              # In-memory repositories
    │   ├── file_repository.py         # Text file repositories
    │   └── binary_file_repository.py  # Binary (pickle) repositories
    ├── services                       # Application business logic
    │   ├── __init__.py
    │   ├── services.py                # Client, Movie, and Rental services
    │   └── undo_service.py            # Command pattern Undo/Redo engine
    ├── settings                       # Configuration parser
    │   ├── __init__.py
    │   └── settings.py                # Settings parser based on configparser
    ├── test                           # Test suite
    │   ├── __init__.py
    │   └── test_objects.py            # Unit tests for entities, repositories, and services
    └── ui                             # Presentation layer
        ├── __init__.py
        └── ui.py                      # Console interface and entry point
```

---

## ⚙️ Configuration

The repository persistence mechanism is configured via `settings.properties` in the project root:

```ini
[RepositorySettings]
# Persistence options: 'inmemory', 'textfiles', 'binaryfiles'
repository=inmemory

# File paths for text file persistence:
#repository=textfiles
#clients=src/ui/clients.txt
#movies=src/ui/movies.txt
#rentals=src/ui/rentals.txt

# File paths for binary file persistence:
#repository=binaryfiles
#clients=src/ui/clients.pickle
#movies=src/ui/movies.pickle
#rentals=src/ui/rentals.pickle
```

Switching repository modes requires only changing the `repository` value and specifying paths.

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.10+**
- Git

### Setup Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd a10-Cata999S
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install faker
   ```

---

## 💻 How to Run

Launch the application by running the UI module from the project root:

```bash
python -m src.ui.ui
```
*(On Windows systems where `python` is aliased, you can also run `py -m src.ui.ui`)*

### Console Menu Navigation
Upon starting, the application displays the main menu:
```text
~~~~~~~~Menu~~~~~~~
1. Manage clients
2. Manage movies
3. Manage rentals
4. Search for clients or movies
5. Undo/Redo
6. Show statistics
0. Exit
```

---

## 🧪 Running Unit Tests

Run the unit test suite using Python's built-in `unittest` runner from the project root:

```bash
python -m unittest discover -s src -p "test_*.py"
```

The test suite validates:
- Entity creation and property access.
- CRUD repository operations.
- Business rules (movie updating, rental creation, returns, and validations).

---

## 🧠 Design Patterns & Principles

- **Layered Architecture**: Strict boundaries between UI, business services, data storage, and domain objects.
- **Command Pattern**: Encapsulates undo and redo actions into executable `FunctionCall` and `Operation` objects.
- **Repository Pattern**: Abstracts storage specifics, allowing in-memory, text, and binary formats behind uniform interfaces.
- **Single Responsibility Principle (SRP)**: Each class is tailored to a single role (e.g., data modeling, persistence, or validation).
- **Dependency Injection**: Services receive repositories and the undo manager via constructor parameters, facilitating unit testing and modularity.
