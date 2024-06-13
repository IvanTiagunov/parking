from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.car import create_car_crud, update_car_crud, get_list_car_crud
from app.db.database import get_db
from app.dependencies import check_rights
from app.enums import Role
from app.schemas.car import CarData, CarDataResponse, CarUpdateData

router = APIRouter(tags=['car'])


@router.post("/car/create", response_model=CarDataResponse)
async def create_car(user: get_us, car_data: CarData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin], error_msg="Создавать машины может только администратор")
    car = create_car_crud(session, car_data)
    return car

@router.post("/car/update", response_model=CarUpdateData)
async def update_car(user: get_us, car_data: CarUpdateData, session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.admin, Role.mechanic], error_msg="Обновлять поля машин могут администратор и механик")
    car = update_car_crud(session, car_data)
    return car

@router.get("/car/get_list", response_model=list[CarDataResponse])
async def get_list_cars(user: get_us, session: Session = Depends(get_db)):
    cars = get_list_car_crud(session)
    return cars