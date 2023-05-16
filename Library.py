import os
import mysql.connector
import datetime
from datetime import datetime, timedelta, date


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
###


# Database Function
def connect_to_database():
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
    # Execute and Update in Database
    dbcursor.execute(sql)
    db.commit()


def fetchone_from_MySQL(sql):
    # Execute the SQL
    dbcursor.execute(sql)
    # Return Fetchone result from SQL
    return dbcursor.fetchone()


def fetchall_from_MySQL(sql):
    # Execute the SQL
    dbcursor.execute(sql)
    # Return Fetchall result from SQL
    return dbcursor.fetchall()


def search_using_keywords_MySQL(inputString, attribute, table):
    # Extract keywords
    keywords = inputString.split(" ")
    # Build SQL to search in MySQL
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


def update_order_status_SQL():
    # get current datetime
    now = datetime.now()
    # Build SQL to Udate
    sql = f"SELECT orderID FROM `Order` WHERE dueDate < '{now}' AND returnDate is NULL;"
    result = fetchall_from_MySQL(sql)
    # update all order is overdue
    for itr in result:
        sql = f"UPDATE `Order` SET status = 'Overdue' WHERE orderID = '{itr[0]}'"
        update_to_MySQL(sql)
    # fetch all book isbn is not return yet
    sql = f"SELECT isbn FROM `Order` WHERE returnDate IS NULL;"
    result = fetchall_from_MySQL(sql)
    # update all book is not return yet
    for itr in result:
        sql = f"UPDATE Book SET availability = 'On Loan' WHERE isbn = '{itr[0]}'"
        update_to_MySQL(sql)


def update_one_attribute_SQL(input, attribute, table, attributeToFind, valueTofind):
    sql = f"UPDATE  {table} SET {attribute} = '{input}' WHERE {attributeToFind} = '{valueTofind}';"
    dbcursor.execute(sql)
    db.commit()
###


# Login Section
def welcome_window():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    # Display Window
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
            # Display Window
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


def check_login(email, password):
    # Execute the SELECT query to check if the email and password combination exists
    sql = f"SELECT * FROM {title} WHERE email = %s AND password = %s"
    # parameters = (email, password)
    parameters = (email, password)
    dbcursor.execute(sql, parameters)
    # Fetch the result of the query
    result = dbcursor.fetchone()
    # Check if Email and Password valid
    global person
    if result is not None:
        person = PersonInfo(result[0], result[1],
                            result[2], result[3], result[4], result[5])
        return True
    else:
        return False


def login_UI():
    welcome_window()
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    # Display Login Window to input email and password
    print(f"Please ENTER E-Mail and Password to login as {title}")
    email = input("E-Mail: ")
    password = input("Password: ")
    while True:
        if check_login(email, password):
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            break
        else:
            print("Email and Password is INVALID")
            input("(Press ENTER to Login Again)")
            welcome_window()
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print(f"Please Enter E-Mail and Password to login as {title}")
            email = input("E-Mail: ")
            password = input("Password: ")
###

# Search Book


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
    # Execute the SQL and print book
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
    # Execute the SQL and print book
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


# View Order
def display_view_order_menu_by_member(memberID):
    results = search_using_keywords_MySQL_selective_attribute(
        memberID, "memberID", "`order`", "orderID, isbn, status")
    print("|OrderID ||     ISBN      ||  Status  |")
    # Display all available Order
    if len(results) > 0:
        for order in results:
            print(order)
    else:
        print("No orders found")


def view_order_detail(orderID):
    # Build SQL to Get data
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
    # Display Order Detail Information
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
            # Check if input is VALID
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

# Edit Personal Information


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


def edit_name():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Name")
    fName = input("Enter New Frist Name: ")
    lName = input("Enter New Last Name: ")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"This is your New Name: {fName} {lName}")
    choice = input("Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            # Update New Data to Database
            update_one_attribute_SQL(
                fName, "fName", title, f"{title}ID", person.ID)
            update_one_attribute_SQL(
                lName, "lName", title, f"{title}ID", person.ID)
            person.fName = fName
            person.lName = lName
            break
        if choice == "N" and len(choice) == 1:
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
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            # Update New Data to Database
            update_one_attribute_SQL(
                email, "email", title, f"{title}ID", person.ID)
            person.email = email
            break
        if choice == "N" and len(choice) == 1:
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
            # Update Data to Database
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

# Manage Book Menu


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
    if (result is not None) and result[4] != "Deleted":
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
        # Check if input is VALID
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
        if len(newBook.title) == 0:
            print("The Title Cannot be BLANK")
        else:
            break
        input("(Press ENTER to RE-ENTER)")
    newBook.availability = "Available"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        newBook.shelf = input("Shelf(only one letter from A to Z): ")
        newBook.shelf = newBook.shelf.upper()
        # Check if input is VALID
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
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            insert_new_book_SQL(newBook)
            print("Insert New Book Successfully")
            input("(Press ENTER to Continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("New Book Information")
            display_book_info(newBook)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")

# Edit Book


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
        # Check if input is VALID
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
        # Check if input is VALID
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
######

# Delete Book


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
        # Check if input is VALID
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
        # Check if input is VALID
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
        # Check if input is VALID
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
######


def manage_book():
    while True:
        display_manage_book_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_book()
                break
            if choice == "2" and len(choice) == 1:
                insert_new_book()
                break
            if choice == "3" and len(choice) == 1:
                edit_book()
                break
            if choice == "4" and len(choice) == 1:
                delete_book()
                break
            else:
                display_manage_book_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
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

# Search Order


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
        orderID = input("ENTER orderID: ")
        if ("000000" <= orderID <= "999999" and len(orderID) == 6) or orderID == "-1":
            if orderID == "-1":
                break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                view_order_detail(orderID)
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
######


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

# Create New Order


def create_new_order():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    if title == "Admin":
        print("Admin Cannot Create New Order")
        print("Please Login as Staff to Create New Order")
        input("Press ENTER to Back")
        return
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
    newOrder.rentDate = datetime.now()
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
VALUES ('{newOrder.orderID}', '{newOrder.staffID}', '{newOrder.memberID}',
        '{newOrder.isbn}', '{newOrder.rentDate}', '{newOrder.dueDate}', '{newOrder.status}')
            """
            update_to_MySQL(sql)
            update_one_attribute_SQL(
                "On Loan", "availability", "book", "isbn", newOrder.isbn)
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
######

# Edit Order


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
######

# Recieve Returning Book


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
    book = Book(result[0], result[1], result[2],
                result[3], result[4], result[5])
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
                datetime.now(), "returnDate", "`order`", "isbn", isbn)
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
######


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

# Manage Member Menu


def display_manage_member_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Manage Member Menu:
1. Search Member
2. Create New Member
3. Edit Member
4. Delete Member
(Enter '-1' to BACK)""")

# Search Member


def display_search_member_menu():
    print("""Search Member Menu:
1. Search Member by Email
2. Search Member by Name
(Enter '-1' to BACK)""")


def display_search_member_by_email(email):
    # Extract keywords
    keywords = email.split(" ")
    # Build SQL to search
    sql = f"SELECT memberID, fName, lName, email FROM member WHERE ("
    for i in range(len(keywords)):
        if i == 0:
            sql += f"email LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR email LIKE '%" + keywords[i] + "%'"

    sql += ") AND status <> 'Disabled'"
    results = fetchall_from_MySQL(sql)
    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No Member Found")


def search_member_by_email():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Member by Email")
        print("(Enter '-1' to BACK)")
        email = input("ENTER Email: ")
        if email == "-1" and len(email) == 2:
            break
        # conver email to keyword to search
        display_search_member_by_email(email)
        input("(Press ENTER to Search Again)")


def display_search_member_by_name(name):
    # Extract keywords
    keywords = name.split(" ")
    # Build SQL to search
    sql = f"SELECT memberID, fName, lName, email FROM member WHERE ("
    for i in range(len(keywords)):
        if i == 0:
            sql += f"fName LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR fName LIKE '%" + keywords[i] + "%'"
    for i in range(len(keywords)):
        sql += f" OR lName LIKE '%" + keywords[i] + "%'"
    sql += ") AND status <> 'Disabled'"
    results = fetchall_from_MySQL(sql)

    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No Member Found")


def search_member_by_name():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Member by Name")
        print("(Enter '-1' to BACK)")
        name = input("ENTER Member Name: ")
        if name == "-1" and len(name) == 2:
            break
        # conver email to keyword to search
        display_search_member_by_name(name)
        input("(Press ENTER to Search Again)")


def search_member():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        display_search_member_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_member_by_email()
                break
            if choice == "2" and len(choice) == 1:
                search_member_by_name()
                break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                display_search_member_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
######

# Create member


def insert_new_member_SQL(newMember):
    sql = f"""INSERT INTO Member (memberID, fName, lName, email, password, status)
VALUES ('{newMember.ID}', '{newMember.fName}', '{newMember.lName}',
        '{ newMember.email}', '{newMember.password}', '{newMember.status}')
ON DUPLICATE KEY UPDATE
    memberID = VALUES(memberID),
    fName = VALUES(fName),
    lName = VALUES(lName),
    email = VALUES(email),
    password = VALUES(password),
    status = VALUES(status);"""
    dbcursor.execute(sql)
    db.commit()


def create_new_member():
    newMember = PersonInfo("", "", "", "", "", "")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Insert New Member Information")
    print("(First Name, Last Name, Email, Password)")
    input("(Press ENTER to continue)")
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Please Insert New Member Information")
        print("(ENTER '-1' to Back)")
        isReturn = False
        newMember.fName = input("Frist Name: ")
        if newMember.fName == "-1" and len(newMember.fName) == 2:
            isReturn = True
            break
        newMember.lName = input("Last Name: ")
        if newMember.lName == "-1" and len(newMember.lName) == 2:
            isReturn = True
            break
        newMember.email = input("Email: ")
        if newMember.email == "-1" and len(newMember.email) == 2:
            isReturn = True
            break
        newMember.password = input("Password: ")
        if newMember.password == "-1" and len(newMember.password) == 2:
            isReturn = True
            break
        isBreak = True
        if len(newMember.fName) == 0:
            isBreak = False
            print("!!!Frist Name CANNOT be BLANK!!!")
        if len(newMember.lName) == 0:
            isBreak = False
            print("!!!Last Name CANNOT be BLANK!!!")
        if len(newMember.email) == 0:
            isBreak = False
            print("!!!Email CANNOT be BLANK!!!")
        if len(newMember.password) == 0:
            isBreak = False
            print("!!!Password CANNOT be BLANK!!!")
        if isBreak:
            break
        input("(Press ENTER to RE-ENTER)")
    if isReturn:
        return

    newMember.status = "Active"
    sql = "SELECT MAX(memberID) FROM Member;"
    result = fetchone_from_MySQL(sql)
    latestMemberIDnumber = result[0]
    newMember.ID = "MB"+str(int(latestMemberIDnumber[-3:])+1).zfill(3)

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("New Member Information")
    display_member_info(newMember)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            insert_new_member_SQL(newMember)
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("New Member Information")
            display_member_info(newMember)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
######

# Edit member


def display_edit_member_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Member Menu")
    print("1. Search Member by Email to EDIT")
    print("2. Search Member by Name to EDIT")
    print("3. Enter MemberID to EDIT")
    print("(Enter '-1' to BACK)")


def update_member_to_MySQL(member):
    update_one_attribute_SQL(
        member.fName, "fName", "member", "memberID", member.ID)
    update_one_attribute_SQL(
        member.lName, "lName", "member", "memberID", member.ID)
    update_one_attribute_SQL(
        member.email, "email", "member", "memberID", member.ID)


def search_member_by_email_to_edit():
    email = "-1"
    memberID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        email = input("Search Member Email: ")
        if email == "-1" and len(email) == 2:
            break
        display_search_member_by_email(email)
        print("Press ENTER if you want to search again")

        memberID = input("ENTER MemberID you want to EDIT: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    if (email == "-1" and len(email) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Member Information")
    display_member_info(member)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        member.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        member.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        member.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_member_to_MySQL(member)
            print("Update Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Member Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def search_member_by_name_to_edit():
    name = "-1"
    memberID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        name = input("Search Member Name: ")
        if name == "-1" and len(name) == 2:
            break
        display_search_member_by_name(name)
        print("Press ENTER if you want to search again")

        memberID = input("ENTER MemberID you want to EDIT: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    if (name == "-1" and len(name) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Member Information")
    display_member_info(member)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        member.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        member.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        member.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_member_to_MySQL(member)
            print("Update Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Member Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_member_by_ID():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        memberID = input("ENTER MemberID you want to EDIT: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    if member.status == "Disabled":
        print("Member has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Member Information")
    display_member_info(member)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        member.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        member.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        member.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_member_to_MySQL(member)
            print("Update Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Member Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_member():
    while True:
        display_edit_member_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_member_by_email_to_edit()
                    break
                if choice == "2":
                    search_member_by_name_to_edit()
                    break
                if choice == "3":
                    edit_member_by_ID()
                    break
            else:
                display_edit_member_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
######

# Delete Member


def display_delete_member_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delet Member Menu")
    print("1. Search Member by Email to Delete")
    print("2. Search Member by Name to Delete")
    print("3. Enter MemberID to Delete")
    print("(Enter '-1' to BACK)")


def display_member_info(member):
    print(f"""MemberID: {member.ID}
Name: {member.fName} {member.lName}
Email: {member.email}""")


def search_member_by_email_to_delete():
    email = "-1"
    memberID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        email = input("Search Member Email: ")
        if email == "-1" and len(email) == 2:
            break
        display_search_member_by_email(email)
        print("Press ENTER if you want to search again")

        memberID = input("ENTER MemberID you want to DELETE: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    if (email == "-1" and len(email) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    if member.status == "Disabled":
        print("Member has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "member", "memberID", member.ID)
            print("Delete Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def search_member_by_name_to_delete():
    name = "-1"
    memberID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        name = input("Search Member Name: ")
        if name == "-1" and len(name) == 2:
            break
        display_search_member_by_name(name)
        print("Press ENTER if you want to search again")

        memberID = input("ENTER MemberID you want to DELETE: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    if (name == "-1" and len(name) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    if member.status == "Disabled":
        print("Member has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "member", "memberID", member.ID)
            print("Delete Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_member_by_ID():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        memberID = input("ENTER MemberID you want to DELETE: ")
        if ("MB000" <= memberID <= "MB999" and len(memberID) == 5 and check_duplicate_SQL(memberID, "memberID", "Member")) or (memberID == "-1" and len(memberID) == 2):
            break
        else:
            print("The MemberID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (memberID == "-1" and len(memberID) == 2):
        return
    result = search_using_exact_keywords_MySQL(memberID, "memberID", "Member")
    member = PersonInfo(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    if member.status == "Disabled":
        print("Member has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Member Information")
    display_member_info(member)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "member", "memberID", member.ID)
            print("Delete Member Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_member_info(member)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_member():
    while True:
        display_delete_member_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_member_by_email_to_delete()
                    break
                if choice == "2":
                    search_member_by_name_to_delete()
                    break
                if choice == "3":
                    delete_member_by_ID()
                    break
            else:
                display_delete_member_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
######


def manage_member():
    while True:
        display_manage_member_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_member()
                break
            if choice == "2" and len(choice) == 1:
                create_new_member()
                break
            if choice == "3" and len(choice) == 1:
                edit_member()
                break
            if choice == "4" and len(choice) == 1:
                delete_member()
                break
            else:
                display_manage_order_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
###

# Manage Staff


def display_manage_staff_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Manage Staff Menu:
1. Search Staff
2. Create New Staff
3. Edit Staff
4. Delete Staff
(Enter '-1' to BACK)""")

# Search Staff


def display_search_staff_menu():
    print("""Search Staff Menu:
1. Search Staff by Email
2. Search Staff by Name
(Enter '-1' to BACK)""")


def display_search_staff_by_email(email):
    # Extract keywords
    keywords = email.split(" ")
    # Build SQL to search
    sql = f"SELECT staffID, fName, lName, email FROM Staff WHERE ("
    for i in range(len(keywords)):
        if i == 0:
            sql += f"email LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR email LIKE '%" + keywords[i] + "%'"
    sql += ") AND status <> 'Disabled'"
    results = fetchall_from_MySQL(sql)
    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No Staff Found")


def search_staff_by_email():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Staff by Email")
        print("(Enter '-1' to BACK)")
        email = input("ENTER Email: ")
        if email == "-1" and len(email) == 2:
            break
        # conver email to keyword to search
        display_search_staff_by_email(email)
        input("(Press ENTER to Search Again)")


def display_search_staff_by_name(name):
    # Extract keywords
    keywords = name.split(" ")
    # Build SQL to search
    sql = f"SELECT staffID, fName, lName, email FROM Staff WHERE ("
    for i in range(len(keywords)):
        if i == 0:
            sql += f"fName LIKE '%" + keywords[i] + "%'"
        else:
            sql += f" OR fName LIKE '%" + keywords[i] + "%'"
    for i in range(len(keywords)):
        sql += f"OR lName LIKE '%" + keywords[i] + "%'"
    sql += ") AND status <> 'Disabled'"
    results = fetchall_from_MySQL(sql)

    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No Staff Found")


def search_staff_by_name():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Search Staff by Name")
        print("(Enter '-1' to BACK)")
        name = input("ENTER Staff Name: ")
        if name == "-1" and len(name) == 2:
            break
        # conver email to keyword to search
        display_search_staff_by_name(name)
        input("(Press ENTER to Search Again)")


def search_staff():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        display_search_staff_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_staff_by_email()
                break
            if choice == "2" and len(choice) == 1:
                search_staff_by_name()
                break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")
                display_search_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
######

# Create Staff


def insert_new_staff_SQL(newStaff):
    sql = f"""INSERT INTO Staff (staffID, fName, lName, email, password, status)
VALUES ('{newStaff.ID}', '{newStaff.fName}', '{newStaff.lName}',
        '{ newStaff.email}', '{newStaff.password}', '{newStaff.status}')
ON DUPLICATE KEY UPDATE
    staffID = VALUES(staffID),
    fName = VALUES(fName),
    lName = VALUES(lName),
    email = VALUES(email),
    password = VALUES(password),
    status = VALUES(status);"""
    dbcursor.execute(sql)
    db.commit()


def create_new_staff():
    newStaff = PersonInfo("", "", "", "", "", "")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Please Insert New Staff Information")
    print("(First Name, Last Name, Email, Password)")
    input("(Press ENTER to continue)")
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Please Insert New Staff Information")
        print("(ENTER '-1' to Back)")
        isReturn = False
        newStaff.fName = input("Frist Name: ")
        if newStaff.fName == "-1" and len(newStaff.fName) == 2:
            isReturn = True
            break
        newStaff.lName = input("Last Name: ")
        if newStaff.lName == "-1" and len(newStaff.lName) == 2:
            isReturn = True
            break
        newStaff.email = input("Email: ")
        if newStaff.email == "-1" and len(newStaff.email) == 2:
            isReturn = True
            break
        newStaff.password = input("Password: ")
        if newStaff.password == "-1" and len(newStaff.password) == 2:
            isReturn = True
            break
        isBreak = True
        if len(newStaff.fName) == 0:
            isBreak = False
            print("!!!Frist Name CANNOT be BLANK!!!")
        if len(newStaff.lName) == 0:
            isBreak = False
            print("!!!Last Name CANNOT be BLANK!!!")
        if len(newStaff.email) == 0:
            isBreak = False
            print("!!!Email CANNOT be BLANK!!!")
        if len(newStaff.password) == 0:
            isBreak = False
            print("!!!Password CANNOT be BLANK!!!")
        if isBreak:
            break
        input("(Press ENTER to RE-ENTER)")
    if isReturn:
        return
    newStaff.status = "Active"
    sql = "SELECT MAX(staffID) FROM Staff;"
    result = fetchone_from_MySQL(sql)
    latestStaffIDnumber = result[0]
    newStaff.ID = "ST"+str(int(latestStaffIDnumber[-3:])+1).zfill(3)

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("New Staff Information")
    display_staff_info(newStaff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            insert_new_staff_SQL(newStaff)
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("New Staff Information")
            display_staff_info(newStaff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(NO) Cancel: ")
######

# Edit Staff


def display_edit_staff_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Edit Staff Menu")
    print("1. Search Staff by Email to EDIT")
    print("2. Search Staff by Name to EDIT")
    print("3. Enter StaffID to EDIT")
    print("(Enter '-1' to BACK)")


def update_staff_to_MySQL(staff):
    update_one_attribute_SQL(
        staff.fName, "fName", "staff", "staffID", staff.ID)
    update_one_attribute_SQL(
        staff.lName, "lName", "staff", "staffID", staff.ID)
    update_one_attribute_SQL(
        staff.email, "email", "staff", "staffID", staff.ID)


def search_staff_by_email_to_edit():
    email = "-1"
    staffID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        email = input("Search Staff Email: ")
        if email == "-1" and len(email) == 2:
            break
        display_search_staff_by_email(email)
        print("Press ENTER if you want to search again")

        staffID = input("ENTER StaffID you want to EDIT: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    if (email == "-1" and len(email) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Staff Information")
    display_staff_info(staff)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        staff.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        staff.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        staff.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_staff_to_MySQL(staff)
            print("Update Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Staff Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def search_staff_by_name_to_edit():
    name = "-1"
    staffID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        name = input("Search Staff Name: ")
        if name == "-1" and len(name) == 2:
            break
        display_search_staff_by_name(name)
        print("Press ENTER if you want to search again")

        staffID = input("ENTER StaffID you want to EDIT: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    if (name == "-1" and len(name) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Staff Information")
    display_staff_info(staff)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        staff.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        staff.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        staff.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_staff_to_MySQL(staff)
            print("Update Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Staff Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_staff_by_ID():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        staffID = input("ENTER StaffID you want to EDIT: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Staff Information")
    display_staff_info(staff)
    input("(Press ENTER to continue)")
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("(Leave BLANK if you to keep the same data)")
    newFName = input("ENTER New Frist Name: ")
    if not len(newFName) == 0:
        staff.fName = newFName
    newLName = input("ENTER New Last Name: ")
    if not len(newLName) == 0:
        staff.lName = newLName
    newEmail = input("ENTER New Email: ")
    if not len(newEmail) == 0:
        staff.email = newEmail

    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Update Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_staff_to_MySQL(staff)
            print("Update Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Update Staff Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def edit_staff():
    while True:
        display_edit_staff_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_staff_by_email_to_edit()
                    break
                if choice == "2":
                    search_staff_by_name_to_edit()
                    break
                if choice == "3":
                    edit_staff_by_ID()
                    break
            else:
                display_edit_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
######

# Delete Staff


def display_delete_staff_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delet Staff Menu")
    print("1. Search Staff by Email to Delete")
    print("2. Search Staff by Name to Delete")
    print("3. Enter StaffID to Delete")
    print("(Enter '-1' to BACK)")


def display_staff_info(staff):
    print(f"""StaffID: {staff.ID}
Name: {staff.fName} {staff.lName}
Email: {staff.email}""")


def search_staff_by_email_to_delete():
    email = "-1"
    staffID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        email = input("Search Staff Email: ")
        if email == "-1" and len(email) == 2:
            break
        display_search_staff_by_email(email)
        print("Press ENTER if you want to search again")

        staffID = input("ENTER StaffID you want to DELETE: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    if (email == "-1" and len(email) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    if staff.status == "Disabled":
        print("Staff has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "Staff", "staffID", staff.ID)
            print("Delete Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def search_staff_by_name_to_delete():
    name = "-1"
    staffID = "-1"
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        # Input bookTitle
        name = input("Search Staff Name: ")
        if name == "-1" and len(name) == 2:
            break
        display_search_staff_by_name(name)
        print("Press ENTER if you want to search again")

        staffID = input("ENTER StaffID you want to DELETE: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    if (name == "-1" and len(name) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    if staff.status == "Disabled":
        print("Staff has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "Staff", "staffID", staff.ID)
            print("Delete Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_staff_by_ID():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("(Enter '-1' to BACK)")
        staffID = input("ENTER StaffID you want to DELETE: ")
        if ("ST000" <= staffID <= "ST999" and len(staffID) == 5 and check_duplicate_SQL(staffID, "staffID", "Staff")) or (staffID == "-1" and len(staffID) == 2):
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("The StaffID NOT EXIST or IS INVALID")
            input("(Press ENTER to RE-ENTER)")
    if (staffID == "-1" and len(staffID) == 2):
        return
    result = search_using_exact_keywords_MySQL(staffID, "staffID", "Staff")
    staff = PersonInfo(result[0], result[1], result[2],
                       result[3], result[4], result[5])

    if staff.status == "Disabled":
        print("Staff has been already Deleted")
        input("(Press ENTER to Back)")
        return
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Delete Staff Information")
    display_staff_info(staff)
    choice = input(
        "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")
    while True:
        choice = choice.upper()
        if choice == "Y" and len(choice) == 1:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            update_one_attribute_SQL(
                "Disabled", "status", "Staff", "staffID", staff.ID)
            print("Delete Staff Successful")
            input("(Press Enter to continue)")
            break
        if choice == "N" and len(choice) == 1:
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
            print("Delete Book Information")
            display_staff_info(staff)
            print("!!!You Have Enter INVALID Value!!!")
            choice = input(
                "Please Enter 'Y'(Yes) to Confirm or 'N'(No) Cancel: ")


def delete_staff():
    while True:
        display_delete_staff_menu()
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_staff_by_email_to_delete()
                    break
                if choice == "2":
                    search_staff_by_name_to_delete()
                    break
                if choice == "3":
                    delete_staff_by_ID()
                    break
            else:
                display_delete_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
######


def manage_staff():
    while True:
        display_manage_staff_menu()
        choice = input("ENTER your action: ")
        while True:
            if choice == "-1" and len(choice) == 2:
                break
            if choice == "1" and len(choice) == 1:
                search_staff()
                break
            if choice == "2" and len(choice) == 1:
                create_new_staff()
                break
            if choice == "3" and len(choice) == 1:
                edit_staff()
                break
            if choice == "4" and len(choice) == 1:
                delete_staff()
                break
            else:
                display_manage_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
###

# Gennerate Report


def generate_report():
    sql = ("""SELECT 
    (SELECT COUNT(*) FROM Book WHERE availability = 'Available') AS num_available_books,
    (SELECT COUNT(*) FROM Book WHERE availability = 'On Loan') AS num_on_loan_books,
    (SELECT COUNT(*) FROM `Order` WHERE status = 'On Loan') AS num_on_loan_orders,
    (SELECT COUNT(*) FROM `Order` WHERE status = 'Overdue') AS num_overdue_orders,
    (SELECT COUNT(*) FROM Member WHERE status = 'Active') AS num_current_members,
    (SELECT COUNT(*) FROM Staff WHERE status = 'Active') AS num_current_staff
;""")
    result = fetchone_from_MySQL(sql)
    amountOfAvailableBooks = result[0]
    amountOfOnLoanBooks = result[1]
    amountOfCurrentOnLoanOrder = result[2]
    amountOfCurrentOverdueOrder = result[3]
    amountOfCurrentMember = result[4]
    amountOfCurrentStaff = result[5]
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"""****CodeX Library Report****
Time: {datetime.now()}
Total Amount of Availabile Books: {amountOfAvailableBooks}
Total Amount of On Loan Books: {amountOfOnLoanBooks}
Total Amount of Current On Loan Order: {amountOfCurrentOnLoanOrder}
Total Amount of Current Overdue Order: {amountOfCurrentOverdueOrder}
Total Current Member: {amountOfCurrentMember}
Total Current Staff: {amountOfCurrentStaff}
****Staff Order****""")
    sql = "SELECT staffID, fName, lName from Staff Where status = 'Active'"
    staffresults = fetchall_from_MySQL(sql)
    for staff in staffresults:
        sql = f"""SELECT count(*) as orderCount
From `Order`
WHERE staffID = '{staff[0]}' AND rentDate LIKE  '{date.today()}%';"""
        totalOrder = fetchone_from_MySQL(sql)
        print(
            f"ID: {staff[0]} Name: {staff[1]} {staff[2]} ||| Total Order: {totalOrder[0]}")
    input("(Press ENTER to Back)")
###

# UI


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
                manage_staff()
                break
            if choice == "5" and len(choice) == 1:
                generate_report()
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
###

# MAIN


connect_to_database()
update_order_status_SQL()
while True:
    login_UI()
    if title == "Member":
        member_UI()
    if title == "Staff":
        staff_UI()
    if title == "Admin":
        admin_UI()
