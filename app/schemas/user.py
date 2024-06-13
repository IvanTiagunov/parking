import datetime
import uuid
from typing import Union
from pydantic import BaseModel
from app.enums import Role, CarAccessType


class UserSchemaPublic(BaseModel):
    id: int
    fullname: Union[str, None]
    job_title: Union[str, None]
    date_of_employment: Union[datetime.date, None]
    date_of_dismissal: Union[datetime.date, None]
    role_name: Role
    is_active: bool


class UserSchemaFull(UserSchemaPublic):
    username: str
    password: str
    token_value: uuid.UUID


class UserCreateData(BaseModel):
    username: str
    password: str
    fullname: Union[str, None]
    job_title: Union[str, None]
    date_of_employment: Union[datetime.date, None]
    date_of_dismissal: Union[datetime.date, None]
    is_active: bool


class DriverCreateData(UserCreateData):
    role_name: Role = Role.driver
    car_access_type: CarAccessType

class DriverDataFromDBResponse(DriverCreateData):
    id: int


class DriverCreateResponseData(UserCreateData):
    role_name: Role = Role.driver
    car_access_type: CarAccessType


class AdminCreateData(UserCreateData):
    role_name: Role = Role.admin


class MechanicCreateData(UserCreateData):
    role_name: Role = Role.mechanic

class MechanicCreateDataResponse(UserCreateData):
    id: int

class DriverUpdateData(BaseModel):
    username: str
    car_access_type: Union[CarAccessType, None]


class UserUpdateFields(BaseModel):
    username: str
    fullname: Union[str, None]
    job_title: Union[str, None]
    date_of_employment: Union[datetime.date, None]
    date_of_dismissal: Union[datetime.date, None]


class UserFromDB(BaseModel):
    id: int
    username: str
    fullname: Union[str, None]
    job_title: Union[str, None]
    date_of_employment: Union[datetime.date, None]
    date_of_dismissal: Union[datetime.date, None]
