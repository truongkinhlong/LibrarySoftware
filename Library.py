import os
import mysql.connector

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
    def __init__(self, ID, fName, lName, email, password):
        self.ID = ID
        self.fName = fName
        self.lName = lName
        self.email = email
        self.password = password


class Book:
    def __int__(self, isbn, title, author, publisher, availability, shelf):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.availability = availability
        self.shelf = shelf

################################################################
# Function
################################################################
# Database Function


# return dbcursor.fetchall()
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
                            result[2], result[3], result[4])
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
def search_book_by_title():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    # Input bookTitle
    bookTitle = input("Search book title: ")

    results = search_using_keywords_MySQL(bookTitle, "title", "book")
    if len(results) > 0:
        for book in results:
            print(book)
        input("Press ENTER to back to Search MENU")
    else:
        print("No books found with title:", bookTitle)
        input("Press ENTER to back to Search MENU")


def search_book_by_isbn():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    # Input ISBN
    isbn = input("Search book ISBN: ")

    # Fetch the result of the query
    results = search_using_keywords_MySQL(isbn, "isbn", "Book")
    if len(results) > 0:
        for book in results:
            print(book)
        input("Press ENTER to back to Search MENU")

    else:
        print("No books found with ISBN:", isbn)
        input("Press ENTER to back to Search MENU")


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
                    search_book_by_title()
                    break
                if choice == "2":
                    search_book_by_isbn()
                    break
            else:
                display_search_book_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
            break
###################################################################################################


# view_your_Order Menu
###################################################################################################
def display_view_order_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    results = search_using_keywords_MySQL_selective_attribute(
        person.ID, "memberID", "`order`", "orderID, isbn, status")
    if len(results) > 0:
        for order in results:
            print(order)

    else:
        print("No orders found")

    print("Enter orderID to view detail")
    print("(Enter '-1' to LOG OUT)")


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
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"""OrderID: {order.orderID} Status: {order.status}
StaffID: {order.staffID}  Name: {order.staffFName} {order.staffLName}
MemberID: {order.memberID} Name: {order.memberFName} {order.memberLName}
Book ISBN: {order.bookIsbn}
Book Title: {order.bookTitle}
Book Author: {order.bookAuthor}
Rent Date: {order.rentDate}       Due Date: {order.dueDate}
Return Date: {order.returnDate}""")
    input("(Press ENTER to return)")


def view_your_order():
    while True:
        display_view_order_menu()

        # Make Choice
        choice = input("ENTER orderID: ")
        while (True):
            if ("000000" <= choice <= "999999" and len(choice) == 6) or choice == "-1":
                if choice == "-1":
                    break
                else:
                    view_order_detail(choice)
                    break
            else:
                # CLEAR SCREEN
                display_view_order_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER OrderID: ")
        if choice == "-1":
            break


###################################################################################################
# edit_personal_information menu()
###################################################################################################
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

###################################################################################################


def display_manage_book_menu():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("""Manage Book Menu
1. Insert New Book
2. Update Book
3. Delete Book
(ENTER '-1' to Back)""")


def display_new_book_info(newBook):
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print(f"""New Book Information
ISBN: {newBook.isbn}
Title: {newBook.title}
Author: {newBook.author}
Publisher: {newBook.publisher}
Shelf: {newBook.shelf}""")


def insert_new_book():
    newBook = Book()
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("Please Insert New Book Information")
        print("(ISBN, Title, Author, Publisher, Shelf)")
        newBook.isbn = input("ISBN: ")
        newBook.title = input("Title: ")
        newBook.author = input("Author: ")
        newBook.publisher = input("Publisher: ")
        newBook.availability = "Available"
        newBook.shelf = input("Shelf: ")
        while True:


def manage_book():
    while True:
        display_manage_book_menu()
        choice = input("ENTER your action: ")
        if choice == "-1" and len(choice) == 2:
            break
        if choice == "1" and len(choice) == 1:
            insert_new_book()
            break
        if choice == "2" and len(choice) == 1:
            update_book()
            break
        if choice == "3" and len(choice) == 1:
            delete_book()
            break
        else:
            display_manage_book_menu()
            print("!!!You Have Enter INVALID Value!!!")
            choice = input("ENTER your action: ")

    ###################################################################################################


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

            if choice == "4" and len(choice) == 1:
                edit_personal_information()
                break
            else:
                display_staff_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("ENTER your action: ")
        if choice == "-1":
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
