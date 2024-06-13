from pydantic import BaseModel
import datetime

from app.enums import CarAccessType, CarLocation


class WaybillDataCreate(BaseModel):
    arrival: datetime.datetime
    departure: datetime.datetime
    car_number: str
    driver_username: str


class WaybillDataFull(BaseModel):
    id: int
    arrival: datetime.datetime
    departure: datetime.datetime
    car_id:int
    car_number: str
    car_location: CarLocation
    driver_id: str
    driver_username: str
    driver_car_access_type: CarAccessType

class WaybillFromDB(BaseModel):
    id: int
    arrival: datetime.datetime
    departure: datetime.datetime
    car_id: str
    driver_id: str
