import tkinter as tk
import requests

class App:
    def __init__(self, master):
        self.master = master
        master.title("Airline App")

        # Create labels and entry field for username input
        self.username_label = tk.Label(master, text="Enter your username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create buttons for retrieving account info and bookings
        self.account_button = tk.Button(master, text="Get Account Info", command=self.get_account_info, bg="#4CAF50", fg="white")
        self.account_button.grid(row=1, column=0, padx=10, pady=10)
        self.bookings_button = tk.Button(master, text="Get Bookings", command=self.get_bookings, bg="#2196F3", fg="white")
        self.bookings_button.grid(row=1, column=1, padx=10, pady=10)

        # Create text box for displaying account info and bookings
        self.text_box = tk.Text(master, height=10, width=50, padx=10, pady=10)
        self.text_box.grid(row=2, column=0, columnspan=2)

    def get_account_info(self):
        # Get username input from user
        username = self.username_entry.get()

        # Make GET request to API endpoint for account info
        response = requests.get(f"http://127.0.0.1:8000/account/{username}/my-account")

        # Update text box with account info
        if response.status_code == 200:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, response.json(), "bold")
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, response.json()["detail"], "bold")

    def get_bookings(self):
        # Get username input from user
        username = self.username_entry.get()

        # Make GET request to API endpoint for bookings
        response = requests.get(f"http://127.0.0.1:8000/account/{username}/my-bookings")

        # Update text box with bookings
        if response.status_code == 200:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, response.json(), "bold")
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, response.json()["detail"], "bold")

        # Set the text style to bold
        self.text_box.tag_configure("bold", font=("Helvetica", 10, "bold"))

root = tk.Tk()
app = App(root)
root.mainloop()