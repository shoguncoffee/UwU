import pickle
from dataclasses import dataclass

# Define the Account class
@dataclass
class Account:
    username: str
    password: str

    def login(self, input_username, input_password):
        if self.username == input_username:
            if self.password == input_password:
                print("Login successful!")
                return True
            else:
                print("Incorrect username or password.")
                return False

    @classmethod
    def register(cls, username, password):
        # Create a new Account instance with the given username and password
        new_account = cls(username, password)
        print(f"New account created: {new_account}")
        return new_account

# Load the users list from a file, if it exists
try:
    with open("app/src/ArthurWork/users.txt", "rb") as f:
        users = pickle.load(f)
        print(users)
except FileNotFoundError:
    users = []

# Prompt user to enter their username and password
input_username = input("Enter your username: ")
input_password = input("Enter your password: ")

# Check if the username and password match a valid user
for user in users:
    if user.login(input_username, input_password) is not None:
        break  # Exit the loop after the first successful login

else:
    # If no match found, prompt user to register
    print("Account not found.")
    register_choice = input("Would you like to register an account? (y/n) ")
    if register_choice.lower() == "y":
        while True:
            new_username = input("Enter a username: ")
            new_password = input("Enter a password: ")
            # Check if the username is already taken
            if new_username in (user.username for user in users):
                # Username already exists, try again
                print("Username already exists. Please choose another.")
                continue
            
            # Check if user don't input new password
            if len(new_password) < 8:
                print("Your Password is too short enter new password atleast 8 characters.")
                continue
            else:
                # Username is available, add new account and break loop
                new_account = Account.register(new_username, new_password)
                users.append(new_account)
                print("Account registered.")
                break
    else:
        print("Login failed. Goodbye.")

# Save the users list to a file
with open("app/src/ArthurWork/users.txt", "wb") as f:
    pickle.dump(users, f)