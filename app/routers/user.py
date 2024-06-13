from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.user import create_user_crud, create_driver_crud, create_mechanic_crud, deactivate_user_crud, \
    get_list_users_crud, update_driver_crud, update_user_crud, check_user_not_exist, get_user_by_id_crud, \
    get_user_by_login_crud, get_driver_by_user_login
from app.db.database import get_db
from app.dependencies import check_rights
from app.enums import Role
from app.schemas.user import DriverCreateData, MechanicCreateData, AdminCreateData, DriverUpdateData, UserUpdateFields, \
    UserFromDB, UserSchemaFull, MechanicCreateDataResponse, DriverDataFromDBResponse

router = APIRouter()


@router.post("/admin/create", response_model=AdminCreateData, tags=['create'])
async def create_admin(user: get_us, admin: AdminCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать администраторов может только администратор")
    user = create_user_crud(session, admin)
    return user


@router.post("/driver/create", tags=['create'], response_model=DriverDataFromDBResponse)
async def create_driver(user: get_us, driver_data: DriverCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать водителей может только администратор")
    user = create_user_crud(session, driver_data)
    driver = create_driver_crud(session, user, driver_data)
    return DriverDataFromDBResponse(id=driver.id,
                                    username=user.username,
                                    password=user.password,
                                    fullname=user.fullname,
                                    job_title=user.job_title,
                                    date_of_employment=user.date_of_employment,
                                    date_of_dismissal=user.date_of_dismissal,
                                    is_active=user.is_active,
                                    role_name=user.role_name,
                                    car_access_type=driver.car_access_type)


@router.post("/mechanic/create", tags=['create'], response_model=MechanicCreateDataResponse)
async def create_mechanic(user: get_us, mechanic_data: MechanicCreateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать механиков может только администратор")
    user = create_user_crud(session, mechanic_data)
    mechanic = create_mechanic_crud(session, user)
    return MechanicCreateDataResponse(id=mechanic.id,
                                      username=user.username,
                                      password=user.password,
                                      fullname=user.fullname,
                                      job_title=user.job_title,
                                      date_of_employment=user.date_of_employment,
                                      date_of_dismissal=user.date_of_dismissal,
                                      is_active=user.is_active,
                                      role_name=user.role_name)


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


@router.post("/driver/update_access", tags=['update'])
async def update_driver_car_access_type(user: get_us, driver_fields: DriverUpdateData,
                                        session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin],
                 error_msg="Обновить тип доступа к машинам у водителя может только администратор")
    driver_user = get_user_by_login_crud(session, driver_fields.username)
    driver = update_driver_crud(session, driver_fields)
    return {f"Обновлены права водителя {driver_fields.username}":
                DriverDataFromDBResponse(id=driver.id,
                                         car_access_type=driver.car_access_type,
                                         username=driver_user.username,
                                         password=driver_user.password,
                                         fullname=driver_user.fullname,
                                         job_title=driver_user.job_title,
                                         date_of_employment=driver_user.date_of_employment,
                                         date_of_dismissal=driver_user.date_of_dismissal,
                                         is_active=driver_user.is_active,
                                         role_name=driver_user.role_name,
                                         )}


@router.get("/user/get_by_name", tags=['get_info'], response_model=UserSchemaFull)
async def get_user_by_name(user: get_us, username: str, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin],
                 error_msg="Обновить тип доступа к машинам у водителя может только администратор")
    user = get_user_by_login_crud(session, username)
    return user

@router.get("/driver/get_by_name", tags=['get_info'], response_model=DriverDataFromDBResponse)
async def get_driver_by_name(user: get_us, username: str, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin],
                 error_msg="Обновить тип доступа к машинам у водителя может только администратор")
    driver_user = get_user_by_login_crud(session, username)
    driver = get_driver_by_user_login(session, driver_user)
    return DriverDataFromDBResponse(id=driver.id,
                                    car_access_type=driver.car_access_type,
                                    username=driver_user.username,
                                    password=driver_user.password,
                                    fullname=driver_user.fullname,
                                    job_title=driver_user.job_title,
                                    date_of_employment=driver_user.date_of_employment,
                                    date_of_dismissal=driver_user.date_of_dismissal,
                                    is_active=driver_user.is_active,
                                    role_name=driver_user.role_name,
                                    )
