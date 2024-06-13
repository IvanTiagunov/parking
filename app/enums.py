from enum import Enum


class Role(Enum):
    admin: str = "админ"
    driver: str = "водитель"
    mechanic: str = "механик"



class CarAccessType(Enum):
    no_access: str = "нет прав"
    passanger_access: str = "легковые"
    truck_access: str = "грузовые"
    all_access: str = "все права"


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