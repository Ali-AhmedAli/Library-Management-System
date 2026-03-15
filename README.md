# 📚 Library Management System

A simple, object-oriented Python library management system that supports book inventory, member registration, borrowing/returning workflows, and JSON-based persistence.

---

## Features

- **Book Management** — Add, remove, update, and search books in the library inventory
- **Member Management** — Register, update, and remove library members
- **Borrow & Return** — Members can borrow up to 5 books at a time and return them when done
- **Librarian Role** — A dedicated `Librarian` class acts as an admin interface for all management operations
- **Data Persistence** — Save and load the entire library state to/from a JSON file

---

## Project Structure

```
library_system/
│
├── library.py        # Main source file containing all classes
└── library.json      # Auto-generated save file (created at runtime)
```

---

## Classes Overview

### `Book`
Represents a book in the library.

| Attribute | Type  | Description                    |
|-----------|-------|--------------------------------|
| `title`   | `str` | Title of the book              |
| `author`  | `str` | Author's name                  |
| `year`    | `int` | Publication year               |
| `copies`  | `int` | Number of available copies     |

---

### `Member`
Represents a library member who can borrow and return books.

| Attribute        | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `name`           | `str`  | Member's full name                   |
| `member_id`      | `str`  | Unique member identifier             |
| `borrowed_books` | `list` | List of currently borrowed book titles |

**Methods:**

| Method | Description |
|--------|-------------|
| `borrow_book(library, title)` | Borrow a book from the library (max 5 at a time) |
| `return_book(library, title)` | Return a previously borrowed book |
| `display_borrowed_books()` | Print and return the list of borrowed books |

---

### `Library`
The core class managing books and members.

**Methods:**

| Method | Description |
|--------|-------------|
| `add_book(title, author, year, copies)` | Add a new book to the inventory |
| `remove_book(title)` | Remove a book by title |
| `search_book(title)` | Find and return a book by title |
| `update_book(title, ...)` | Update book attributes (author, year, copies) |
| `display_books()` | Print all books in the library |
| `register_member(member)` | Register a new member |
| `remove_member(member)` | Remove a member from the system |
| `search_member(member_id)` | Find a member by their ID |
| `update_member(member, name)` | Update a member's name |
| `display_members()` | Print all registered members |
| `save_to_file(filepath)` | Persist library state to a JSON file |
| `load_from_file(filepath)` | Load library state from a JSON file |

---

### `Librarian`
An admin wrapper around `Library` that logs every action performed.

| Method | Description |
|--------|-------------|
| `add_book(library, ...)` | Add a book with a confirmation message |
| `remove_book(library, title)` | Remove a book with a confirmation message |
| `update_book(library, title, ...)` | Update a book with a confirmation message |
| `search_book(library, title)` | Search and display a book result |
| `register_member(library, member)` | Register a member with a confirmation message |
| `remove_member(library, member)` | Remove a member with a confirmation message |
| `update_member(library, member, ...)` | Update a member with a confirmation message |
| `search_member(library, member_id)` | Search and display a member result |
| `display_books(library)` | Display all books |
| `display_members(library)` | Display all members |

---

## Getting Started

### Prerequisites
- Python 3.7+
- No external dependencies required

### Installation

```bash
git clone https://github.com/your-username/library-system.git
cd library-system
```

### Run

```bash
python library.py
```

---

## Usage Example

```python
from library import Library, Librarian, Member

# Initialize
library = Library()
librarian = Librarian("Ali")

# Add books
librarian.add_book(library, "Clean Code", "Robert Martin", 2008, 3)
librarian.add_book(library, "Deep Work", "Cal Newport", 2016, 1)

# Register members
ahmed = Member("Ahmed", "M001")
librarian.register_member(library, ahmed)

# Borrow and return
ahmed.borrow_book(library, "Clean Code")
ahmed.display_borrowed_books()
ahmed.return_book(library, "Clean Code")

# Persist state
library.save_to_file("library.json")

# Reload state
library2 = Library()
library2.load_from_file("library.json")
```

---

## Borrow Rules

- A member can borrow a **maximum of 5 books** at a time.
- A member **cannot borrow the same book twice** simultaneously.
- A book can only be borrowed if **at least 1 copy is available**.
- Only **registered members** can borrow books.

---

## Data Persistence Format

Library state is saved as a structured JSON file:

```json
{
    "books": [
        {
            "title": "Clean Code",
            "author": "Robert Martin",
            "year": 2008,
            "copies": 2
        }
    ],
    "members": [
        {
            "name": "Ahmed",
            "member_id": "M001",
            "borrowed_books": ["Clean Code"]
        }
    ]
}
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).