from tkinter import *
import tkinter.messagebox as tmsg

def login():
    username = user_entry.get()
    password = pass_entry.get()
    if username == "admin" and password == "1234":
        tmsg.showinfo("Success", "Logged in successfully")
    else:
        tmsg.showerror("Error", "Invalid credentials")

root = Tk()
root.geometry("500x300")
root.title("Login Window")

user_label = Label(root, text="Username")
user_label.pack()

user_entry = Entry(root)
user_entry.pack()

pass_label = Label(root, text="Password")
pass_label.pack()

pass_entry = Entry(root)
pass_entry.pack()

login_button = Button(root, text="Login", command=login)
login_button.pack()

root.mainloop()
