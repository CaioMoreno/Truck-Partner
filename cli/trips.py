import psycopg

from db import get_connection


def create_trip():
    driver_id = input("Driver ID: ")
    truck_id = input("Truck ID: ")
    address_departure = input("Departure address: ")
    address_arrival = input("Arrival address: ")

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO trips (driver_id, truck_id, address_departure, address_arrival)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (driver_id, truck_id, address_departure, address_arrival),
            )

            trip_id = cur.fetchone()[0]

            print(f"\nTrip {trip_id} created successfully.")
    except psycopg.errors.ForeignKeyViolation:
        print("This Driver or Truck doesn't exist")


def list_trips():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, address_arrival, address_departure FROM trips
            ORDER BY id;
            """
        )
        trips = cur.fetchall()
        if not trips:
            print("No trips found.")
            return

        print("\nTrips")
        print("--------------------------------")

        for trip in trips:
            print(f"\nID: {trip[0]}")
            print(f"Address Departure: {trip[2]}")
            print(f"Address Arrival: {trip[1]}")


def add_cargo():
    trip_id = input("Trip ID to add cargo: ")
    cargo_id = input("Cargo ID to add to trip: ")

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO trip_cargo (trip_id, cargo_id)
            VALUES (%s, %s)
            RETURNING trip_id, cargo_id;
            """,
            (trip_id, cargo_id),
        )

        trip_cargo = cur.fetchone()
        print(f"\nTrip {trip_cargo[0]} has been added cargo {trip_cargo[1]}")


def remove_cargo():
    trip_id = input("Trip ID to remove cargo: ")
    cargo_id = input("Cargo ID to remove from the trip: ")

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM trip_cargo
            WHERE trip_id = %s AND cargo_id = %s;
            """,
            (trip_id, cargo_id),
        )
        if cur.rowcount == 0:
            print("Couldn't find trip with this cargo.")
        else:
            print("Cargo deleted from trip successfully")


def show_details():
    trip_id = input("Trip ID: ")

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM trip_details
            WHERE trip_id = %s;
            """, (trip_id)
        )

        trips = cur.fetchall()

        if not trips:
            print("No trips found.")
            return

        for trip in trips:
            print("\nTrips Details")
            print("--------------------------------")
            print(f"ID: {trip[0]}")
            print(f"Driver: {trip[1]} {trip[2]}")
            print(f"Truck: {trip[3]} - Maximum weight{trip[4]}KG")
            print(f"Address departure: {trip[5]}")
            print(f"Address arrival: {trip[6]}")
            print("\nCargoes")
            print("--------------------------------")
            print(f"ID: {trip[7]}")
            print(f"Item: {trip[8]}")
            if trip[9] is None:
                print(f"Weight: {trip[9]}")
            else:
                print(f"Weight: {trip[9]} KG")


def check_weight():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM check_weight
            ORDER BY trip_id;
            """
        )

        trips = cur.fetchall()

        if not trips:
            print("No trips found.")
            return

        print("\nChecking Weight")
        print("--------------------------------")

        for trip in trips:
            print(f"\nID: {trip[0]}")
            print(f"Cargo Weight: {trip[1]}")
            print(f"Truck maximum weight: {trip[2]}")
            print(f"Overloaded: {trip[3]}")


if __name__ == "__main__":
    create_trip()
    add_cargo()
    remove_cargo()
    show_details()
    check_weight()
    list_trips()
