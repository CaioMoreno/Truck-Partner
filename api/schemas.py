from pydantic import BaseModel, ConfigDict, Field


class DriverBase(BaseModel):
    first_name: str
    last_name: str
    cpf_document: str = Field(min_length=11, max_length=11)

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class TruckBase(BaseModel):
    plate: str = Field(min_length=7, max_length=7)
    model: str
    max_weight: float = Field(gt=0)

class TruckCreate(TruckBase):
    pass

class TruckResponse(TruckBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CargoBase(BaseModel):
    weight: float = Field(gt=0)
    item: str

class CargoCreate(CargoBase):
    pass

class CargoResponse(CargoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class TripBase(BaseModel):
    address_departure: str
    address_arrival: str

class TripCreate(TripBase):
    driver_id: int
    truck_id: int

class TripResponse(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    driver: DriverResponse
    truck: TruckResponse
    cargoes: list[CargoResponse] = Field(default_factory=list)