import os
import mysql.connector
import datetime
from datetime import date, timedelta


# classes


class ViewOrder:
    def __init__(self, orderID, staffID, staffFName, staffLName, memberID, memberFName, memberLName, bookIsbn, bookTitle, bookAuthor, rentDate, dueDate, status, returnDate):
        self.orderID = orderID
        self.staffID = staffID
        self.staffFName = staffFName
        self.staffLName = staffLName
        self.memberID = memberID
        self.memberFName = memberFName
        self.memberLName = memberLName
        self.bookIsbn = bookIsbn
        self.bookTitle = bookTitle
        self.bookAuthor = bookAuthor
        self.rentDate = rentDate
        self.dueDate = dueDate
        self.status = status
        self.returnDate = returnDate


class PersonInfo:
    def __init__(self, ID, fName, lName, email, password, status):
        self.ID = ID
        self.fName = fName
        self.lName = lName
        self.email = email
        self.password = password
        self.status = status


class Book:
    def __init__(self, isbn, title, author, publisher, availability, shelf):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.availability = availability
        self.shelf = shelf


class Order:
    def _init_(self, orderID, staffID, memberID, isbn, rentDate, dueDate, status, returnDate):
        self.orderID = orderID
        self.staffID = staffID
        self.memberID = memberID
        self.isbn = isbn
        self.rentDate = rentDate
        self.dueDate = dueDate
        self.status = status
        self.returDate = returnDate

################################################################
# Function
################################################################
# Database Function


def connect_to_database():  # Return VOID
    global db
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3020",
        database="librarydatabase"
    )

    # Create a cursor object to execute SQL queries
    global dbcursor
    dbcursor = db.cursor()


def update_to_MySQL(sql):
    # Execute the SQL
    dbcursor.execute(sql)
    db.commit()


def fetchone_from_MySQL(sql):
    # Execute the SQL
    dbcursor.execute(sql)

    # Return Fetchall result from SQL
    return dbcursor.fetchone()


def search_using_keywords_MySQL(inputString, attribute, table):
    # Extract keywords
    keywords = inputString.split(" ")

    # Build SQL to search
    sql = f"SELECT * FROM {table} WHERE "
    for i in range(len(keywords)):
        if i == 0:
            sql += f"{attribute} LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR {attribute} LIKE '%" + keywords[i] + "%'"

    # Execute the SQL
    dbcursor.execute(sql)

    # Return Fetchall result from SQL
    return dbcursor.fetchall()


def search_using_exact_keywords_MySQL(inputString, attribute, table):
    # Build SQL to search
    sql = f"SELECT * FROM {table} WHERE {attribute} =  '{inputString}' "

    # Execute the SQL
    dbcursor.execute(sql)

    # Return Fetchall result from SQL
    return dbcursor.fetchone()


def search_using_keywords_MySQL_selective_attribute(inputString, attribute, table, atributesToShow):
    # Extract keywords
    keywords = inputString.split(" ")

    # Build SQL to search
    sql = f"SELECT {atributesToShow} FROM {table} WHERE "
    for i in range(len(keywords)):
        if i == 0:
            sql += f"{attribute} LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR {attribute} LIKE '%" + keywords[i] + "%'"

    # Execute the SQL
    dbcursor.execute(sql)

    # Return Fetchall result from SQL
    return dbcursor.fetchall()


# Login Section
################################################################


def welcome_window():  # RETURN VOID
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    print("Welcome to CodeX Library")
    print("Choose your login as:")
    print("1. Member")
    print("2. Staff")
    print("3. Admin")

    # Choose Tittle
    choice = input("Please ENTER your choice: ")
    while (True):
        if ("1" <= choice <= "3" and len(choice) == 1):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Choose your login as:")
            print("1. Member")
            print("2. Staff")
            print("3. Admin")
            print("You Have Enter INVALID Value!")
            choice = input("Please ENTER your choice: ")

    # Assign tittle
    global title
    if choice == "1":
        title = "Member"
    if choice == "2":
        title = "Staff"
    if choice == "3":
        title = "Admin"


def check_login(email, password):  # RETURN True or False

    # Execute the SELECT query to check if the email and password combination exists
    sql = f"SELECT * FROM {title} WHERE email = %s AND password = %s"

    # parameters = (email, password)
    parameters = (email, password)
    dbcursor.execute(sql, parameters)

    # Fetch the result of the query
    result = dbcursor.fetchone()

    global person

    # Check if the result is not None (i.e., the email and password combination exists)
    if result is not None:
        person = PersonInfo(result[0], result[1],
                            result[2], result[3], result[4], result[5])
        return True
    else:
        return False


def login_UI():  # return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    print(f"Please ENTER E-Mail and Password to login as {title}")

    email = input("E-Mail: ")
    password = input("Password: ")
    while True:
        if check_login(email, password):
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Login Successfull")
            print("Press ENTER to continue ...")
            input
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Email and Password is INVALID")
            print(f"Please Enter E-Mail and Password to login as {title}")
            email = input("E-Mail: ")
            password = input("Password: ")
################################################################

# Member UI & Function
################################################################


# Search_book Menu
###################################################################################################
def search_book_by_title(bookTitle):
    # Extract keywords
    keywords = bookTitle.split(" ")
    # Build SQL to search
    sql = f"SELECT * FROM Book WHERE availability <> 'Deleted' and ("
    for i in range(len(keywords)):
        if i == 0:
            sql += f"title LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR title LIKE '%" + keywords[i] + "%'"
    sql += ");"
    dbcursor.execute(sql)
    results = dbcursor.fetchall()
    if len(results) > 0:
        for book in results:
            print(book)
    else:
        print("No books found with title:", bookTitle)


def search_book_by_isbn(isbn):
    # Build SQL to search
    sql = f"SELECT * FROM Book WHERE availability <> 'Deleted' and (isbn LIKE '%{isbn}%');"
    dbcursor.execute(sql)
    results = dbcursor.fetchall()
    if len(results) > 0:
        for book in results:
            print(book)

    else:
        print("No books found with ISBN:", isbn)


def display_search_book_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Search book by: ")
    print("1. Title")
    print("2. ISBN")
    print("(Enter '-1' to BACK)")


def search_book():
    while True:
        display_search_book_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "2" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    # CLEAR SCREEN
                    os.system("cls" if os.name == "nt" else "clear")
                    # Input bookTitle
                    bookTitle = input("Search book title: ")
                    search_book_by_title(bookTitle)
                    input("Press ENTER to back to Search MENU")
                    break
                if choice == "2":
                    # CLEAR SCREEN
                    os.system("cls" if os.name == "nt" else "clear")
                    # Input ISBN
                    isbn = input("Search book ISBN: ")
                    search_book_by_isbn(isbn)
                    input("Press ENTER to back to Search MENU")
                    break
            else:
                display_search_book_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
###


# view_your_Order Menu
###
def display_view_order_menu_by_member(memberID):
    results = search_using_keywords_MySQL_selective_attribute(
        memberID, "memberID", "`order`", "orderID, isbn, status")
    print("|OrderID ||     ISBN      ||  Status  |")
    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No orders found")


def view_order_detail(orderID):
    # Build SQL to search
    sql = f"""SELECT
    o.orderID,
    o.staffID,
    s.fName AS staffFName,
    s.lName AS staffLName,
    o.memberID,
    m.fName AS memberFName,
    m.lName AS memberLName,
    o.isbn,
    b.title AS bookTitle,
    b.author AS bookAuthor,
    o.rentDate,
    o.dueDate,
    o.status,
    o.returnDate
FROM
    `Order` o
    INNER JOIN Staff s ON o.staffID = s.staffID
    INNER JOIN Member m ON o.memberID = m.memberID
    INNER JOIN Book b ON o.isbn = b.isbn
    where orderID = {orderID}"""

    # Execute the SQL
    dbcursor.execute(sql)

    # Return Fetchall result from SQL
    result = (dbcursor.fetchone())
    order = ViewOrder(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                      result[7], result[8], result[9], result[10], result[11], result[12], result[13])
    print(f"""OrderID: {order.orderID} Status: {order.status}
StaffID: {order.staffID}  Name: {order.staffFName} {order.staffLName}
MemberID: {order.memberID} Name: {order.memberFName} {order.memberLName}
Book ISBN: {order.bookIsbn}
Book Title: {order.bookTitle}
Book Author: {order.bookAuthor}
Rent Date: {order.rentDate}       Due Date: {order.dueDate}
Return Date: {order.returnDate}""")


def view_your_order():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        display_view_order_menu_by_member(person.ID)
        print("Enter orderID to view detail")
        print("(Enter '-1' to LOG OUT)")
        # Make Choice
        choice = input("ENTER orderID: ")
        while (True):
            if ("000000" <= choice <= "999999" and len(choice) == 6) or choice == "-1":
                if choice == "-1":
                    break
                else:
                    # CLEAR SCREEN
                    os.system("cls" if os.name == "nt" else "clear")
                    view_order_detail(choice)
                    input("(Press ENTER to return)")
                    break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                display_view_order_menu_by_member(person.ID)
                print("Enter orderID to view detail")
                print("(Enter '-1' to LOG OUT)")
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER OrderID: ")
        if choice == "-1":
            break


###
# edit_personal_information menu()
###
def display_edit_personal_information_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"""ID: {person.ID}
Name: {person.fName} {person.lName}
Email: {person.email}
Password: {"*" * 10}
Menu:
1. Edit Name
2. Edit Email
3. Edit Password
(Enter '-1' to Back)""")


def update_one_attribute_SQL(input, attribute, table, attributeToFind, valueTofind):
    sql = f"UPDATE  {table} SET {attribute} = '{input}' WHERE {attributeToFind} = '{valueTofind}';"
    dbcursor.execute(sql)
    db.commit()


def edit_name():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Name")
    fName = input("Enter New Frist Name: ")
    lName = input("Enter New Last Name: ")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"This is your New Name: {fName} {lName}")
    choice = input("Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        if choice == "Y" or "y" and len(choice) == 1:
            update_one_attribute_SQL(
                fName, "fName", title, f"{title}ID", person.ID)
            update_one_attribute_SQL(
                lName, "lName", title, f"{title}ID", person.ID)
            person.fName = fName
            person.lName = lName
            break
        if choice == "N" or "n" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print(f"This is your New Name: {fName} {lName}")
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")


def edit_email():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Email")
    email = input("Enter New Email: ")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"This is your New Email: {email}")
    choice = input("Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        if choice == "Y" or "y" and len(choice) == 1:
            update_one_attribute_SQL(
                email, "email", title, f"{title}ID", person.ID)
            person.email = email
            break
        if choice == "N" or "n" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print(f"This is your New Email: {email}")
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")


def edit_password():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Edit Password")
        password1 = input("Enter New Password: ")
        password2 = input("REPEAT New Password: ")
        if password1 == password2 and len(password1) != "":
            update_one_attribute_SQL(
                password1, "password", title, f"{title}ID", person.ID)
            person.password = password1
            print("Your Password has been successfully changed")
            input("(Press ENTER to Back)")
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("REPEAT New Password does not match the previous")
            print("(Enter '-1' to Cancel Process)")
            choice = input("Press any key to try again")
            if choice == "-1":
                break


def edit_personal_information():
    while True:
        display_edit_personal_information_menu()
        # Make Choice
        choice = input("ENTER your action: ")
        while (True):
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                edit_name()
                break
            if choice == "2" and len(choice) == 1:
                edit_email()
                break
            if choice == "3" and len(choice) == 1:
                edit_password()
                break
            else:
                display_edit_personal_information_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break

###

###
# Display Manage Book Menu


def display_manage_book_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Manage Book Menu
1. Search Book
2. Insert New Book
3. Edit Book
4. Delete Book
(ENTER '-1' to Back)""")


def display_book_info(book):

    print(f"""ISBN: {book.isbn}
Title: {book.title}
Author: {book.author}
Publisher: {book.publisher}
Shelf: {book.shelf}""")


def insert_new_book_SQL(newBook):
    sql = f"""INSERT INTO Book (isbn, title, author, publisher, availability, shelf)
VALUES ('{newBook.isbn}', '{newBook.title}', '{newBook.author}',
        '{ newBook.publisher}', '{newBook.availability}', '{newBook.shelf}')
ON DUPLICATE KEY UPDATE
    title = VALUES(title),
    author = VALUES(author),
    publisher = VALUES(publisher),
    availability = VALUES(availability),
    shelf = VALUES(shelf);"""
    dbcursor.execute(sql)
    db.commit()


def check_duplicate_isbn_SQL(isbn):
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    if result is not None:
        return True
    else:
        return False


def insert_new_book():
    newBook = Book("", "", "", "", "", "")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Insert New Book Information")
    print("(ISBN, Title, Author, Publisher, Shelf)")
    input("(Press ENTER to continue)")

    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        newBook.isbn = input("ISBN: ")
        isDuplicate = bool(False)
        isDuplicate = (check_duplicate_isbn_SQL(newBook.isbn))
        if "0000000000000" <= newBook.isbn <= "9999999999999" and len(newBook.isbn) == 13 and not isDuplicate:
            break
        else:
            if isDuplicate:
                print("The ISBN is already available")
            else:
                print("!!!You Have Enter INVALID Value!!!")
            input("(Press ENTER to RE-ENTER)")
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        newBook.title = input("Title: ")
        newBook.author = input("Author: ")
        newBook.publisher = input("Publisher: ")
        if len(newBook.title) and len(newBook.author) and len(newBook.publisher) <= 100:
            break
        else:
            if len(newBook.title) > 100:
                print("The Title is Too Long")
            if len(newBook.author) > 100:
                print("The Author is Too Long")
            if len(newBook.publisher) > 100:
                print("The Publisher is Too Long")
            input("(Press ENTER to RE-ENTER)")
    newBook.availability = "Available"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        newBook.shelf = input("Shelf(only one letter from A to Z): ")
        newBook.shelf = newBook.shelf.upper()
        if len(newBook.shelf) == 1 and "A" <= newBook.shelf <= "Z":
            break
        else:
            print("!!!You Have Enter INVALID Value!!!")
            input("(Press ENTER to RE-ENTER)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("New Book Information")
    display_book_info(newBook)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        if choice == "Y" or "y" and len(choice) == 1:
            insert_new_book_SQL(newBook)
            break
        if choice == "N" or "n" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("New Book Information")
            display_book_info(newBook)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")


def display_edit_book_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Book Menu")
    print("1. Search Book by Title to EDIT")
    print("2. Search Book by ISBN to EDIT")
    print("3. Enter book ISBN to EDIT")
    print("(Enter '-1' to BACK)")


def update_book_to_MySQL(book):
    update_one_attribute_SQL(
        book.title, "title", "book", "isbn", book.isbn)
    update_one_attribute_SQL(
        book.author, "author", "book", "isbn", book.isbn)
    update_one_attribute_SQL(
        book.publisher, "publisher", "book", "isbn", book.isbn)
    update_one_attribute_SQL(
        book.shelf, "shelf", "book", "isbn", book.isbn)


def search_book_by_isbn_to_edit():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input isbn
        isbn = input("Search book isbn: ")
        if isbn == "-1" and len(isbn) == 2:
            break
        search_book_by_isbn(isbn)
        print("Press ENTER if you want to search again")
        isbn = input("ENTER ISBN of Book you want to EDIT: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            print("The ISBN NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Book Information")
    display_book_info(book)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newTitle = input("ENTER New Title: ")
    if not len(newTitle) == 0:
        book.title = newTitle
    newAuthor = input("ENTER New Author: ")
    if not len(newAuthor) == 0:
        book.author = newAuthor
    newPublisher = input("ENTER New Publisher: ")
    if not len(newPublisher) == 0:
        book.publisher = newPublisher
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Choose Shelf from A to Z")
    newShelf = input("ENTER New Shelf: ")
    while True:
        newShelf = newShelf.upper()
        if ("A" <= newShelf <= "Z" and len(newShelf) == 1) or (len(newShelf) == 0):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Please Choose Shelf from A to Z")
            print("!!!You Have Enter INVALID Value!!!")
            newShelf = input("ENTER New Shelf: ")
    if not len(newShelf) == 0:
        book.shelf = newShelf
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_book_to_MySQL(book)
            print("Update Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def search_book_by_title_to_edit():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input isbn
        title = input("Search book title: ")
        if title == "-1" and len(title) == 2:
            break
        search_book_by_title(title)
        print("Press ENTER if you want to search again")
        isbn = input("ENTER ISBN of Book you want to EDIT: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            print("The ISBN NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Book Information")
    display_book_info(book)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newTitle = input("ENTER New Title: ")
    if not len(newTitle) == 0:
        book.title = newTitle
    newAuthor = input("ENTER New Author: ")
    if not len(newAuthor) == 0:
        book.author = newAuthor
    newPublisher = input("ENTER New Publisher: ")
    if not len(newPublisher) == 0:
        book.publisher = newPublisher
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Choose Shelf from A to Z")
    newShelf = input("ENTER New Shelf: ")
    while True:
        newShelf = newShelf.upper()
        if ("A" <= newShelf <= "Z" and len(newShelf) == 1) or (len(newShelf) == 0):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Please Choose Shelf from A to Z")
            print("!!!You Have Enter INVALID Value!!!")
            newShelf = input("ENTER New Shelf: ")
    if not len(newShelf) == 0:
        book.shelf = newShelf
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_book_to_MySQL(book)
            print("Update Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_book_by_isbn():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        isbn = input("ENTER ISBN of Book you want to EDIT: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            print("The ISBN NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Book Information")
    display_book_info(book)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newTitle = input("ENTER New Title: ")
    if not len(newTitle) == 0:
        book.title = newTitle
    newAuthor = input("ENTER New Author: ")
    if not len(newAuthor) == 0:
        book.author = newAuthor
    newPublisher = input("ENTER New Publisher: ")
    if not len(newPublisher) == 0:
        book.publisher = newPublisher
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Choose Shelf from A to Z")
    newShelf = input("ENTER New Shelf: ")
    while True:
        newShelf = newShelf.upper()
        if ("A" <= newShelf <= "Z" and len(newShelf) == 1) or (len(newShelf) == 0):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Please Choose Shelf from A to Z")
            print("!!!You Have Enter INVALID Value!!!")
            newShelf = input("ENTER New Shelf: ")
    if not len(newShelf) == 0:
        book.shelf = newShelf
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_book_to_MySQL(book)
            print("Update Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_book():
    while True:
        display_edit_book_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_book_by_title_to_edit()
                    break
                if choice == "2":
                    search_book_by_isbn_to_edit()
                    break
                if choice == "3":
                    edit_book_by_isbn()
                    break
            else:
                display_edit_book_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break


def display_delete_book_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delet Book Menu")
    print("1. Search Book by Title to Delete")
    print("2. Search Book by ISBN to Delete")
    print("3. Enter book ISBN to Delete")
    print("(Enter '-1' to BACK)")


def search_book_by_isbn_to_delete():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input isbn
        isbn = input("Search book isbn: ")
        if isbn == "-1" and len(isbn) == 2:
            break
        search_book_by_isbn(isbn)
        print("Press ENTER if you want to search again")
        isbn = input("ENTER isbn of Book you want to DELETE: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The ISBN NOT EXIST Or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])
    if book.availability == "On Loan":
        print("Book is currently On Loan")
        print("CANNOT DELETE")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        choice = choice.upper()
        if (choice == "Y") and (len(choice) == 1):
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Deleted", "availability", "book", "isbn", isbn)
            print("Delete Book Successful")
            input("(Press Enter to continue)")
            break
        if (choice == "N") and (len(choice) == 1):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")


def search_book_by_title_to_delete():
    isbn = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        bookTitle = input("Search book title: ")
        if bookTitle == "-1" and len(bookTitle) == 2:
            break
        search_book_by_title(bookTitle)
        print("Press ENTER if you want to search again")

        isbn = input("ENTER isbn of Book you want to DELETE: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The ISBN NOT EXIST Or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2) or (bookTitle == "-1" and len(bookTitle) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])

    if book.availability == "On Loan":
        print("Book is currently On Loan")
        print("CANNOT DELETE")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) to Cancel: ")
    while True:
        choice = choice.upper()
        if (choice == "Y") and (len(choice) == 1):
            input(choice)
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Deleted", "availability", "book", "isbn", isbn)
            print("Delete Book Successful")
            input("(Press Enter to continue)")
            break
        if (choice == "N") and (len(choice) == 1):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_book_by_isbn():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        isbn = input("ENTER isbn of Book you want to DELETE: ")
        isExist = bool(False)
        isExist = (check_duplicate_isbn_SQL(isbn))
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and isExist) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            print("The ISBN NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])

    if book.availability == "On Loan":
        print("Book is currently On Loan")
        print("CANNOT DELETE")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Deleted", "availability", "book", "isbn", isbn)
            print("Delete Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_book():
    while True:
        display_delete_book_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_book_by_title_to_delete()
                    break
                if choice == "2":
                    search_book_by_isbn_to_delete()
                    break
                if choice == "3":
                    delete_book_by_isbn()
                    break
            else:
                display_delete_book_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break


def manage_book():
    while True:
        display_manage_book_menu()
        choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
        if choice == "1" and len(choice) == 1:
            search_book()
        if choice == "2" and len(choice) == 1:
            insert_new_book()
        if choice == "3" and len(choice) == 1:
            edit_book()
        if choice == "4" and len(choice) == 1:
            delete_book()
        else:
            display_manage_book_menu()
            print("!!!You Have Enter INVALID Value!!!")
            choice = input("ENTER your action: ")


###
###
# Display Manage Order Menu
def display_manage_order_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Manage Order Menu:
1. Search Order
2. Create New Order
3. Edit Order
4. Recieve Returning Book
(Enter '-1' to BACK)""")


def display_search_order_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Search Order Menu:
1. Search Order by ISBN
2. Search Order by MemberID
(Enter '-1' to BACK)""")


def display_view_order_menu_by_isbn(isbn):
    results = search_using_keywords_MySQL_selective_attribute(
        isbn, "isbn", "`order`", "orderID, isbn, status")
    print("|OrderID ||     ISBN      ||  Status  |")
    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No orders found")


def search_order_by_isbn():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Order by ISBN")
        print("(Enter '-1' to BACK)")
        isbn = input("ENTER ISBN: ")
        if isbn == "-1" and len(isbn) == 2:
            break
        display_view_order_menu_by_isbn(isbn)
        print("Press ENTER if you want to search again")
        print("Enter orderID to view detail")
        # Make Choice
        choice = input("ENTER orderID: ")
        if ("000000" <= choice <= "999999" and len(choice) == 6) or choice == "-1":
            if choice == "-1":
                break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                view_order_detail(choice)
                input("(Press ENTER to return)")
                break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("!!!OrderID NOT EXIST or IS INVALID !!!")
            input("(Press ENTER to RE-ENTER)")


def search_order_by_memberID():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Order by MemberID")
        print("(Enter '-1' to BACK)")
        memberID = input("ENTER MemberID: ")
        if memberID == "-1" and len(memberID) == 2:
            break
        display_view_order_menu_by_member(memberID)
        print("Press ENTER if you want to search again")
        print("Enter orderID to view detail")
        # Make Choice
        choice = input("ENTER orderID: ")
        if ("000000" <= choice <= "999999" and len(choice) == 6) or choice == "-1":
            if choice == "-1":
                break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                view_order_detail(choice)
                input("(Press ENTER to return)")
                break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("!!!OrderID NOT EXIST or IS INVALID !!!")
            input("(Press ENTER to RE-ENTER)")


def search_order():
    while True:
        display_search_order_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_order_by_isbn()
                break
            if choice == "2" and len(choice) == 1:
                search_order_by_memberID()
                break
            else:
                display_search_order_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break


def display_edit_order_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Edit Order Menu:
1. Search Order by ID to EDIT
2. Search Order by staffID to EDIT
3. EDIT Order by ID
(Enter '-1' to BACK)""")


def check_duplicate_orderID_SQL(orderID):
    result = search_using_exact_keywords_MySQL(orderID, "orderID", "`Order`")
    if result is not None:
        return True
    else:
        return False


def check_duplicate_SQL(value, attribute, table):
    result = search_using_exact_keywords_MySQL(value, attribute, table)
    if result is not None:
        return True
    else:
        return False


def update_order_to_MySQL(memberID, isbn, orderID):
    update_one_attribute_SQL(
        memberID, "memberID", "`Order`", "orderID", orderID)
    update_one_attribute_SQL(
        isbn, "isbn", "`Order`", "orderID", orderID)


def display_new_order_detail(newOrder):
    sql = f"SELECT fName, lName FROM Staff WHERE staffID = '{newOrder.staffID}'"
    result = fetchone_from_MySQL(sql)
    staffFName = result[0]
    staffLName = result[1]
    sql = f"SELECT fName, lName FROM Member WHERE memberID = '{newOrder.memberID}'"
    result = fetchone_from_MySQL(sql)
    memberFName = result[0]
    memberLName = result[1]
    sql = f"SELECT title, author FROM Book WHERE isbn = '{newOrder.isbn}'"
    result = fetchone_from_MySQL(sql)
    bookTitle = result[0]
    bookAuthor = result[1]

    print(f"""OrderID: {newOrder.orderID}
StaffID: {newOrder.staffID}  Name: {staffFName} {staffLName}
MemberID: {newOrder.memberID} Name: {memberFName} {memberLName}
Book ISBN: {newOrder.isbn}
Book Title: {bookTitle}
Book Author: {bookAuthor}
Rent Date: {newOrder.rentDate}       Due Date: {newOrder.dueDate}""")


def create_new_order():
    newOrder = Order()
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Create New Order")
    print("(ENTER '-1' to Back)")
    newOrder.memberID = input("Enter MemberID for New Order: ")
    while True:
        if ("MB000" <= newOrder.memberID <= "MB999" and len(newOrder.memberID) == 5 and check_duplicate_SQL(newOrder.memberID, "memberID", "Member")) or (newOrder.memberID == "-1" and len(newOrder.memberID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Create New Order")
            print("(ENTER '-1' to Back)")
            print("!!!MemberID NOT EXIST or INVALID!!!")
            newOrder.memberID = input("Enter MemberID for New Order: ")
    if newOrder.memberID == "-1" and len(newOrder.memberID) == 2:
        return

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Create New Order")
    print("(ENTER '-1' to Back)")
    newOrder.isbn = input("Enter Book ISBN for New Order: ")
    while True:
        if ("0000000000000" <= newOrder.isbn <= "9999999999999" and len(newOrder.isbn) == 13 and check_duplicate_SQL(newOrder.isbn, "isbn", "Book")) or (newOrder.isbn == "-1" and len(newOrder.isbn) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Create New Order")
            print("(ENTER '-1' to Back)")
            print("!!!ISBN NOT EXIST or INVALID!!!")
            newOrder.isbn = input("Enter Book ISBN for New Order: ")
    if newOrder.isbn == "-1" and len(newOrder.isbn) == 2:
        return

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Create New Order")
    print("(ENTER '-1' to Back)")
    numberOfRentDays = input("Enter Borrow Time in Days(Up to 30 Days): ")
    while True:
        if numberOfRentDays == "-1" and len(numberOfRentDays) == 2:
            break
        if len(numberOfRentDays) <= 2:
            numberOfRentDays.zfill(2)
            if ("0" <= (numberOfRentDays[0]) <= "9") and ("0" <= (numberOfRentDays[1]) <= "9"):
                if 1 <= int(numberOfRentDays) <= 30:
                    break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Create New Order")
            print("(ENTER '-1' to Back)")
            numberOfRentDays = input(
                "Enter Borrow Time in Days(Up to 30 Days): ")
    if numberOfRentDays == "-1" and len(numberOfRentDays) == 2:
        return

    sql = "SELECT MAX(orderID) FROM `Order`"
    result = fetchone_from_MySQL(sql)
    latestOrderID = result[0]
    newOrder.orderID = str(int(latestOrderID)+1).zfill(6)
    newOrder.staffID = person.ID
    newOrder.rentDate = datetime.datetime.now()
    newOrder.dueDate = newOrder.rentDate.date() + timedelta(days=int(numberOfRentDays))
    newOrder.status = "On Loan"

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    display_new_order_detail(newOrder)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            sql = f"""INSERT IGNORE INTO `Order` (orderID, staffID, memberID, isbn, rentDate, dueDate, status) 
VALUES ('{newOrder.orderID}', '{newOrder.staffID}', '{newOrder.memberID}', '{newOrder.isbn}', '{newOrder.rentDate}', '{newOrder.dueDate}', '{newOrder.status}')
            """
            update_to_MySQL(sql)
            update_one_attribute_SQL(
                "On Loan", "avalability", "book", "isbn", newOrder.isbn)
            print("Create Order Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Information")
            display_new_order_detail(newOrder)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_order():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        orderID = input("ENTER OrderID you want to EDIT: ")
        if ("000000" <= orderID <= "999999" and len(orderID) == 6 and check_duplicate_orderID_SQL(orderID)) or (orderID == "-1" and len(orderID) == 2):
            break
        else:
            print("The OrderID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (orderID == "-1" and len(orderID) == 2):
        return

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Order Information")
    view_order_detail(orderID)
    sql = f"SELECT memberID FROM `Order` WHERE orderID = '{orderID}'"
    result = fetchone_from_MySQL(sql)
    currMemberID = result[0]
    sql = f"SELECT isbn FROM `Order` WHERE orderID = '{orderID}'"
    result = fetchone_from_MySQL(sql)
    currIsbn = result[0]
    input("(Press ENTER to continue)")

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    memberID = input("ENTER New MemberID: ")
    while True:
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5) or (len(memberID) == 0):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("!!!You Have Enter INVALID Value!!!")
            print("(Leave BLANK if you to keep the same data)")
            memberID = input("ENTER New Book MemberID: ")
    if len(memberID) != 0:
        update_one_attribute_SQL(memberID, "memberID",
                                 "`Order`", "orderID", orderID)

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    isbn = input("ENTER New Book ISBN: ")
    while True:
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13 and check_duplicate_isbn_SQL(isbn)) or (len(isbn) == 0):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("ISBN NOT EXIST or IS INVALID")
            print("(Leave BLANK if you to keep the same data)")
            isbn = input("ENTER New Book ISBN: ")
    if not len(isbn) == 0:
        update_one_attribute_SQL(
            isbn, "isbn", "`Order`", "orderID", orderID)

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Order Information")
    view_order_detail(orderID)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            update_order_to_MySQL(
                currMemberID, currIsbn, orderID)
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Book Information")
            view_order_detail(orderID)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def recieve_returning_book():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Receive Returning Book")
    print("(Enter '-1' to BACK)")
    isbn = input("ENTER ISBN of Returning Book: ")
    while True:
        if ("0000000000000" <= isbn <= "9999999999999" and len(isbn) == 13) or (isbn == "-1" and len(isbn) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Receive Returned Book")
            print("The ISBN NOT EXIST or IS INVALID")
            print("(Enter '-1' to BACK)")
            isbn = input("ENTER ISBN of Returned Book: ")
    if (isbn == "-1" and len(isbn) == 2):
        return
    result = search_using_exact_keywords_MySQL(isbn, "isbn", "Book")
    book = Book()
    book.isbn = result[0]
    book.title = result[1]
    book.author = result[2]
    book.publisher = result[3]
    book.availability = result[4]
    book.shelf = result[5]
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Returning Book Information")
    display_book_info(book)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            # CLEAR SCREEN
            os.system("cls" if os.name == "nt" else "clear")
            update_one_attribute_SQL(
                "Available", "availability", "book", "isbn", isbn)
            update_one_attribute_SQL(
                "Returned", "status", "`order`", "isbn", isbn)
            update_one_attribute_SQL(
                datetime.datetime.now(), "returnDate", "`order`", "isbn", isbn)
            print("Returning Book Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            # CLEAR SCREEN
            os.system("cls" if os.name == "nt" else "clear")
            print("Returning Book Information")
            display_book_info(book)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def manage_order():
    while True:
        display_manage_order_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_order()
                break
            if choice == "2" and len(choice) == 1:
                create_new_order()
                break
            if choice == "3" and len(choice) == 1:
                edit_order()
                break
            if choice == "4" and len(choice) == 1:
                recieve_returning_book()
                break
            else:
                display_manage_order_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
###
###
# Manage Member Menu
def display_manage_member_menu
def manage_member()
###


def display_member_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Member Menu:")
    print("1. Search Book")
    print("2. View Your Order")
    print("3. Edit Personal Information")
    print("(Enter '-1' to LOG OUT)")


def member_UI():
    while True:
        display_member_menu()
        # Make Choice
        choice = input("ENTER your action: ")
        while (True):
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_book()
                break
            if choice == "2" and len(choice) == 1:
                view_your_order()
                break
            if choice == "3" and len(choice) == 1:
                edit_personal_information()
                break
            else:
                display_member_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break


def display_staff_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Staff Menu:")
    print("1. Manage Book")
    print("2. Manage Order")
    print("3. Manage Member")
    print("4. Edit Personal Information")
    print("(Enter '-1' to LOG OUT)")


def staff_UI():
    while True:
        display_staff_menu()
        # Make Choice
        choice = input("ENTER your action: ")
        while (True):
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                manage_book()
                break
            if choice == "2" and len(choice) == 1:
                manage_order()
                break
            if choice == "3" and len(choice) == 1:
                manage_member()
                break
            if choice == "4" and len(choice) == 1:
                edit_personal_information()
                break
            else:
                display_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break


def display_admin_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Admin Menu:")
    print("1. Manage Book")
    print("2. Manage Order")
    print("3. Manage Member")
    print("4. Manage Staff")
    print("5. Gennerate Report")
    print("6. Edit Personal Information")
    print("(Enter '-1' to LOG OUT)")


def admin_UI():
    while True:
        display_admin_menu()
        # Make Choice
        choice = input("ENTER your action: ")
        while (True):
            if choice == "-1" and len(choice) == 2:
                break

            if choice == "6" and len(choice) == 1:
                edit_personal_information()
                break
            else:
                display_admin_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break

################################################################


# MAIN
connect_to_database()
while True:
    welcome_window()
    login_UI()
    if title == "Member":
        member_UI()
    if title == "Staff":
        staff_UI()
    if title == "Admin":
        admin_UI()
