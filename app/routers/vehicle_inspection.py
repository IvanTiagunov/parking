from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.auth import get_us
from app.crud.car import create_car_crud, update_car_crud, get_list_car_crud, get_car_by_id_crud
from app.crud.user import get_user_by_id_crud
from app.crud.vehicle_inspection import create_vi_crud, get_list_vi_crud, get_vi_info_by_id_crud
from app.db.database import get_db
from app.dependencies import check_rights
from app.enums import Role
from app.schemas.car import CarData, CarDataResponse, CarUpdateData
from app.schemas.vehicle_inspection import VehicleInspectionDataResponse, \
    VehicleInspectionCreateWithCarNumber, VIFromDB, VehicleInspectionFull

router = APIRouter(tags=['vehicle_inspection'])


@router.post("/vehicle_inspection/create", response_model=VehicleInspectionFull)
async def create_vehicle_inspection(user: get_us, vehicle_inspection: VehicleInspectionCreateWithCarNumber,
                                    session: Session = Depends(get_db)):
    check_rights(user, roles=[Role.mechanic], error_msg="Проводить технический осмотр может только механик")
    vi = create_vi_crud(session, vehicle_inspection, user.id)
    car = get_car_by_id_crud(session, vi.car_id)
    return VehicleInspectionFull(id=vi.id,
                                 date=vi.date,
                                 inspection_result=vi.inspection_result,
                                 car_id=vi.car_id,
                                 car_number=car.number,
                                 mechanic_id=user.id,
                                 mechanic_name=user.username,
                                 mechanic_fullname=user.fullname)


@router.get("/vehicle_inspection/get_list", response_model=list[VIFromDB])
async def get_list_vehicle_inspection(user: get_us, session: Session = Depends(get_db)):
    vis = get_list_vi_crud(session)
    return vis


@router.get("/vehicle_inspection/get_info_by_id", response_model=VehicleInspectionFull)
async def get_vi_info_by_id(user: get_us, vi_id: int, session: Session = Depends(get_db)):
    vi = get_vi_info_by_id_crud(session, vi_id)
    car = get_car_by_id_crud(session, vi.car_id)
    mechanic_user = get_user_by_id_crud(session, user_id=vi.mechanic_id)
    return VehicleInspectionFull(
        id=vi.id,
        date=vi.date,
        inspection_result=vi.inspection_result,
        car_id=car.id,
        car_number=car.number,
        mechanic_id=mechanic_user.id,
        mechanic_name=mechanic_user.username,
        mechanic_fullname=mechanic_user.fullname)
