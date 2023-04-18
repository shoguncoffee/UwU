import tkinter as tk
import requests

API_EndPoint1 = "http://127.0.0.1:8000/account"
API_EndPoint2 = "http://127.0.0.1:8000/account/login"

class AccountGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Account Manager")
        self.grid()
        
        self.create_widgets()

    def create_widgets(self):
        # Create username and password entry fields
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        # Create buttons for creating an account and logging in
        self.create_account_button = tk.Button(self, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=2, column=0)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1)

        # Create text box for displaying messages
        self.message_box = tk.Text(self, height=5, width=30)
        self.message_box.grid(row=3, column=0, columnspan=2)

    def create_account(self):
        # Get the username and password from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate the input fields
        if not username:
            self.message_box.delete(1.0, tk.END)
            self.message_box.insert(tk.END, "Please enter a username.")
            return
        if not password:
            self.message_box.delete(1.0, tk.END)
            self.message_box.insert(tk.END, "Please enter a password.")
            return

        # Send a POST request to the FastAPI API to create a new account
        response = requests.post(API_EndPoint1, params={"username": username, "password": password})

        # Display the response message in the message box
        self.message_box.delete(1.0, tk.END)
        if "message" in response.json():
            self.message_box.insert(tk.END, response.json()["message"])
        else:
            self.message_box.insert(tk.END, "Unknown error")

    def login(self):
        # Send a POST request to the FastAPI API to log in to an existing account
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = requests.post(API_EndPoint2, params={"username": username, "password": password})

        # Display the response message in the message box
        self.message_box.delete(1.0, tk.END)
        if "message" in response.json():
            self.message_box.insert(tk.END, response.json()["message"])
        else:
            self.message_box.insert(tk.END, "Unknown error")

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountGUI(root)
    app.mainloop()