from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.car import get_car_by_id_crud, get_car_by_number_crud
from app.crud.user import get_user_by_id_crud, get_driver_by_user, get_user_by_login_crud
from app.crud.waybill import create_waybill_crud, get_list_waybill_crud, get_waybill_info_by_id_crud
from app.db.database import get_db
from app.dependencies import check_rights
from app.enums import Role, CarLocation
from app.schemas.vehicle_inspection import VehicleInspectionFull
from app.schemas.waybill import WaybillDataCreate, WaybillDataFull, WaybillFromDB

router = APIRouter(tags=['waybill'])


@router.post("/waybill/create", response_model=WaybillDataFull)
async def create_waybill(user: get_us, waybill_data: WaybillDataCreate,
                         session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.driver, Role.admin], error_msg="Создаnm и запустить путевой лист может только водитель или администратор")
    car = get_car_by_number_crud(session, waybill_data.car_number)
    waybill_user = get_user_by_login_crud(session, waybill_data.driver_username)
    driver = get_driver_by_user(session, waybill_user)
    waybill = create_waybill_crud(session, waybill_data, car=car, driver=driver)
    return WaybillDataFull(id=waybill.id,
                           arrival=waybill.arrival,
                           departure=waybill.departure,
                           car_id=car.id,
                           car_number=car.number,
                           car_location=CarLocation.left_parking,
                           driver_id=driver.id,
                           driver_car_access_type=driver.car_access_type,
                           driver_username=waybill_user.username
                           )


@router.get("/waybill/get_list", response_model=list[WaybillFromDB])
async def get_list_waybills(user: get_us, session: Session = Depends(get_db)):
    waybills = get_list_waybill_crud(session)
    return waybills

@router.get("/waybill/get_info_by_id", response_model=VehicleInspectionFull)
async def get_waybill_info_by_id(user: get_us, waybill_id: int, session: Session = Depends(get_db)):
    waybill = get_waybill_info_by_id_crud(session, waybill_id)
    car = get_car_by_id_crud(session, waybill.car_id)
    driver_user = get_user_by_id_crud(session, user_id=waybill.driver_id)
    driver_info = get_driver_by_user(session, driver_user)

    return WaybillDataFull(id=waybill.id,
                           arrival=waybill.arrival,
                           departure=waybill.departure,
                           car_id=car.id,
                           car_number=car.number,
                           car_location=CarLocation.left_parking,
                           driver_id=driver_user.driver_id,
                           driver_car_access_type=driver_info.car_access_type,
                           driver_username=driver_user.username
                           )

#todo закрытие путевого листа

# @router.post("/waybill/close", response_model=WaybillDataFull)
# async def create_waybill(user: get_us, waybill_data: WaybillDataClose,
#                          session: Session = Depends(get_db)):
#     check_rights(user, roles=[Role.driver], error_msg="Закрывать путевой лист может только водитель")
#     car = get_car_by_number_crud(session, waybill_data.car_number)
#     driver = get_driver_by_user(user)
#     waybill = create_waybill_crud(session, waybill_data, car=car, driver=driver)
#     return WaybillDataFull(id=waybill.id,
#                            arrival=waybill.arrival,
#                            departure=waybill.departure,
#                            car_id=car.id,
#                            car_number=car.number,
#                            car_location=CarLocation.left_parking,
#                            driver_id=driver.id,
#                            driver_car_access_type=driver.car_access_type,
#                            driver_username=user.username
#                            )