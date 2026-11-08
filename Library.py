from database import get_connection
class Library:

    def validate_text(self, value, field_name):

        value = value.strip()

        if not value:
            print(f"{field_name} cannot be empty.")
            return None

        return value

    def validate_id(self, value, field_name):

        value = str(value).strip()

        if not value.isdigit():
            print(f"Invalid {field_name}.")
            return None

        return value

    def validate_quantity(self, value):

        value = str(value).strip()

        if not value.isdigit():
            print("Invalid quantity.")
            return None

        return int(value)

    def display_books(self, books):

        for book in books:
            print("Book ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("Quantity:", book[3])
            print("-------------------------")

    def get_book(self, cursor, book_id):

        cursor.execute(
            "SELECT * FROM books WHERE book_id = %s",
            (book_id,)
        )

        return cursor.fetchone()

    def check_records(self, records, message):

        if not records:
            print(message)
            return False

        return True

    def add_book(self, title, author, quantity):

        title = self.validate_text(title, "Title")
        if title is None:
            return

        author = self.validate_text(author, "Author")
        if author is None:
            return

        quantity = self.validate_quantity(quantity)
        if quantity is None:
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO books (title, author, quantity)
                    VALUES (%s, %s, %s)
                    """,
                    (title.strip(), author.strip(), quantity)
                )

        print("Book added successfully!")
    def view_book(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute("SELECT * FROM books")

                books = cursor.fetchall()

                if not self.check_records(books, "No books found."):
                    return
                self.display_books(books)

    def search_book(self, search_text):

            search_text = self.validate_text(search_text, "Search")
            if search_text is None:
                return

            search_text = "%" + search_text + "%"

            with get_connection() as conn:
                with conn.cursor() as cursor:

                    cursor.execute("""
                                   SELECT *
                                   FROM books
                                   WHERE title ILIKE %s OR author ILIKE %s
                                   """, (search_text, search_text))

                    books = cursor.fetchall()

                    if not self.check_records(books, "No books found."):
                        return

                    self.display_books(books)

    def update_book(self, book_id):

        book_id = self.validate_id(book_id, "Book ID")
        if book_id is None:
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                book = self.get_book(cursor, book_id)

                if not book:
                    print("Book not found.")
                    return

                title = input("Enter new title: ").strip()
                author = input("Enter new author: ").strip()
                quantity = input("Enter new quantity: ").strip()

                title = self.validate_text(title, "Title")
                if title is None:
                    return

                author = self.validate_text(author, "Author")
                if author is None:
                    return

                quantity = self.validate_quantity(quantity)
                if quantity is None:
                    return

                cursor.execute("""
                               UPDATE books
                               SET title    = %s,
                                   author   = %s,
                                   quantity = %s
                               WHERE book_id = %s
                               """, (title, author, quantity, book_id))

                print("Book updated successfully!")

    def delete_book(self,book_id):

        book_id = self.validate_id(book_id, "Book ID")
        if book_id is None:
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                book = self.get_book(cursor, book_id)

                if not book:
                    print("Book not found.")
                    return

                cursor.execute(
                    "DELETE FROM books WHERE book_id = %s",
                    (book_id,)
                )

        print("Book deleted successfully!")

    def add_member(self, name):

        name = self.validate_text(name, "Name")
        if name is None:
            return

        if not any(char.isalpha() for char in name):
            print("Name must contain letters.")
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                               INSERT INTO Members (name)
                               VALUES (%s) 
                               RETURNING member_id
                               """, (name,))
                member_id = cursor.fetchone()[0]

        print("Member added successfully!")
        print(f"Member ID: {member_id}")
        print(f"Member Name: {name}")

    def borrow_book(self, member_id, book_id):

        member_id = self.validate_id(member_id, "Member ID")
        if member_id is None:
            return

        book_id = self.validate_id(book_id, "Book ID")
        if book_id is None:
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Members WHERE member_id = %s",
                    (member_id,)
                )
                member = cursor.fetchone()

                if not member:
                    print("Member not found.")
                    return

                book = self.get_book(cursor, book_id)

                if not book:
                    print("Book not found.")
                    return

                quantity = book[3]

                if quantity <= 0:
                    print("Book is not available.")
                    return

                cursor.execute("""
                               UPDATE Books
                               SET quantity = quantity - 1
                               WHERE book_id = %s
                               """, (book_id,))

                cursor.execute("""
                               INSERT INTO Borrowings (member_id, book_id, borrow_date)
                               VALUES (%s, %s, CURRENT_DATE)
                               """, (member_id, book_id))

        print("Book borrowed successfully!")

    def return_book(self, member_id, book_id):

        member_id = self.validate_id(member_id, "Member ID")
        if member_id is None:
            return

        book_id = self.validate_id(book_id, "Book ID")
        if book_id is None:
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM Borrowings
                    WHERE member_id = %s
                      AND book_id = %s
                      AND return_date IS NULL
                    """,
                    (member_id, book_id)
                )
                borrowing = cursor.fetchone()

                if not borrowing:
                    print("No active borrowing found.")
                    return
                borrow_id = borrowing[0]
                cursor.execute(
                    """
                    UPDATE Borrowings
                    set return_date = CURRENT_DATE
                    where borrow_id = %s
                    """,
                    (borrow_id,)
                )
                cursor.execute("""
                    UPDATE Books
                    set quantity = quantity + 1
                    where  book_id = %s
                    """,
                    (book_id,)
                )
        print("Book returned successfully!")


    def view_borrowed_books(self):

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT
                Members.name,
                Books.title,
                Borrowings.borrow_date
                FROM Borrowings
                JOIN Members    
                ON Members.member_id = Borrowings.member_id
                JOIN Books
                ON Books.book_id = Borrowings.book_id 
                WHERE Borrowings.return_date IS NULL;    
                """
                )
                borrowings = cursor.fetchall()

                if not borrowings:
                    print("No borrowed books found.")
                    return
                for borrowing in borrowings:
                    print("Member Name:", borrowing[0])
                    print("Book Title:", borrowing[1])
                    print("Borrow Date:", borrowing[2])
                    print("----------------------")


