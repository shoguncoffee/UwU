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
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    raise HTTPException(status_code=404, detail="Account not found")