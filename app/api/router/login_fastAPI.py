from .base import *

router = APIRouter(
    prefix='/account',
    tags=["login"],
)
        
@router.post("/login")
def login_account(username: str, password: str):
    if username in system.accounts:
        if system.login(username, password):
            return {"message": "Login successful!"}
        else:
            raise HTTPException(401, "Incorrect username or password")
        
    raise HTTPException(404, "Account not found")