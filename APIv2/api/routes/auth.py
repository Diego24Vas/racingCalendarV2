from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import login_for_access_token, get_current_user

router = APIRouter()

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_for_access_token(form_data)

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
