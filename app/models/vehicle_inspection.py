from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class InspectionResult(Enum):
    ok: str = "Не требуется ремонт"
    not_ok: str = "Требуется ремонт"

class VehicleInspection(Base):
    """Технический осмотр транспортного средства"""
    __tablename__ = 'vehicle_inspection'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    date: Mapped[DateTime] = mapped_column(default=datetime.now())
    inspection_result: Mapped[InspectionResult] = mapped_column(default=InspectionResult.ok)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    mechanic_id = Mapped[int] = mapped_column(ForeignKey("mechanic.id"))