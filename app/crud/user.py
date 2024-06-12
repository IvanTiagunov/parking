from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.models.user import User, Driver, Mechanic
from app.schemas.user import UserCreateData, DriverCreateData

def get_user_by_login_crud(session, username):
    get_user_query = select(User).where(User.username == username)
    user_from_table = session.scalar(get_user_query)
    if not user_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Пользователя с переданным логином - '{username}' не существует")
    return user_from_table

def create_user_crud(session: Session, user_data: UserCreateData):
    """Создать пользователя"""
    check_user_not_exist(session, user_data)
    user = User(username=user_data.username,
                password=user_data.password,
                fullname=user_data.fullname,
                job_title=user_data.job_title,
                date_of_employment=user_data.date_of_employment,
                date_of_dismissal=user_data.date_of_dismissal,
                role_name=user_data.role_name,
                is_active=user_data.is_active
                )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def check_user_not_exist(session, user_data):
    get_user_query = select(User).where(User.username == user_data.username)
    user_from_table = session.scalar(get_user_query)
    if user_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Пользователя с переданным логином - '{user_data.username}' уже существует. "
                                   f"Поменяйте поле 'username' чтобы продолжить")
        return None




def create_driver_crud(session: Session, user, driver_data: DriverCreateData):
    """Создать водителя"""
    driver = Driver(id=user.id, car_access_type=driver_data.car_access_type)
    session.add(driver)
    session.commit()
    #session.refresh(driver)
    return driver


def create_mechanic_crud(session: Session, user):
    """Создать механика"""
    mechanic = Mechanic(id=user.id)
    session.add(mechanic)
    session.commit()
    #session.refresh(mechanic)
    return mechanic

def deactivate_user_crud(session, username):
    """Деактивировать пользователя"""
    get_user_query = select(User).where(User.username == username)
    user_from_table = session.scalar(get_user_query)
    if not user_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Пользователя с переданным логином - '{username}' не существует")

    update_st = update(User).where(User.username == username).values(is_active=False).returning(User)
    result = session.scalar(update_st)
    session.commit()
    return result


def get_list_users_crud(session):
    get_users_query = select(User)
    users_from_table = session.scalars(get_users_query).all()
    return users_from_table

def get_driver_by_user_login(session, user):
    get_driver_query = select(Driver).where(Driver.id == user.id)
    driver_from_table = session.scalar(get_driver_query)
    if not driver_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Водителя  - '{user.username}' не существует,"
                                   f" пользователь имеет роль {user.role_name}")
    return driver_from_table

def update_driver_crud(session, driver_fields):
    """Обновить поля водителя"""
    user = get_user_by_login_crud(session, driver_fields.username)
    get_driver_by_user_login(session, user)

    update_st = update(Driver).where(Driver.id == user.id).values(
        car_access_type=driver_fields.car_access_type
    ).returning(Driver)
    session.execute(update_st)
    session.commit()
    updated_driver = get_driver_by_user_login(session, user)
    return updated_driver


def update_user_crud(session: Session, user_data):
    user = get_user_by_login_crud(session, user_data.username)
    update_st = update(User).where(User.id == user.id).values(
        **user_data.model_dump()
    ).returning(User)
    session.execute(update_st)
    session.commit()
    new_user = get_user_by_login_crud(session, user_data.username)
    return new_user


def get_user_by_id_crud(session, user_id):
    query = select(User).where(User.id == user_id)
    user_from_table = session.scalar(query)
    if not user_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Пользователя с переданным id - '{user_id}' не существует")
    return user_from_table
