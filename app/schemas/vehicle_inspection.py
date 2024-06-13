import datetime
import uuid
from typing import Union
from pydantic import BaseModel

from app.enums import Role, CarAccessType, RepairStatus


class VehicleInspectionData(BaseModel):
    date: datetime.datetime
    inspection_result: RepairStatus
    car_id: int


class VehicleInspectionDataResponse(VehicleInspectionData):
    id: int
    mechanic_id: int
    mechanic_name: str

class VehicleInspectionCreateWithCarNumber(BaseModel):
    date: datetime.datetime
    inspection_result: RepairStatus
    car_number: str

class VIFromDB(BaseModel):
    id: int
    date: datetime.datetime
    inspection_result: RepairStatus
    car_id: int
    mechanic_id: int

class VehicleInspectionFull(BaseModel):
    id: int
    date: datetime.datetime
    inspection_result: RepairStatus
    car_id: int
    car_number: str
    mechanic_id: int
    mechanic_name: str