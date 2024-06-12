from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.database import Base


class Waybill(Base):
    """Путевой лист"""
    __tablename__ = 'waybill'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    arrival: Mapped[DateTime] = mapped_column(default=datetime.now())
    departure: Mapped[DateTime] = mapped_column(default=datetime.now())
    vehicle_inspection: Mapped[int] = mapped_column(ForeignKey("vehicle_inspection.id"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id"))