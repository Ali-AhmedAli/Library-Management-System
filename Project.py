# ================================
# ======== Library System ========
# ================================
import json

class Book:
    def __init__(self, title, author, year, copies):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - Copies: {self.copies}"


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = [] 

    def borrow_book(self, library, title):
        if library.search_member(self.member_id) is None:
            print(f"{self.name} is not a registered member of this library.")
            return

        if title in self.borrowed_books:
            print(f"{self.name} has already borrowed '{title}'.")
            return

        if len(self.borrowed_books) >= 5:
            print(f"{self.name} has reached the borrow limit of 5 books.")
            return

        book = library.search_book(title)
        if book and book.copies > 0:
            self.borrowed_books.append(title)
            library.update_book(title, copies=book.copies - 1)
            print(f"{self.name} borrowed '{title}'.")
        else:
            print(f"'{title}' is not available for borrowing.")

    def return_book(self, library, title):
        if title not in self.borrowed_books:
            print(f"{self.name} does not have '{title}' to return.")
            return

        self.borrowed_books.remove(title)
        current_book = library.search_book(title)
        if current_book is None:
            print(f"'{title}' no longer exists in the library.")
            return

        library.update_book(title, copies=current_book.copies + 1)
        print(f"{self.name} returned '{title}'.")

    def display_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name} has borrowed:")
            for title in self.borrowed_books:
                print(f" - {title}")
        else:
            print(f"{self.name} has not borrowed any books.")
        return list(self.borrowed_books)


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, title, author, year, copies):
        if title in self.books:
            raise ValueError(f"'{title}' already exists. Use update_book instead.")
        self.books[title] = Book(title, author, year, copies)

    def remove_book(self, title):
        if title not in self.books:
            raise KeyError(f"'{title}' not found in the library.")
        del self.books[title]

    def search_book(self, title):
        return self.books.get(title)

    def display_books(self):
        if not self.books:
            print("No books in the library.")
            return []
        for book in self.books.values():
            print(book)
        return list(self.books.values())

    def update_book(self, title, author=None, year=None, copies=None):
        if title not in self.books:
            raise KeyError(f"'{title}' not found in the library.")
        if author is not None:
            self.books[title].author = author
        if year is not None:
            if not isinstance(year, int) or not (1 <= year <= 9999):
                raise ValueError(f"Invalid year '{year}'. Must be an integer between 1 and 9999.")
            self.books[title].year = year
        if copies is not None:
            if copies < 0:
                raise ValueError("Copies cannot be negative.")
            self.books[title].copies = copies

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError(f"Member ID '{member.member_id}' already exists.")
        self.members[member.member_id] = member

    def remove_member(self, member):
        if member.member_id not in self.members:
            raise KeyError(f"Member ID '{member.member_id}' not found.")
        del self.members[member.member_id]

    def search_member(self, member_id):
        return self.members.get(member_id)

    def display_members(self):
        if not self.members:
            print("No members registered.")
            return []
        for member in self.members.values():
            print(f"{member.name} (ID: {member.member_id}) - Borrowed Books: {len(member.borrowed_books)}")
        return list(self.members.values())

    def update_member(self, member, name=None):
        if member.member_id not in self.members:
            raise KeyError(f"Member ID '{member.member_id}' not found.")
        if name is not None:
            self.members[member.member_id].name = name

    def save_to_file(self, filepath):
        data = {
            "books": [
                {
                    "title": b.title,
                    "author": b.author,
                    "year": b.year,
                    "copies": b.copies,
                }
                for b in self.books.values()
            ],
            "members": [
                {
                    "name": m.name,
                    "member_id": m.member_id,
                    "borrowed_books": m.borrowed_books,
                }
                for m in self.members.values()
            ],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Library saved to '{filepath}'.")

    def load_from_file(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        for b in data.get("books", []):
            self.books[b["title"]] = Book(b["title"], b["author"], b["year"], b["copies"])
        for m in data.get("members", []):
            member = Member(m["name"], m["member_id"])
            member.borrowed_books = m["borrowed_books"]
            self.members[m["member_id"]] = member
        print(f"Library loaded from '{filepath}'.")


class Librarian:
    def __init__(self, name):
        self.name = name

    def add_book(self, library, title, author, year, copies):
        library.add_book(title, author, year, copies)
        print(f"{self.name} added '{title}' to the library.")

    def remove_book(self, library, title):
        library.remove_book(title)
        print(f"{self.name} removed '{title}' from the library.")

    def update_book(self, library, title, author=None, year=None, copies=None):
        library.update_book(title, author, year, copies)
        print(f"{self.name} updated '{title}' in the library.")

    def search_book(self, library, title):
        book = library.search_book(title)
        if book:
            print(f"{self.name} found '{title}': {book}")
        else:
            print(f"{self.name} could not find '{title}' in the library.")
        return book

    def display_books(self, library):
        return library.display_books()

    def register_member(self, library, member):
        library.register_member(member)
        print(f"{self.name} registered member '{member.name}' with ID '{member.member_id}'.")

    def remove_member(self, library, member):
        library.remove_member(member)
        print(f"{self.name} removed member '{member.name}' with ID '{member.member_id}' from the library.")

    def update_member(self, library, member, name=None):
        library.update_member(member, name)
        print(f"{self.name} updated member with ID '{member.member_id}'.")

    def display_members(self, library):
        return library.display_members()

    def search_member(self, library, member_id):
        result = library.search_member(member_id)
        if result:
            print(f"{self.name} found '{result.name}' (ID: {result.member_id}).")
        else:
            print(f"{self.name} could not find member with ID '{member_id}'.")
        return result




if __name__ == "__main__":
    # Setup
    library = Library()
    librarian = Librarian("Ali")

    # Add books
    librarian.add_book(library, "Clean Code", "Robert Martin", 2008, 3)
    librarian.add_book(library, "The Pragmatic Programmer", "David Thomas", 1999, 2)
    librarian.add_book(library, "Deep Work", "Cal Newport", 2016, 1)

    # Register members
    ahmed = Member("Ahmed", "M001")
    sara = Member("Sara", "M002")
    librarian.register_member(library, ahmed)
    librarian.register_member(library, sara)

    print("\n--- Library Books ---")
    library.display_books()

    print("\n--- Borrow Books ---")
    ahmed.borrow_book(library, "Clean Code")
    ahmed.borrow_book(library, "Deep Work")
    sara.borrow_book(library, "Clean Code")
    sara.borrow_book(library, "Clean Code") 

    print("\n--- Borrowed Books ---")
    ahmed.display_borrowed_books()
    sara.display_borrowed_books()

    print("\n--- Return a Book ---")
    ahmed.return_book(library, "Clean Code")
    ahmed.display_borrowed_books()

    print("\n--- Library Members ---")
    library.display_members()

    print("\n--- Save & Reload ---")
    library.save_to_file("library.json")
    library2 = Library()
    library2.load_from_file("library.json")
    library2.display_books()
    library2.display_members()