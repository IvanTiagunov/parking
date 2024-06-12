import datetime

from sqlalchemy import UniqueConstraint, String, DATE
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.enums import CarType, CarLocation, RepairStatus


class Car(Base):
    """Машина"""
    __tablename__ = 'car'
    __table_args__ = (UniqueConstraint('number'),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    number: Mapped[str] = mapped_column(String(length=320), nullable=False)
    type: Mapped[CarType] = mapped_column(default=CarType.passenger, nullable=False)
    manufacture_date: Mapped[datetime.date] = mapped_column(nullable=False)
    location_status: Mapped[CarLocation] = mapped_column(default=CarLocation.on_parking)
    repair_status: Mapped[RepairStatus] = mapped_column(default=RepairStatus.normal)