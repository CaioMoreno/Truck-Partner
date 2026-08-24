from db import get_connection
from truck_system import TruckSystem


def main():
    try:
        with get_connection():
            print("Connected to PostgreSQL!")

    except Exception as error:  # noqa: BLE001
        print(f"Could not connect to PostgreSQL: {error}")
        return

    system = TruckSystem()
    system.execute()


if __name__ == "__main__":
    main()
