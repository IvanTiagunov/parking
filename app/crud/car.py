from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.models.car import Car
from app.schemas.car import CarData, CarUpdateData


def check_car_not_exist_by_number(session, car_data):
    car_query = select(Car).where(Car.number == car_data.number)
    car_from_table = session.scalar(car_query)
    if car_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Машина с переданным номером - '{car_data.number}' уже существует. "
                                   f"Поменяйте поле 'number' чтобы продолжить")

def check_car_exist_by_id(session, car_data):
    car_query = select(Car).where(Car.number == car_data.number)
    car_from_table = session.scalar(car_query)
    if not car_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Машина с переданным идентификатором - '{car_data.number}' не существует. "
                                   f"Поменяйте поле 'id' чтобы продолжить")


def create_car_crud(session: Session, car_data: CarData):
    """Создание"""
    check_car_not_exist_by_number(session, car_data)
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

def update_car_crud(session: Session, car_data: CarUpdateData):
    """Обновление машины по id"""
    check_car_exist_by_id(session, car_data)
    update_stmt = (
        update(Car)
        .where(Car.id == car_data.id)
        .values(**car_data.model_dump())
    ).returning(Car)

    updated_car = session.execute(update_stmt).scalar_one()
    session.commit()
    return updated_car

def get_list_car_crud(session: Session):
    """Получение списка машин"""
    get_cars_query = select(Car)
    cars_from_table = session.scalars(get_cars_query).all()
    return cars_from_table

def get_car_by_number_crud(session, number):
    car_query = select(Car).where(Car.number == number)
    car_from_table = session.scalar(car_query)
    if not car_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Машина с переданным номером - '{number}' не существует. "
                                   f"Поменяйте поле 'number' чтобы продолжить")
    return car_from_table


def get_car_by_id_crud(session, car_id):
    car_query = select(Car).where(Car.id == car_id)
    car_from_table = session.scalar(car_query)
    if not car_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Машина с переданным идентификатором - '{car_id}' не существует. "
                                   f"Поменяйте поле 'car_id' чтобы продолжить")
    return car_from_table