import tkinter as tk
import requests

API_EndPoint1 = "http://127.0.0.1:8000/account/createAccount"
API_EndPoint2 = "http://127.0.0.1:8000/account/login"

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        self.master.geometry("300x150")

        # Create labels and entries for user input
        self.username_label = tk.Label(master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        # Create a button to submit the form
        self.submit_button = tk.Button(master, text="Login", command=self.submit_form)
        self.submit_button.pack()

        # Create a button to go to the registration window
        self.register_button = tk.Button(master, text="Register", command=self.open_registration)
        self.register_button.pack()

        # Create a label for the response message
        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

    def submit_form(self):
        # Get input values from the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Send a POST request to the server to login
        url = API_EndPoint2
        data = {"username": username, "password": password}
        response = requests.post(url, params=data)

        # Show the response message to the user
        if response.status_code == 200:
            self.response_label.config(text="Login successful!", fg="green")
        else:
            self.response_label.config(text="Error: " + response.json()["detail"], fg="red")

    def open_registration(self):
        # Close the login window
        self.master.destroy()

        # Open the registration window
        root = tk.Tk()
        registration_window = RegistrationWindow(root)
        root.mainloop()

class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        master.title("Register")
        self.master.geometry("300x250")

        # Create labels and entries for user input
        self.username_label = tk.Label(master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.email_label = tk.Label(master, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(master)
        self.email_entry.pack()

        self.phone_label = tk.Label(master, text="Phone")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(master)
        self.phone_entry.pack()

        # Create a button to submit the form
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_form)
        self.submit_button.pack()

        # Create a button to go back to the login window
        self.login_button = tk.Button(master, text="Back to Login", command=self.go_to_login)
        self.login_button.pack()

        # Create a label for the response message
        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

    def submit_form(self):
        # Get input values from the user
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        # Send a POST request to the server to create a new account
        data = {"username": username, "password": password, "email": email, "phone": phone}
        response = requests.post(API_EndPoint1, params=data)

        # Show the response message to the user
        if response.status_code == 200:
            self.response_label.config(text="New account created!", fg="green")
        else:
            self.response_label.config(text="Error: " + response.json()["detail"], fg="red")

        self.response_label.pack()

    def go_to_login(self):
        # Close the registration window
        self.master.destroy()
        
        # Open the login window
        root = tk.Tk()
        login_window = LoginWindow(root)
        root.mainloop() 

root = tk.Tk()
login_window = LoginWindow(root)
root.mainloop()