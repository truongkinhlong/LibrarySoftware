import os


os.system("cls" if os.name == "nt" else "clear")


def open_window():
    # Clear the screen
    #os.system("cls" if os.name == "nt" else "clear")

    print("Welcome to CodeX Library \n")
    print("Choose your login as: \n")
    print("1. Member\n")
    print("2. Staff\n")
    print("3. Admin\n")
    choice = input("Please enter your choice: ")


open_window()
