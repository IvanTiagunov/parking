from typing import Union
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing_extensions import Annotated

from app.enums import Role


def generate_uuid():
    return str(uuid4())

def check_active(user):
    if not user.is_active:
        raise HTTPException(status_code=401,
                             detail=f"Недостаточно прав. Пользователь деактивирован")
def check_admin(user, error_msg):
    if user.role_name != Role.admin:
        raise HTTPException(status_code=401,
                             detail=f"Недостаточно прав. {error_msg}")
    check_active(user)