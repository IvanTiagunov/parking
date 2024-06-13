from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.crud.car import get_car_by_number_crud, update_car_crud
from app.enums import CarType, CarLocation, RepairStatus
from app.models.vehicle_inspection import VehicleInspection
from app.schemas.car import CarUpdateData
from app.schemas.vehicle_inspection import VehicleInspectionCreateWithCarNumber


def create_vi_crud(session: Session, vi_data: VehicleInspectionCreateWithCarNumber, user_id):
    """Создание техосмотра"""
    car = get_car_by_number_crud(session, vi_data.car_number)

    db_vi = VehicleInspection(
        date=vi_data.date,
        inspection_result=vi_data.inspection_result,
        car_id=car.id,
        mechanic_id=user_id
    )
    session.add(db_vi)
    session.commit()
    session.refresh(db_vi)

    car.repair_status = vi_data.inspection_result
    update_car_crud(session,
                    CarUpdateData(id=car.id,
                                  number=car.number,
                                  type=car.type,
                                  manufacture_date=car.manufacture_date,
                                  location_status=car.location_status,
                                  repair_status=car.repair_status
                                  )
                    )
    return db_vi


def get_list_vi_crud(session: Session):
    """Получение списка всех техосмотров"""
    get_vi_query = select(VehicleInspection)
    vi_from_table = session.scalars(get_vi_query).all()
    return vi_from_table


def get_vi_info_by_id_crud(session, vi_id):
    vi_query = select(VehicleInspection).where(VehicleInspection.id == vi_id)
    vi_from_table = session.scalar(vi_query)
    if not vi_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Технический осмотр с переданным идентификатором - '{vi_id}' не существует. "
                                   f"Поменяйте поле 'vi_id' чтобы продолжить")
    return vi_from_table