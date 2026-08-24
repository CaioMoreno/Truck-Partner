--INSERTED SOME DATA IN THE DRIVERS TABLE
INSERT INTO "drivers"("first_name", "last_name", "cpf_document")
VALUES
('Super Paulin', 'De Krypton Universe', '18565423584'),
('Joker Space', 'Of The Great Big Bang', '03569874155');
SELECT * FROM "drivers";

--INSERTED SOME DATA IN THE TRUCKS TABLE
INSERT INTO "trucks"("plate", "model", "max_weight")
VALUES
('GCC2026', 'Volkswagen Delivery 11.180', 10.80),
('SSH2025', 'Volvo FH 540', 20.50);
SELECT * FROM "trucks";

--INSERTED SOME DATA IN THE TRIPS TABLE
INSERT INTO "trips"("driver_id", "truck_id", "address_arrival", "address_departure")
VALUES
(1, 2, 'China, Beijing, St. Xixie', 'China, Xian, St. Norhtwest'),
(2, 1, 'Japan, Tokyo, St. Yakuza', 'Japan, Tokyo, St. Otaku');
SELECT * FROM "trips";

--INSERTED SOME DATA IN THE CARGOES TABLE
INSERT INTO "cargoes"("weight", "item")
VALUES
(1.35, 'Wood'),
(4.5, 'Ciment Blocks'),
(3.3, 'Metal Bars'),
(0.75, 'Car'),
(0.50, 'Motocycle');
SELECT * FROM "cargoes";

--INSERT THE DATA OF THE RELATION BETWEEN CARGO AND TRIP
INSERT INTO "trip_cargo"("trip_id", "cargo_id")
VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5);
SELECT * FROM "trip_cargo";

--A SELECT JOIN TO SEE THE INFORMATION ABOUT THE DRIVERS IN THOSE TRIPS
SELECT "trips"."id" AS "trips_id",
"drivers"."first_name",
"drivers"."last_name",
"trucks"."plate",
"trucks"."model",
"cargoes"."item",
"cargoes"."weight"
FROM "trips"
JOIN "drivers"
ON "trips"."driver_id" = "drivers"."id"
JOIN "trucks"
ON "trips"."truck_id" = "trucks"."id"
JOIN "trip_cargo"
ON "trip_cargo"."trip_id" = "trips"."id"
JOIN "cargoes"
ON "trip_cargo"."cargo_id" = "cargoes"."id";

--UPDATED THE CARGOES ITEM
UPDATE "cargoes"
SET "item" = 'Construction Sand'
WHERE "item" = 'Wood';

--DELETED A CARGOES ITEM FIRST DELETING OF THE DEPENDENT TABLE
DELETE FROM "trip_cargo"
WHERE "cargo_id" = 3;
DELETE FROM "cargoes"
WHERE "id" = 3;

--TESTING VIEW OF TRIP DETAILS
SELECT * FROM "trip_details";

--EXPLAIN QUERY PLAN OF INDEX
EXPLAIN ANALYSE
SELECT * FROM "trips"
WHERE "truck_id" = 2;

--TESTING VIEW OF CHECKING THE WEIGHT
SELECT * FROM "check_weight";