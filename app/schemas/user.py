import datetime
import uuid
from typing import Union

from pydantic import BaseModel

from app.models.user import Role, CarAccessType


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
    role_name: Role.driver
    car_access_type: CarAccessType

class AdminCreateData(UserCreateData):
    role_name: Role.admin

class MechanicCreateData(UserCreateData):
    role_name: Role.mechanic

