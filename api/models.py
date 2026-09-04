from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base

#Associative table  that connects what cargoes that trip has or vice versa
trip_cargo = Table(
    "trip_cargo",
    Base.metadata,
    Column(
        "trip_id",
        ForeignKey("trips.id"),
        primary_key=True,
    ),
    Column(
        "cargo_id",
        ForeignKey("cargoes.id"),
        primary_key=True,
    ),
)


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    cpf_document: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    trips: Mapped[list["Trip"]] = relationship(back_populates="driver")


class Truck(Base):
    __tablename__ = "trucks"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    max_weight: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        CheckConstraint("max_weight > 0", name="chk_max_weight_positive"),
        nullable=False,
    )
    trips: Mapped[list["Trip"]] = relationship(back_populates="truck")


class Cargo(Base):
    __tablename__ = "cargoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        CheckConstraint("weight > 0", name="chk_weight_positive"),
        nullable=False,
    )

    trips: Mapped[list["Trip"]] = relationship(
        secondary=trip_cargo,
        back_populates="cargoes",
    )


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), nullable=False)
    truck_id: Mapped[int] = mapped_column(ForeignKey("trucks.id"), nullable=False)
    address_departure: Mapped[str] = mapped_column(String, nullable=False)
    address_arrival: Mapped[str] = mapped_column(String, nullable=False)

    driver: Mapped["Driver"] = relationship(back_populates="trips")
    truck: Mapped["Truck"] = relationship(back_populates="trips")
    cargoes: Mapped[list["Cargo"]] = relationship(
        secondary=trip_cargo,
        back_populates="trips",
    )
