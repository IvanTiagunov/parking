from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.user import create_user_crud, create_driver_crud, create_mechanic_crud, deactivate_user_crud, \
    get_list_users_crud
from app.db.database import get_db
from app.enums import Role
from app.schemas.user import DriverCreateData, MechanicCreateData, AdminCreateData

router = APIRouter(tags=["users"])


@router.post("/admin/create", response_model=AdminCreateData)
async def create_admin(user: get_us, admin: AdminCreateData, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Создавать администраторов может только администратор")
    user = create_user_crud(session, admin)
    return user


@router.post("/driver/create", response_model=DriverCreateData)
async def create_driver(user: get_us, driver_data: DriverCreateData, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Создавать водителей может только администратор")
    user = create_user_crud(session, driver_data)
    driver = create_driver_crud(session, user, driver_data)
    return driver


@router.post("/mechanic/create", response_model=MechanicCreateData)
async def create_mechanic(user: get_us, mechanic_data: MechanicCreateData, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Создавать механиков может только администратор")
    user = create_user_crud(session, mechanic_data)
    mechanic = create_mechanic_crud(session, user)
    return mechanic



@router.post("/user/deactivate")
async def deactivate_user(user: get_us, user_login_to_deactivate:str, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Деактивировать пользователей может только администратор")
    user = deactivate_user_crud(session, user_login_to_deactivate)
    return {"Пользователь успешно деактивирован":{user}}


@router.get("/user/get_list")
async def deactivate_user(user: get_us, session: Session = Depends(get_db)):
    if user.role_name != Role.admin:
        return HTTPException(status_code=401,
                             detail="Недостаточно прав. Получить список пользователей может только администратор")
    all_users = get_list_users_crud(session)
    return all_users