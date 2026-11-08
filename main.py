from Library import Library

def show_menu():
    print("""
====== Library Management ======
1. Add Book
2. View Books
3. Search Book
4. Update Book
5. Delete Book
6. Add Member
7. Borrow Book
8. Return Book
9.  Currently Borrowed Books
0. Exit
""")

def main():
    library = Library()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("--Add Book--")
            title = input("Enter Book Title: ").strip()
            author = input("Enter Book Author: ").strip()
            quantity = input("Enter Quantity: ").strip()

            book = library.add_book(title, author, quantity)

            if book is not None:
                print("Book added successfully!")

        elif choice == "2":
            library.view_book()

        elif choice == "3":
            print("--Search Book--")
            search_text = input("Enter book title or author: ")
            library.search_book(search_text)

        elif choice == "4":
            print("--Update Book--")
            book_id = input("Enter Book ID to update: ")
            library.update_book(book_id)

        elif choice == "5":
            print("--Delete Book--")
            book_id = input("Enter Book ID to delete: ")
            library.delete_book(book_id)

        elif choice == "6":
            print("--Add Member--")
            name = input("Enter Member Name: ").strip()

            library.add_member(name)

        elif choice == "7":
            print("--Borrow book--")
            member_id = input("Enter Member ID: ")
            book_id = input("Enter Book ID: ")

            library.borrow_book(member_id, book_id)

        elif choice == "8":
            print("--Return Book--")
            member_id = input("Enter Member ID: ")
            book_id = input("Enter Book ID: ")

            library.return_book(member_id, book_id)

        elif choice == "9":
            print("-- Currently Borrowed Books --")
            library.view_borrowed_books()


        elif choice == "0":
            print("Goodbye")
            exit()

if __name__ == "__main__":
    main()