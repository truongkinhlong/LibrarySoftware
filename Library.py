import os
import mysql.connector

################################################################
# Function
################################################################


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

            print("You Have Enter INVALID Value!")
            print("Choose your login as:")
            print("1. Member")
            print("2. Staff")
            print("3. Admin")
            choice = input("Please RE-ENTER your choice: ")

    # Assign tittle
    global title
    if choice == "1":
        title = "Member"
    if choice == "2":
        title = "Staff"
    if choice == "3":
        title = "Admin"


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


def check_login(email, password):  # RETURN True or False

    # Execute the SELECT query to check if the email and password combination exists
    sql = f"SELECT * FROM {title} WHERE email = %s AND password = %s"

    #parameters = (email, password)
    parameters = (email, password)
    dbcursor.execute(sql, parameters)

    # Fetch the result of the query
    result = dbcursor.fetchone()

    # Check if the result is not None (i.e., the email and password combination exists)
    if result is not None:
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
            print(f"Please Re-Enter E-Mail and Password to login as {title}")
            email = input("E-Mail: ")
            password = input("Password: ")
################################################################

# Member UI & Function
################################################################


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
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

            print("You Have Enter INVALID Value!")
            print("Member Menu:")
            print("1. Search Book")
            print("2. View Your Order")
            print("3. Edit Personal Information")
            choice = input("RE-ENTER your action: ")
################################################################


# MAIN
connect_to_database()
welcome_window()
login_UI()
if title == "Member":
    member_UI()
# if title == "Staff":
    # staff_UI()
# if title == "Admin":
    # admin_UI()
