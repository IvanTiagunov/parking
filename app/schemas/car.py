
import datetime
from typing import Union
from pydantic import BaseModel

from app.enums import CarType, CarLocation, RepairStatus


class CarCreateData(BaseModel):
    number: str
    type: CarType
    manufacture_date: datetime.date
    location_status: CarLocation
    repair_status: RepairStatus

class CarCreateDataResponse(CarCreateData):
    id: int