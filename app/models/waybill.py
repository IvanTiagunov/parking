import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.database import Base


class Waybill(Base):
    """Путевой лист"""
    __tablename__ = 'waybill'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    arrival: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    departure: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id"))