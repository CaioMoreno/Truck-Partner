# 🚛 Truck-Partner

**Truck-Partner** is a logistics management system built with **Python, PostgreSQL, FastAPI, and SQLAlchemy** for managing drivers, trucks, cargoes, and trips.

The project started as a command-line application and is evolving into a full REST API backend, combining relational database design, an ORM data layer, and HTTP endpoints, while keeping the original CLI as a record of the project's evolution.

## 📌 About the Project

Truck-Partner was created as a practical project for developing and applying skills in **Python, SQL, PostgreSQL, relational database design, Git, backend development, REST APIs, and ORM-based architecture**.

Instead of treating drivers, trucks, cargoes, and trips as isolated data, the system connects them through relational database structures and exposes them both through a CLI and, increasingly, through a FastAPI REST API.

The project now has two parallel entry points:

* **`cli/`** — the original command-line application (kept as-is, as a record of the project's earlier stage)
* **`api/`** — the FastAPI + SQLAlchemy REST API, which is the actively evolving part of the project

The current API allows clients to:

* Create and list drivers
* Create and list trucks
* Create and list cargoes
* Create and list trips, with driver, truck, and cargo details
* Assign cargoes to trips

The project is designed to evolve incrementally as new backend technologies and concepts are introduced.


## ✨ Features

### 🌐 REST API (FastAPI + SQLAlchemy)

* Create and list drivers, trucks, and cargoes
* Create and list trips with nested driver, truck, and cargo details
* Assign cargoes to a trip, preventing duplicate assignments
* Input validation with Pydantic (e.g., positive weight/capacity, fixed-length CPF and plate)
* Existence checks for related resources (e.g., a trip cannot be created with a non-existent driver or truck)
* Auto-generated interactive documentation via Swagger UI (`/docs`)

### 💻 CLI (original entry point)

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


## 🛠️ Technologies

| Technology    | Purpose                                    |
| ------------- | ------------------------------------------- |
| Python        | Application, API, and CLI logic            |
| FastAPI       | REST API framework                         |
| SQLAlchemy    | ORM and database models                    |
| Pydantic      | Request/response validation                |
| Uvicorn       | ASGI server for running the API            |
| PostgreSQL    | Relational database                        |
| Psycopg       | Python ↔ PostgreSQL communication (CLI)    |
| python-dotenv | Environment variable management            |
| uv            | Python project and dependency management  |
| Ruff          | Python linting and formatting              |
| Git           | Version control                            |
| GitHub        | Source code hosting                        |


## 📂 Project Structure

```text
Truck-Partner/
│
├── api/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── cli/
│   ├── __init__.py
│   ├── cargoes.py
│   ├── db.py
│   ├── drivers.py
│   ├── main.py
│   ├── trips.py
│   ├── truck_system.py
│   └── trucks.py
│
├── database/
│   ├── queries.sql
│   └── schema.sql
│
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

### Main components

**`api/main.py`**
FastAPI application entry point. Defines all REST endpoints and creates the database tables on startup.

**`api/models.py`**
SQLAlchemy ORM models (`Driver`, `Truck`, `Cargo`, `Trip`) and the `trip_cargo` association table, including relationships and check constraints.

**`api/schemas.py`**
Pydantic schemas used for request validation and response serialization, separated into `Base`, `Create`, and `Response` variants per resource.

**`api/database.py`**
Configures the SQLAlchemy engine and session, and exposes the `get_db()` dependency used by the API routes.

**`cli/main.py`**
Original CLI entry point. Tests the PostgreSQL connection and starts the CLI system.

**`cli/truck_system.py`**
Controls the CLI menus and navigation between the different areas of the application.

**`cli/db.py`**
Creates raw `psycopg` PostgreSQL connections used by the CLI, using credentials stored in environment variables.

**`cli/drivers.py`, `cli/trucks.py`, `cli/cargoes.py`, `cli/trips.py`**
Contain the original CRUD operations for each resource, kept as a record of the project's earlier CLI-only stage.


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


## 🔗 API Endpoints

```text
GET    /                              Welcome message
GET    /status                        API status and version

GET    /drivers                       List all drivers
GET    /drivers/{driver_id}           Get a driver by id
POST   /drivers                       Create a driver

GET    /trucks                        List all trucks
GET    /trucks/{truck_id}             Get a truck by id
POST   /trucks                        Create a truck

GET    /cargoes                       List all cargoes
GET    /cargoes/{cargo_id}            Get a cargo by id
POST   /cargoes                       Create a cargo

GET    /trips                         List all trips (with driver, truck, cargoes)
GET    /trips/{trip_id}               Get a trip by id (with driver, truck, cargoes)
POST   /trips                         Create a trip
POST   /trips/{trip_id}/cargoes/{cargo_id}   Assign a cargo to a trip
```

Interactive documentation (Swagger UI) is available at `/docs` once the API is running.

## ▶️ Running the API

```bash
uv run fastapi dev api/main.py
```

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


## 🔐 Security

Database credentials are not stored directly in the Python source code.

Truck-Partner loads PostgreSQL configuration from environment variables using `python-dotenv`.

In the API, request data is validated with Pydantic before it reaches the database layer (e.g., weight and capacity fields must be positive, CPF and license plate fields have fixed length), and related resources are checked for existence before creating relationships (e.g., a trip cannot reference a non-existent driver or truck).

In the CLI, SQL operations use parameterized Psycopg queries:

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

### v0.2 — REST API (FastAPI)

* [x] FastAPI application setup
* [x] Create and list endpoints for drivers, trucks, cargoes, and trips
* [x] Cargo assignment endpoint
* [x] Pydantic request/response validation

### v0.5 — ORM (SQLAlchemy)

* [x] SQLAlchemy models for all resources
* [x] Many-to-many relationship between trips and cargoes
* [x] Database-level check constraints (positive weight/capacity)
* [x] Dependency-injected database session

### Future Development

Planned areas of expansion include:

* [ ] Complete CRUD (update and delete endpoints) in the API
* [ ] Authentication and authorization (JWT)
* [ ] Automated testing (pytest)
* [ ] Docker containerization
* [ ] CI/CD (GitHub Actions)
* [ ] Expanded logistics data and business rules
* [ ] Stops and rest tracking
* [ ] Fuel records
* [ ] Vehicle maintenance
* [ ] Delivery tracking
* [ ] Deployment

The long-term goal is to evolve Truck-Partner from a CLI database application into a more complete logistics backend system.


## 🎯 Project Goals

Truck-Partner is both a functional logistics project and a learning platform for progressively applying backend engineering concepts.

The project focuses on:

* Relational database modeling
* SQL and PostgreSQL
* Python application development
* Database constraints and relationships
* CRUD operations
* Many-to-many relationships
* REST API design with FastAPI
* ORM modeling with SQLAlchemy
* Request/response validation with Pydantic
* Separation of application responsibilities
* Secure database configuration
* Version control
* Progressive backend architecture


## 📄 Version

**Truck-Partner v0.5.0**

Current stage: **FastAPI REST API + SQLAlchemy ORM + PostgreSQL** (original CLI preserved in `cli/`)


## 👨‍💻 Author

Developed by **Caio Moreno**.

This project is under active development as part of an ongoing software engineering and backend development learning journey.