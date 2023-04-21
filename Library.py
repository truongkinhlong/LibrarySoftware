import os
import mysql.connector
#########################################################
# Function
#########################################################


def front_window():
    print("Welcome to CodeX Library \n")
    print("Choose your login as: \n")
    print("1. Member\n")
    print("2. Staff\n")
    print("3. Admin\n")
    while (True):
        choice = input("Please enter your choice: ")
        if ('1' <= choice <= '3'):
            break
    return int(choice)


def login_UI(choice: str):
    os.system("cls" if os.name == "nt" else "clear")  # CLEAR SCREEN

    print("Please enter E-Mail and Password to login\n")
    email = input("E-Mail: ")
    password = input("Password: ")

    # return (valid, choice)


#########################################################
# MAIN
#########################################################
temp = front_window()
login_UI(temp)
