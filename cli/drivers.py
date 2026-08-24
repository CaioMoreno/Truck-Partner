import psycopg

from db import get_connection


def add_driver():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    cpf_document = input("CPF: ")

    if not first_name or not last_name or not cpf_document:
        print("All fields are required.")
        return

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO drivers (first_name, last_name, cpf_document)
                VALUES (%s, %s, %s);
            """,
                (first_name, last_name, cpf_document),
            )

            print("Driver added successfully.")
    except psycopg.errors.UniqueViolation:
        print("A driver with this CPF already exists.")


def list_drivers():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
                SELECT *
                FROM drivers
                ORDER BY id;
            """)
        drivers = cur.fetchall()

        if not drivers:
            print("\nNo drivers found")
            return

        print("\nDrivers")
        print("--------------------------------")

        for driver in drivers:
            print(f"\nID: {driver[0]}")
            print(f"First name: {driver[1]}")
            print(f"Last name: {driver[2]}")
            print(f"CPF: {driver[3]}")


def update_driver():
    driver_id = input("Driver id to update: ")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    cpf_document = input("CPF: ")

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE drivers
                SET first_name = %s,
                last_name = %s,
                cpf_document = %s
                WHERE id = %s;
                """,
                (first_name, last_name, cpf_document, driver_id),
            )
            if cur.rowcount == 0:
                print("Driver not found.")
            else:
                print("Driver updated successfully.")
    except psycopg.errors.UniqueViolation:
        print("A driver with this CPF already exists.")


def delete_driver():
    driver_id = input("Driver id to delete: ")

    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM drivers
                WHERE id = %s;
                """,
                (driver_id,),
            )
            if cur.rowcount == 0:
                print("Driver not found.")
            else:
                print("Driver deleted successfully.")
    except psycopg.errors.UniqueViolation:
        print("Cannot delete this driver because he is assigned to a trip.")


if __name__ == "__main__":
    add_driver()
    update_driver()
    delete_driver()
    list_drivers()
