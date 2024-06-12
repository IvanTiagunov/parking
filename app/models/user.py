import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.enums import Role, CarAccessType



class User(Base):
    __tablename__ = 'user'
    __table_args__ = (UniqueConstraint('username', 'token_value'),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=320), nullable=False)
    password: Mapped[str] = mapped_column(String(length=320), nullable=False)
    fullname: Mapped[str] = mapped_column(String(length=320), nullable=True)
    job_title: Mapped[str] = mapped_column(String(length=320), nullable=True)
    date_of_employment: Mapped[datetime] = mapped_column(Date, nullable=True)
    date_of_dismissal: Mapped[datetime] = mapped_column(Date, nullable=True)
    token_value: Mapped[uuid.UUID] = mapped_column(unique=True, default=uuid.uuid4)

    role_name: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Driver(Base):
    """Водитель"""
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    car_access_type: Mapped[CarAccessType] = mapped_column(default=CarAccessType.no_access)


class Mechanic(Base):
    """Механик"""
    __tablename__ = 'mechanic'
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

