import tkinter as tk
import requests

API_EndPoint1 = "http://127.0.0.1:8000/account/create"
API_EndPoint2 = "http://127.0.0.1:8000/account/login"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.phone_label = tk.Label(self, text="Phone:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        self.create_account_button = tk.Button(self, text="Create Account", command=self.create_account)
        self.create_account_button.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.master.quit)
        self.quit_button.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        response = requests.post(API_EndPoint1, params={"username": username, "password": password, "email": email, "phone": phone})
        if response.status_code == 200:
            self.status_label.config(text="New account created!")
        else:
            self.status_label.config(text="Error creating account")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = requests.post(API_EndPoint2, params={"username": username, "password": password})
        if response.status_code == 200:
            self.status_label.config(text="Login successful!")
        else:
            self.status_label.config(text="Incorrect username or password")

root = tk.Tk()
app = Application(master=root)
app.mainloop()