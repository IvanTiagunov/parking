from sqlalchemy.orm import Session

from app.models.user import User, Driver, Mechanic
from app.schemas.user import UserCreateData, DriverCreateData


def create_user_crud(session: Session, user_data: UserCreateData):
    """Создать пользователя"""
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


def create_driver_crud(session: Session, user, driver_data: DriverCreateData):
    """Создать водителя"""
    driver = Driver(id=user.id, car_access_type=driver_data.car_access_type)
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return user


def create_mechanic_crud(session: Session, user):
    """Создать механика"""
    mechanic = Mechanic(id=user.id)
    session.add(mechanic)
    session.commit()
    session.refresh(mechanic)
    return mechanic
