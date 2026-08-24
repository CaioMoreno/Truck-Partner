
-- DRIVERS

CREATE TABLE "drivers" (
    "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "cpf_document" VARCHAR(11) NOT NULL UNIQUE
);


-- TRUCKS

CREATE TABLE "trucks" (
    "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "plate" VARCHAR(7) NOT NULL UNIQUE,
    "model" VARCHAR(255) NOT NULL,
    "max_weight" NUMERIC(10, 2) NOT NULL
        CHECK ("max_weight" > 0)
);


-- TRIPS

CREATE TABLE "trips" (
    "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "driver_id" INT NOT NULL,
    "truck_id" INT NOT NULL,
    "address_arrival" VARCHAR(255) NOT NULL,
    "address_departure" VARCHAR(255) NOT NULL,

    CONSTRAINT "fk_driver"
        FOREIGN KEY ("driver_id")
        REFERENCES "drivers"("id"),

    CONSTRAINT "fk_truck"
        FOREIGN KEY ("truck_id")
        REFERENCES "trucks"("id")
);


-- CARGOES

CREATE TABLE "cargoes" (
    "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "weight" NUMERIC(10, 2) NOT NULL
        CHECK ("weight" > 0),
    "item" VARCHAR(255) NOT NULL
);


-- MANY-TO-MANY BETWEEN TRIPS AND CARGOES

CREATE TABLE "trip_cargo" (
    "trip_id" INT NOT NULL
        REFERENCES "trips"("id")
        ON DELETE CASCADE,

    "cargo_id" INT NOT NULL
        REFERENCES "cargoes"("id")
        ON DELETE CASCADE,

    PRIMARY KEY ("trip_id", "cargo_id")
);


-- INDEXES

CREATE INDEX "idx_trips_driver_id"
ON "trips"("driver_id");

CREATE INDEX "idx_trips_truck_id"
ON "trips"("truck_id");

CREATE INDEX "idx_trip_cargo_cargo_id"
ON "trip_cargo"("cargo_id");


-- VIEW: TRIP DETAILS

CREATE OR REPLACE VIEW "trip_details" AS
SELECT
    "trips"."id" AS "trip_id",
    "drivers"."first_name",
    "drivers"."last_name",
    "trucks"."plate",
    "trucks"."model",
    "trips"."address_departure",
    "trips"."address_arrival",
    "cargoes"."id" AS "cargo_id",
    "cargoes"."item" AS "cargo_item",
    "cargoes"."weight" AS "cargo_weight"
FROM "trips"
JOIN "drivers"
    ON "trips"."driver_id" = "drivers"."id"
JOIN "trucks"
    ON "trips"."truck_id" = "trucks"."id"
LEFT JOIN "trip_cargo"
    ON "trips"."id" = "trip_cargo"."trip_id"
LEFT JOIN "cargoes"
    ON "trip_cargo"."cargo_id" = "cargoes"."id";


-- VIEW: TRUCK WEIGHT

CREATE VIEW "check_weight" AS
SELECT
    "trips"."id" AS "trip_id",
    SUM("cargoes"."weight") AS "cargo_weight",
    "trucks"."max_weight",
    SUM("cargoes"."weight") > "trucks"."max_weight"
        AS "overloaded"
FROM "trips"
JOIN "trucks"
    ON "trips"."truck_id" = "trucks"."id"
JOIN "trip_cargo"
    ON "trips"."id" = "trip_cargo"."trip_id"
JOIN "cargoes"
    ON "cargoes"."id" = "trip_cargo"."cargo_id"
GROUP BY
    "trips"."id",
    "trucks"."max_weight";