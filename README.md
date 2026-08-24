# 🚛 Truck-Partner

**Truck-Partner** is a command-line logistics management system built with **Python and PostgreSQL** for managing drivers, trucks, cargoes, and trips.

The project combines Python application logic with a relational PostgreSQL database, providing a practical system for organizing trucking operations while enforcing relationships and business rules at the database level.


---

## 📌 About the Project

Truck-Partner was created as a practical project for developing and applying skills in **Python, SQL, PostgreSQL, relational database design, Git, and backend development**.

Instead of treating drivers, trucks, cargoes, and trips as isolated data, the system connects them through relational database structures and provides a CLI for interacting with the data.

The current version allows users to:

* Manage drivers
* Manage trucks
* Manage cargoes
* Create and inspect trips
* Assign cargoes to trips
* Remove cargoes from trips
* View detailed trip information
* Compare cargo weight with truck capacity

The project is designed to evolve incrementally as new backend technologies and concepts are introduced.

---

## ✨ Features

### 👤 Driver Management

* Add drivers
* List registered drivers
* Update driver information
* Delete drivers
* Prevent duplicate CPF records

### 🚚 Truck Management

* Add trucks
* List registered trucks
* Update truck information
* Delete trucks
* Prevent duplicate license plates
* Store maximum weight capacity

### 📦 Cargo Management

* Add cargoes
* List cargoes
* Update cargo information
* Delete cargoes
* Store cargo weight

### 🛣️ Trip Management

* Create trips
* List trips
* Assign drivers and trucks to trips
* Add cargoes to trips
* Remove cargoes from trips
* Display detailed trip information
* Display cargoes associated with trips
* Check total cargo weight against truck capacity

---

## 🧠 Business Logic

Truck-Partner uses PostgreSQL relationships and queries to model logistics operations.

A trip connects a **driver** and a **truck**, while cargoes can be associated with trips through a junction table.

```text
Driver ─────┐
            │
            ▼
           Trip ◄───── Truck
            │
            │
            ▼
       Trip_Cargo
            │
            ▼
          Cargo
```

This structure allows one trip to contain multiple cargoes while keeping cargo and trip information separated.

The database also provides information for checking whether the combined weight of cargo assigned to a trip exceeds the truck's maximum supported weight.

---

## 🛠️ Technologies

| Technology    | Purpose                                  |
| ------------- | ---------------------------------------- |
| Python        | Application and CLI logic                |
| PostgreSQL    | Relational database                      |
| Psycopg       | Python ↔ PostgreSQL communication        |
| python-dotenv | Environment variable management          |
| uv            | Python project and dependency management |
| Ruff          | Python linting and formatting            |
| Git           | Version control                          |
| GitHub        | Source code hosting                      |

---

## 📂 Project Structure

```text
Truck-Partner/
│
├── cli/
│   ├── __init__.py
│   ├── cargoes.py
│   ├── drivers.py
│   ├── trips.py
│   └── trucks.py
│
├── db.py
├── main.py
├── truck_system.py
│
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

### Main components

**`main.py`**
Application entry point. Tests the PostgreSQL connection and starts the system.

**`truck_system.py`**
Controls the CLI menus and navigation between the different areas of the application.

**`db.py`**
Creates PostgreSQL connections using credentials stored in environment variables.

**`cli/drivers.py`**
Contains driver CRUD operations.

**`cli/trucks.py`**
Contains truck CRUD operations.

**`cli/cargoes.py`**
Contains cargo CRUD operations.

**`cli/trips.py`**
Contains trip creation, cargo assignment, trip details, and weight-checking operations.

---

## 🗄️ Database Model

The current database is centered around five main structures:

### `drivers`

Stores information about drivers, including their name and CPF.

### `trucks`

Stores truck information such as license plate, model, and maximum supported weight.

### `cargoes`

Stores cargo descriptions and weights.

### `trips`

Represents logistics trips and connects a driver and truck with departure and arrival information.

### `trip_cargo`

Junction table connecting trips and cargoes, allowing cargo to be assigned to trips.

PostgreSQL views are also used to provide information such as detailed trip data and cargo-weight checks.

---

## 💻 CLI

Running Truck-Partner opens the main menu:

```text
================================
       TRUCK MANAGEMENT
================================

1. Drivers
2. Trucks
3. Cargoes
4. Trips
0. Exit
```

Each section provides operations specific to that resource.

For example, the Trips menu provides:

```text
Trips
--------------------------------
1. Create trip
2. List trips
3. Add cargo to trip
4. Remove cargo from trip
5. Show trip details
6. Check trip weight
0. Back
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Truck-Partner
```

### 2. Install dependencies

The project uses `uv` for dependency management.

```bash
uv sync
```

Alternatively, the dependencies listed in `pyproject.toml` can be installed using another compatible Python environment.

### 3. Configure PostgreSQL

Create the PostgreSQL database required by the application and execute the project's database schema.

The application expects the following environment variables:

```env
DB_NAME=your_database_name
DB_USER=your_postgresql_user
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432
```

Copy `.env.example` to a new `.env` file and replace the example values with your local PostgreSQL configuration.


### 4. Run Truck-Partner

From the project root:

```bash
uv run python main.py
```

If the database configuration is correct, the application will connect to PostgreSQL and display the main CLI menu.

---

## 🧹 Code Quality

The project uses **Ruff** for Python linting and formatting.

Format the project:

```bash
uv run ruff format .
```

Check the code:

```bash
uv run ruff check .
```

Automatically fix supported linting issues:

```bash
uv run ruff check --fix .
```

---

## 🔐 Security

Database credentials are not stored directly in the Python source code.

Truck-Partner loads PostgreSQL configuration from environment variables using `python-dotenv`.

SQL operations use parameterized Psycopg queries:

```python
cur.execute(
    """
    DELETE FROM drivers
    WHERE id = %s;
    """,
    (driver_id,),
)
```

This avoids constructing SQL statements directly from user input.

---

## 🗺️ Roadmap

Truck-Partner is being developed incrementally.

### v0.1 — Database & CLI

* [x] PostgreSQL database
* [x] Python ↔ PostgreSQL connection
* [x] Environment configuration
* [x] Driver CRUD
* [x] Truck CRUD
* [x] Cargo CRUD
* [x] Trip creation
* [x] Cargo assignment
* [x] Trip details
* [x] Truck capacity checking
* [x] CLI navigation

### Future Development

Planned areas of expansion include:

* [ ] REST API
* [ ] ORM/database abstraction
* [ ] Authentication and authorization
* [ ] Automated testing
* [ ] Docker containerization
* [ ] CI/CD
* [ ] Expanded logistics data and business rules
* [ ] Stops and rest tracking
* [ ] Fuel records
* [ ] Vehicle maintenance
* [ ] Delivery tracking
* [ ] Deployment

The long-term goal is to evolve Truck-Partner from a CLI database application into a more complete logistics backend system.

---

## 🎯 Project Goals

Truck-Partner is both a functional logistics project and a learning platform for progressively applying backend engineering concepts.

The project focuses on:

* Relational database modeling
* SQL and PostgreSQL
* Python application development
* Database constraints and relationships
* CRUD operations
* Many-to-many relationships
* Separation of application responsibilities
* Secure database configuration
* Version control
* Progressive backend architecture

---

## 📄 Version

**Truck-Partner v0.1.0**

Current stage: **Python CLI + PostgreSQL**

---

## 👨‍💻 Author

Developed by **Caio Moreno**.

This project is under active development as part of an ongoing software engineering and backend development learning journey.
