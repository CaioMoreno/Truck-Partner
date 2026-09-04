from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from api import models
from api.database import Base, engine, get_db
from api.schemas import (
    CargoCreate,
    CargoResponse,
    DriverCreate,
    DriverResponse,
    TripCreate,
    TripResponse,
    TruckCreate,
    TruckResponse,
)

Base.metadata.create_all(bind=engine)

DbSession = Annotated[Session, Depends(get_db)]

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Truck-Partner API!"}


@app.get("/status")
def get_status():
    return {"application": "Truck Partner", "running": True, "version": 0.2}


@app.get("/drivers", response_model=list[DriverResponse])
def get_drivers(db: DbSession):
    statement = select(models.Driver)

    return db.scalars(statement).all()


@app.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: DbSession):
    driver = db.get(models.Driver, driver_id)

    if driver:
        return driver

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
    )


@app.post(
    "/drivers", response_model=DriverResponse, status_code=status.HTTP_201_CREATED
)
def create_driver(driver: DriverCreate, db: DbSession):
    statement = select(models.Driver).where(
        models.Driver.cpf_document == driver.cpf_document
    )
    existing_driver = db.scalars(statement).first()

    if existing_driver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver already exists",
        )

    new_driver = models.Driver(
        first_name=driver.first_name,
        last_name=driver.last_name,
        cpf_document=driver.cpf_document,
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return new_driver


@app.get("/trucks", response_model=list[TruckResponse])
def get_trucks(db: DbSession):
    statement = select(models.Truck)

    return db.scalars(statement).all()


@app.get("/trucks/{truck_id}", response_model=TruckResponse)
def get_truck(truck_id: int, db: DbSession):
    truck = db.get(models.Truck, truck_id)

    if truck:
        return truck

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Truck not found")


@app.post("/trucks", response_model=TruckResponse, status_code=status.HTTP_201_CREATED)
def create_truck(truck: TruckCreate, db: DbSession):
    statement = select(models.Truck).where(models.Truck.plate == truck.plate)

    existing_truck = db.scalars(statement).first()

    if existing_truck:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Truck plate already exists",
        )

    new_truck = models.Truck(
        plate=truck.plate, model=truck.model, max_weight=truck.max_weight
    )
    db.add(new_truck)
    db.commit()
    db.refresh(new_truck)

    return new_truck


@app.get("/cargoes", response_model=list[CargoResponse])
def get_cargoes(db: DbSession):
    statement = select(models.Cargo)

    return db.scalars(statement).all()


@app.get("/cargoes/{cargo_id}", response_model=CargoResponse)
def get_cargo(cargo_id: int, db: DbSession):
    statement = select(models.Cargo).where(models.Cargo.id == cargo_id)
    cargo = db.scalars(statement).first()

    if cargo:
        return cargo

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo not found")


@app.post("/cargoes", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def create_cargo(cargo: CargoCreate, db: DbSession):
    new_cargo = models.Cargo(item=cargo.item, weight=cargo.weight)

    db.add(new_cargo)
    db.commit()
    db.refresh(new_cargo)

    return new_cargo


@app.get("/trips", response_model=list[TripResponse])
def get_trips(db: DbSession):
    statement = select(models.Trip).options(
        selectinload(models.Trip.cargoes),
        selectinload(models.Trip.driver),
        selectinload(models.Trip.truck),
    )

    return db.scalars(statement).all()


@app.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: DbSession):
    statement = (
        select(models.Trip)
        .where(models.Trip.id == trip_id)
        .options(
            selectinload(models.Trip.cargoes),
            selectinload(models.Trip.driver),
            selectinload(models.Trip.truck),
        )
    )
    trip = db.scalars(statement).first()

    if trip:
        return trip

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")


@app.post("/trips", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip: TripCreate, db: DbSession):
    driver = db.get(models.Driver, trip.driver_id)

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found",
        )

    truck = db.get(models.Truck, trip.truck_id)

    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Truck not found",
        )

    new_trip = models.Trip(
        driver_id=trip.driver_id,
        truck_id=trip.truck_id,
        address_departure=trip.address_departure,
        address_arrival=trip.address_arrival,
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip


@app.post("/trips/{trip_id}/cargoes/{cargo_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_cargo_to_trip(trip_id: int, cargo_id: int, db: DbSession):
    trip = db.get(models.Trip, trip_id)

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    cargo = db.get(models.Cargo, cargo_id)

    if not cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo not found",
        )

    if cargo in trip.cargoes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cargo already added to trip",
        )

    trip.cargoes.append(cargo)

    db.commit()
