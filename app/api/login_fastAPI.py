from fastapi import FastAPI
from app.src.ArthurWork.test_login import Account
from typing import Dict

app = FastAPI()

accounts: Dict[str, Account] = {}

@app.post("/account")
def create_account(username: str, password: str):
    account = Account.register(username, password)
    accounts[username] = account
    return {"message": "New account created!", "account": account.__dict__}

@app.get("/accounts")
def get_accounts():
    return {"accounts": [account.__dict__ for account in accounts.values()]}

@app.post("/account/login")
def login_account(username: str, password: str):
    if username in accounts:
        account = accounts[username]
        if account.login(username, password):
            return {"message": "Login successful!"}
        else:
            return {"message": "Incorrect username or password"}
            #raise HTTPException(status_code=401, detail="Incorrect username or password")
    else:
        return {"message": "Account not found"}
        #raise HTTPException(status_code=404, detail="Account not found")