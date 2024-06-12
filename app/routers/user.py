from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.user import create_user_crud, create_driver_crud
from app.db.database import get_db
from app.models.user import User, Role
from app.schemas.user import UserSchemaFull, UserCreateData, DriverCreateData

router = APIRouter(tags=["users"])


@router.post("/driver/create", response_model=UserSchemaFull)
async def create_driver(user: get_us, driver_data: DriverCreateData, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Создавать пользователей может только администратор")
    user = create_user_crud(session, driver_data)
    create_driver_crud(session, user, driver_data)
    return user
