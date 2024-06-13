from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.car import get_car_by_number_crud, get_car_by_id_crud, update_car_crud
from app.enums import RepairStatus, CarLocation, CarType, CarAccessType
from app.models.waybill import Waybill
from app.schemas.car import CarInDB, CarUpdateData
from app.schemas.user import DriverInDB
from app.schemas.waybill import WaybillDataCreate


def check_driver_car_access(car_type, driver_access_type):
    if driver_access_type == CarAccessType.all_access:
        return
    if driver_access_type == CarAccessType.no_access:
        raise HTTPException(status_code=401,
                            detail="Невозможно создать Путевой лист с водителем, который не имеет прав на владение Транспортными Средствами."
                                   "Замените водителя (поле driver_name) для продолжения")
    if driver_access_type == CarAccessType.passanger_access and car_type == CarType.passenger:
        return

    if driver_access_type == CarAccessType.truck_access and car_type == CarType.truck:
        return

    raise HTTPException(status_code=401,
                        detail=f"Невозможно создать Путевой лист с водителем, который не имеет прав на владение видом"
                               f" переданного Транспортного средства. Права водителя: {driver_access_type}, тип авто: {car_type}"
                               "Замените водителя или транспортное средство для продолжения")


def create_waybill_crud(session: Session, waybill_data: WaybillDataCreate, car:CarInDB, driver:DriverInDB):
    """Создание и запуск путевого листа"""
    # проводим проверки
    if car.location_status == CarLocation.left_parking:
        raise HTTPException(status_code=401,
                            detail="Невозможно создать Путевой лист с машиной, которая не находится на парковке."
                                   "Замените машину (поле car_number) для продолжения")

    if car.repair_status == RepairStatus.need_repair:
        raise HTTPException(status_code=401,
                            detail="Невозможно создать Путевой лист с машиной, которой требуется ремонт."
                                   "Замените машину (поле car_number) для продолжения")

    check_driver_car_access(car.type, driver.car_access_type)

    # создаём путевой лист
    db_waybill = Waybill(
        arrival=waybill_data.arrival,
        departure=waybill_data.departure,
        car_id=car.id,
        driver_id=driver.id
    )
    session.add(db_waybill)
    session.commit()
    session.refresh(db_waybill)

    #Обновляем поля ТС
    car.location_status = CarLocation.left_parking
    update_car_crud(session,
                    CarUpdateData(id=car.id,
                                  number=car.number,
                                  type=car.type,
                                  manufacture_date=car.manufacture_date,
                                  location_status=car.location_status,
                                  repair_status=car.repair_status
                                  )
                    )

    return db_waybill

def get_list_waybill_crud(session: Session):
    """Получение списка всех техосмотров"""
    get_waybill_query = select(Waybill)
    waybills_from_table = session.scalars(get_waybill_query).all()
    return waybills_from_table


def get_waybill_info_by_id_crud(session, waybill_id):
    waybill_query = select(Waybill).where(Waybill.id == waybill_id)
    waybill_from_table = session.scalar(waybill_query)
    if not waybill_from_table:
        raise HTTPException(status_code=400,
                            detail=f"Путевой лист по переданному идентификатору - '{waybill_id}' не найден. "
                                   f"Поменяйте поле 'waybill_id' чтобы продолжить")
    return waybill_from_table