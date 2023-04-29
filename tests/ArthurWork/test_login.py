class Account:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self, input_username: str, input_password: str):
        if self.username == input_username:
            if self.password == input_password:
                print("Login successful!")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Incorrect username.")
            return False

    @classmethod
    def register(cls, username: str, password: str):
        print("register method called")
        # Create a new Account instance with the given username and password
        new_account = cls(username, password)
        print(f"New account created: {new_account}")
        return new_account