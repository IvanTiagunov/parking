
import datetime
from typing import Union
from pydantic import BaseModel

from app.enums import CarType, CarLocation, RepairStatus


class CarData(BaseModel):
    number: str
    type: CarType
    manufacture_date: datetime.date
    location_status: CarLocation
    repair_status: RepairStatus

class CarDataResponse(CarData):
    id: int

class CarUpdateData(CarData):
    id: int

class CarInDB(BaseModel):
    id: int
    number: str
    type: CarType
    manufacture_date: datetime.date
    location_status: CarLocation
    repair_status: RepairStatus
