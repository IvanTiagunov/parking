from enum import Enum


class Role(Enum):
    admin: str = "админ"
    driver: str = "водитель"
    mechanic: str = "механик"



class CarAccessType(Enum):
    no_access: str = "no_access"
    passanger_access: str = "passanger_access"
    truck_access: str = "truck_access"
    all_access: str = "all_access"