from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.enums import RepairStatus


class VehicleInspection(Base):
    """Технический осмотр транспортного средства"""
    __tablename__ = 'vehicle_inspection'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now())
    inspection_result: Mapped[RepairStatus] = mapped_column(default=RepairStatus.normal)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanic.id"))