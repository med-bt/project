class Book():
    def __init__(self,ISBN,title,author):
        self.ISBN = ISBN
        self.title = title
        self.author = author

book1 = Book("123-456-789","python programming","JOHN DOE")
book2 = Book("789-123-456","data science basics","JAMES SMITH")
book3 = Book("456-789-123","web with django","ALICE JONSON")

class Librray():
    def __init__(self):
        self.books = []
        self.students = []
    def add_book(self,book):
        self.books.append(book)
    def rm_book(self,book):
        self.books.remove(book)
    def display_books(self):
        for book in self.books:
            print(book.title)
    def show_borrowed(self,student):
        if student not in self.students:
            print("student not exists")
        else:
            for book in student.b_books:
                print(book.title)
            

library = Librray()

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

class Student():
    def __init__(self,CNE,name,email):
        self.CNE = CNE
        self.name= name
        self.email=email
        self.b_books = []
    def borrow_book(self,book):
        if book in library.books and self not in library.students:
            self.b_books.append(book)
            library.rm_book(book)
            library.students.append(self)
        else:
            print("book or student not exists ")
    def return_book(self,book):
        self.b_books.remove(book)
        library.add_book(book)
        library.students.remove(self)


adam = Student(34567,"adam","adam@test.com")
taha = Student(87654,"taha","taha@domain.com")
adam.borrow_book(book1)
taha.borrow_book(book3)

print(library.show_borrowed(taha))

