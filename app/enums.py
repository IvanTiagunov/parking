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


class CarType(Enum):
    """Тип авто"""
    passenger: str = "легковая"
    truck: str = "грузовая"


class CarLocation(Enum):
    """Местоположение машины"""
    on_parking: str = "на парковке"
    left_parking: str = "уехала с парковки"


class RepairStatus(Enum):
    """Техническое состояния авто"""
    normal: str = "не требуется ремонт"
    need_repair: str = "требуется ремонт"