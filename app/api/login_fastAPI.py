from .base import *
from typing import Dict

router = APIRouter(
    prefix='/account',
    tags=["login"],
)

@router.post("/create")
def create_account(username: str, password: str, email: str, phone: str):
    account = Account(username, password, email, phone)
    if Airline.register(account):
        return {"message": "New account created!", "account": account.username}
        
@router.post("/login")
def login_account(username: str, password: str):
    if username in Airline.accounts:
        if Airline.login(username, password):
            return {"message": "Login successful!"}
        
        return {"message": "Incorrect username or password"}
        #raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"message": "Account not found"}
    #raise HTTPException(status_code=404, detail="Account not found")