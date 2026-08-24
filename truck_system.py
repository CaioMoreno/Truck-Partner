from cli import cargoes, drivers, trips, trucks


class TruckSystem:
    def __init__(self):
        pass

    def help_main(self):
        print("\n================================")
        print("       TRUCK MANAGEMENT")
        print("================================\n")
        print("1. Drivers")
        print("2. Trucks")
        print("3. Cargoes")
        print("4. Trips")
        print("0. Exit\n")

    def trip_help(self):
        print("Trips")
        print("--------------------------------")
        print("1. Create trip")
        print("2. List trips")
        print("3. Add cargo to trip")
        print("4. Remove cargo from trip")
        print("5. Show trip details")
        print("6. Check trip weight")
        print("0. Back\n")

    def driver_help(self):
        print("Drivers")
        print("--------------------------------")
        print("1. Add driver")
        print("2. List drivers")
        print("3. Update Driver")
        print("4. Delete Driver")
        print("0. Back\n")

    def truck_help(self):
        print("Trucks")
        print("--------------------------------")
        print("1. Add truck")
        print("2. List trucks")
        print("3. Update truck")
        print("4. Delete truck")
        print("0. Back\n")

    def cargoes_help(self):
        print("Cargoes")
        print("--------------------------------")
        print("1. Add cargo")
        print("2. List cargoes")
        print("3. Update cargo")
        print("4. Delete cargo")
        print("0. Back\n")

    def trip_menu(self):
        while True:
            self.trip_help()
            option = input("Choose an option: ")
            if option == "1":
                trips.create_trip()
            elif option == "2":
                trips.list_trips()
            elif option == "3":
                trips.add_cargo()
            elif option == "4":
                trips.remove_cargo()
            elif option == "5":
                trips.show_details()
            elif option == "6":
                trips.check_weight()
            elif option == "0":
                break
            else:
                print("Option not available")

    def driver_menu(self):
        while True:
            self.driver_help()
            option = input("Choose an option: ")
            if option == "1":
                drivers.add_driver()
            elif option == "2":
                drivers.list_drivers()
            elif option == "3":
                drivers.update_driver()
            elif option == "4":
                drivers.delete_driver()
            elif option == "0":
                break
            else:
                print("Option not available")

    def truck_menu(self):
        while True:
            self.truck_help()
            option = input("Choose an option: ")
            if option == "1":
                trucks.add_truck()
            elif option == "2":
                trucks.list_trucks()
            elif option == "3":
                trucks.update_truck()
            elif option == "4":
                trucks.delete_truck()
            elif option == "0":
                break
            else:
                print("Option not available")

    def cargoes_menu(self):
        while True:
            self.cargoes_help()
            option = input("Choose an option: ")
            if option == "1":
                cargoes.add_cargo()
            elif option == "2":
                cargoes.list_cargoes()
            elif option == "3":
                cargoes.update_cargo()
            elif option == "4":
                cargoes.delete_cargo()
            elif option == "0":
                break
            else:
                print("Option not available")

    def execute(self):
        while True:
            self.help_main()
            option = input("Choose an option: ")
            if option == "1":
                self.driver_menu()
            elif option == "2":
                self.truck_menu()
            elif option == "3":
                self.cargoes_menu()
            elif option == "4":
                self.trip_menu()
            elif option == "0":
                print("Bye!!")
                break
            else:
                print("Option not available!!")
