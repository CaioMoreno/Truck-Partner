from db import get_connection


def add_cargo():
    item = input("Cargo: ")
    weight = input("Weight: ")

    if not item or not weight:
        print("All fields are required.")
        return

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """ 
            INSERT INTO cargoes (item, weight)
            VALUES (%s, %s);
            """,
            (item, weight),
        )


def list_cargoes():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM cargoes
            ORDER BY id;
            """
        )
        cargoes = cur.fetchall()

        if not cargoes:
            print("\nNo cargoes found.")
            return

        print("\nCargoes")
        print("--------------------------------")

        for cargo in cargoes:
            print(f"\nID: {cargo[0]}")
            print(f"Item: {cargo[2]}")
            print(f"Weight: {cargo[1]}")


def update_cargo():
    cargo_id = input("Cargo id to update: ")
    item = input("Cargo: ")
    weight = input("Weight: ")

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE cargoes
            SET item = %s,
            weight = %s
            WHERE id = %s;
            """,
            (item, weight, cargo_id),
        )
        if cur.rowcount == 0:
            print("Cargo not found.")
        else:
            print("Cargo updated successfully.")


def delete_cargo():
    cargo_id = input("Cargo id to delete: ")

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM cargoes
            WHERE id = %s;
            """,
            (cargo_id,),
        )
        if cur.rowcount == 0:
            print("Cargo not found")
        else:
            print("Cargo deleted successfully")


if __name__ == "__main__":
    add_cargo()
    update_cargo()
    delete_cargo()
    list_cargoes()
