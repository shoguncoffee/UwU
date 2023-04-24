from ..base import *

router = APIRouter(
    prefix='/account',
    tags=["registor"],
)

@router.post("/createAccount")
def create_account(username: str, password: str, email: str, phone: str):
    account = src.Customer(username, password, email, phone)
    if Airline.register(account):
        return {"message": "New account created!", "account": account.username}