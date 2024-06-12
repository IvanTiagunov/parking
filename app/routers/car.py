from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.car import create_car_crud
from app.db.database import get_db
from app.dependencies import check_admin
from app.schemas.car import CarCreateData, CarCreateDataResponse

router = APIRouter(tags=['car'])


@router.post("/car/create", response_model=CarCreateDataResponse)
async def create_car(user: get_us, car_data: CarCreateData, session: Session = Depends(get_db)):
    check_admin(user, "Создавать машины может только администратор")
    car = create_car_crud(session, car_data)
    return car
