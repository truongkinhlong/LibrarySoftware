import os
import mysql.connector


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
                choice = input("RE-ENTER your action: ")
        if choice == "-1":
            break
###################################################################################################


# view_your_Order Menu
###################################################################################################
def view_your_Order():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
        print("View Menu:")
        print("1. ")
        print("2. ")
        print("3. ")
        print("(Enter '-1' to LOG OUT)")

        # Make Choice
        choice = input("ENTER your action: ")
        while (True):
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_book()
                    break
                if choice == "2":
                    view_your_Order()
                    break
            else:
                # CLEAR SCREEN
                os.system("cls" if os.name == "nt" else "clear")

                print("View Order Menu:")
                print("1. ")
                print("2. ")
                print("3. ")
                print("(Enter '-1' to LOG OUT)")
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("RE-ENTER your action: ")
        if choice == "-1":
            break


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
            if ("1" <= choice <= "3" and len(choice) == 1) or choice == "-1":
                if choice == "-1":
                    break
                if choice == "1":
                    search_book()
                    break
                if choice == "2":
                    view_your_Order()
                    break
            else:
                display_member_menu()
                print("!!!You Have Enter INVALID Value!!!")
                choice = input("RE-ENTER your action: ")
        if choice == "-1":
            break


connect_to_database()
member_UI()
