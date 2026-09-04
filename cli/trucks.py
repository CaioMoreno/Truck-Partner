import psycopg

from cli.db import get_connection


def add_truck():
    plate = input("Plate: ")
    model = input("Truck Model: ")
    max_weight = input("Maximum weight: ")

    if not model or not plate or not max_weight:
        print("All fields are required.")
        return

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO trucks (plate, model, max_weight)
                VALUES (%s, %s, %s);
            """,
                (plate, model, max_weight),
            )

            print("Truck added successfully.")
    except psycopg.errors.UniqueViolation:
        print("A truck with this plate already exists.")


def list_trucks():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM trucks
            ORDER BY id;
        """
        )
        trucks = cur.fetchall()

        if not trucks:
            print("\nNo trucks found")
            return

        print("\nTrucks")
        print("--------------------------------")

        for truck in trucks:
            print(f"\nID: {truck[0]}")
            print(f"Plate: {truck[1]}")
            print(f"Model: {truck[2]}")
            print(f"Maximum Weight: {truck[3]}")


def update_truck():
    truck_id = input("Truck id to update: ")
    plate = input("Plate: ")
    model = input("Truck Model: ")
    max_weight = input("Maximum weight: ")

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE trucks
                SET plate = %s,
                model = %s,
                max_weight = %s
                WHERE id = %s;
                """,
                (plate, model, max_weight, truck_id),
            )
            if cur.rowcount == 0:
                print("Truck not found.")
            else:
                print("Truck updated successfully.")
    except psycopg.errors.UniqueViolation:
        print("A truck with this plate already exists.")


def delete_truck():
    truck_id = input("Truck id to delete: ")

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM trucks
                WHERE id = %s;
                """,
                (truck_id,),
            )
            if cur.rowcount == 0:
                print("Truck not found")
            else:
                print("Truck deleted successfully")
    except psycopg.errors.UniqueViolation:
        print("Cannot delete this truck because it is assigned to a trip.")


if __name__ == "__main__":
    add_truck()
    update_truck()
    delete_truck()
    list_trucks()
