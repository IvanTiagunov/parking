from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.auth import get_user_by_username_and_password, get_us
from app.db.database import get_db

router = APIRouter()


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Авторизация"""
    user = get_user_by_username_and_password(form_data.username, form_data.password)
    token = str(user.token_value)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", tags=['get_info'])
async def read_user_me(user: get_us):
    """Получение текущего пользователя"""
    return user