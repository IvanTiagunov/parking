from typing import Annotated
from uuid import uuid4

from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import status

from app.db.database import get_db, SessionLocal
from app.models.user import User
from app.schemas.user import UserSchemaFull

# Todo создание пользователя
# def create_user_crud(client, token_type, session: Session):
#     token_value = generate_uuid()
#     token = Tokens(type=token_type,
#                    value=token_value,
#                    parent_id=client.token_id)
#     session.add(token)
#     session.commit()
#     session.refresh(token)
#     return token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session, token: str):
    """Получение пользователя по токену"""
    get_user_query = select(User).where(User.token_value == token)
    user_from_table = session.scalar(get_user_query)
    if not user_from_table:
        raise HTTPException(status_code=401, detail="Пользовать не авторизирован или отсутствует")

    if not user_from_table.is_active:
        raise HTTPException(status_code=404, detail="Пользователь заблокирован. Обратитесь к администратору")
    return user_from_table


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    """Возвращение текущего пользователя"""
    user = get_user(session, token)
    return user

get_us = Annotated[UserSchemaFull, Depends(get_current_user)]

def get_user_by_username_and_password(username, password):
    """Получение токена по логину и паролю"""
    # ищем по имени
    # проверяем пароль
    # возвращаем токен
    session = SessionLocal()
    get_user = select(User).where(User.username == username)
    user_from_table = session.scalar(get_user)
    if user_from_table == None:
        return HTTPException(status_code=400, detail="Неверное имя пользователя")
    if user_from_table.password != str(password):
        return HTTPException(status_code=400, detail="Неверный пароль")
    return user_from_table



