from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.user import create_user_crud, create_driver_crud, create_mechanic_crud, deactivate_user_crud, \
    get_list_users_crud, update_driver_crud, update_user_crud, check_user_not_exist, get_user_by_id_crud
from app.db.database import get_db
from app.dependencies import check_rights
from app.enums import Role
from app.schemas.user import DriverCreateData, MechanicCreateData, AdminCreateData, DriverUpdateData, UserUpdateFields, \
    DriverCreateResponseData, UserFromDB, UserSchemaFull

router = APIRouter()


@router.post("/admin/create", response_model=AdminCreateData, tags=['create'])
async def create_admin(user: get_us, admin: AdminCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать администраторов может только администратор")
    user = create_user_crud(session, admin)
    return user


@router.post("/driver/create", tags=['create'])
async def create_driver(user: get_us, driver_data: DriverCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать водителей может только администратор")
    user = create_user_crud(session, driver_data)
    driver = create_driver_crud(session, user, driver_data)
    return user, driver


@router.post("/mechanic/create", tags=['create'])
async def create_mechanic(user: get_us, mechanic_data: MechanicCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать механиков может только администратор")
    user = create_user_crud(session, mechanic_data)
    mechanic = create_mechanic_crud(session, user)
    return mechanic


@router.post("/user/deactivate")
async def deactivate_user(user: get_us, user_login_to_deactivate: str, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Деактивировать пользователей может только администратор")
    deactivate_user_crud(session, user_login_to_deactivate)
    return {"Успешно деактивирован пользователь с логином": {user_login_to_deactivate}}


@router.get("/user/get_list", tags=['get_info'])
async def get_user_list(user: get_us, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Получить список пользователей может только администратор")
    all_users = get_list_users_crud(session)
    return all_users


@router.get("/user/get_by_id", response_model=UserFromDB, tags=['get_info'])
async def get_user_by_id(user: get_us, user_id, session: Session = Depends(get_db)):
    user_from_db = get_user_by_id_crud(session, user_id)
    return user_from_db


@router.post("/user/update", tags=['update'], response_model=UserSchemaFull)
async def update_user_data(user: get_us, user_fields: UserUpdateFields, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Обновить данные пользователя может только администратор")
    new_user = update_user_crud(session, user_fields)
    return new_user


@router.post("/driver/update", tags=['update'])
async def update_driver_car_access_type(user: get_us, driver_fields: DriverUpdateData,
                                        session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin],
                 error_msg="Обновить тип доступа к машинам у водителя может только администратор")
    driver_rights = update_driver_crud(session, driver_fields)
    return {f"Обновлены права водителя {driver_fields.username}": driver_rights}
