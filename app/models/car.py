from enum import Enum

from sqlalchemy import UniqueConstraint, String, DATE
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


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


class Car(Base):
    """Машина"""
    __tablename__ = 'car'
    __table_args__ = (UniqueConstraint('car_number'),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    car_number: Mapped[str] = mapped_column(String(length=320), nullable=False)
    car_type: Mapped[CarType] = mapped_column(default=CarType.passenger, nullable=False)
    manufacture_date: Mapped[DATE] = mapped_column(nullable=False)
    location_status: Mapped[CarLocation] = mapped_column(default=CarLocation.on_parking)
    repair_status: Mapped[RepairStatus] = mapped_column(default=RepairStatus.normal)