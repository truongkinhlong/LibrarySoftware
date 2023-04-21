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


def search_book_by_title():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    # Input bookTitle
    bookTitle = input("Search book title: ")

    # Extract keywords from bookTitle
    keywordsFromTitle = bookTitle.split(" ")

    # Build SQL to search
    sql = "SELECT * FROM book WHERE "
    for i in range(len(keywordsFromTitle)):
        if i == 0:
            sql += "title LIKE '%" + keywordsFromTitle[i] + "%'"
        else:
            sql += " OR title LIKE '%" + keywordsFromTitle[i] + "%'"

    # Execute the SQL
    dbcursor.execute(sql)

    results = dbcursor.fetchall()
    if len(results) > 0:
        for book in results:
            print(book)
    else:
        print("No books found with title:", bookTitle)
    # def search_book_by_isbn():


def search_book():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN
    print("Search book by: ")
    print("1. Title")
    print("2. ISBN")
    choice = input("ENTER your action: ")
    while (True):
        if ("1" <= choice <= "2" and len(choice) == 1):
            if choice == "1":
                search_book_by_title()
                break
            # if choice == "2":
            # search_book_by_isbn()
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

            print("Search book by: ")
            print("1. Title")
            print("2. ISBN")
            print("!!!You Have Enter INVALID Value!!!")
            choice = input("RE-ENTER your action: ")


def member_UI():
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    print("Member Menu:")
    print("1. Search Book")
    print("2. View Your Order")
    print("3. Edit Personal Information")

    # Make Choice
    choice = input("ENTER your action: ")
    while (True):
        if ("1" <= choice <= "3" and len(choice) == 1):
            if choice == "1":
                search_book()
                break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

            print("You Have Enter INVALID Value!")
            print("Member Menu:")
            print("1. Search Book")
            print("2. View Your Order")
            print("3. Edit Personal Information")
            choice = input("RE-ENTER your action: ")


connect_to_database()
member_UI()
