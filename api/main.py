from fastapi import FastAPI, HTTPException, status
from schemas import (
    CargoCreate,
    CargoResponse,
    DriverCreate,
    DriverResponse,
    TruckCreate,
    TruckResponse,
)

app = FastAPI()

drivers: list[dict] = [
    {
        "id": 1,
        "first_name": "Caio",
        "last_name": "Moreno",
        "cpf": "11111111111",
    },
    {
        "id": 2,
        "first_name": "Lu",
        "last_name": "Lu",
        "cpf": "22222222222"
    }
]

trucks: list[dict] = [
    {
        "id": 1,
        "plate": "API1999",
        "model": "Volvo FH",
        "max_weight": 1000
    }
]

cargoes: list[dict] = [
    {
        "id": 1,
        "weight": 200,
        "item": "wood"
    }
]


@app.get("/")
def home():
    return {"message": "Welcome to Truck-Partner API!"}


@app.get("/status")
def get_status():
    return {"application": "Truck Partner", "running": True, "version": 0.2}


@app.get("/drivers", response_model=list[DriverResponse])
def get_drivers():
    return drivers

@app.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int):
    for driver in drivers:
        if driver.get("id") == driver_id:
            return driver

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Driver not found"
    )


@app.post(
        "/drivers",
        response_model=DriverResponse,
        status_code=status.HTTP_201_CREATED
)
def create_driver(driver: DriverCreate):
    new_id = max(d["id"] for d in drivers) + 1 if drivers else 1

    new_driver = {
        "id": new_id,
        "first_name": driver.first_name,
        "last_name": driver.last_name,
        "cpf": driver.cpf
    }
    drivers.append(new_driver)
    return new_driver


@app.get("/trucks", response_model=list[TruckResponse])
def get_trucks():
    return trucks

@app.get("/trucks/{truck_id}", response_model=TruckResponse)
def get_truck(truck_id: int):
    for truck in trucks:
        if truck.get("id") == truck_id:
            return truck
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Truck not found"
    )

@app.post(
        "/trucks",
        response_model=TruckResponse,
        status_code=status.HTTP_201_CREATED
)
def create_truck(truck: TruckCreate):
    new_id = max(t["id"] for t in trucks) + 1 if trucks else 1

    new_truck = {
        "id": new_id,
        "plate": truck.plate,
        "model": truck.model,
        "max_weight": truck.max_weight
    }

    trucks.append(new_truck)
    return new_truck

@app.get("/cargoes")
def get_cargoes():
    return cargoes

@app.get("/cargoes/{cargo_id}")
def get_cargo(cargo_id: int):
    for cargo in cargoes:
        if cargo.get("id") == cargo_id:
            return cargo
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cargo not found"
    )

@app.post(
    "/cargoes",
    response_model=CargoResponse,
    status_code = status.HTTP_201_CREATED
)
def create_cargo(cargo: CargoCreate):
    new_id = max(c["id"] for c in cargoes) + 1 if cargoes else 1

    new_cargo = {
        "id": new_id,
        "weight": cargo.weight,
        "item": cargo.item
    }

    cargoes.append(new_cargo)
    return new_cargo