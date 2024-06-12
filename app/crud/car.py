from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.models.user import User, Driver, Mechanic
from app.models.car import Car
from app.schemas.car import CarCreateData


def check_car_not_exist(session, car_data):
    car_query = select(Car).where(Car.number == car_data.number)
    car_from_table = session.scalar(car_query)
    if car_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Машина с переданным номером - '{car_data.number}' уже существует. "
                                   f"Поменяйте поле 'number' чтобы продолжить")


def create_car_crud(session: Session, car_data: CarCreateData):
    check_car_not_exist(session, car_data)
    car = Car(
        number=car_data.number,
        type=car_data.type,
        manufacture_date=car_data.manufacture_date,
        location_status=car_data.location_status,
        repair_status=car_data.repair_status
    )
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

