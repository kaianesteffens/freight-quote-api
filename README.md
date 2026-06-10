# freight-quote-api

## Live Demo

A running instance with interactive Swagger UI is available at:
https://freight-quote-api.onrender.com/docs

A fictional freight quotation REST API built as a portfolio demo. It does **not**
integrate with any real carrier — quotes are calculated with a simple, deterministic
formula. The goal is to showcase a clean, production-style FastAPI codebase: layered
architecture, JWT authentication, SQLAlchemy 2.x models, Alembic migrations, Docker,
and a Pytest suite.

## Features

- **Auth** — user registration and login, returning a JWT access token.
- **Quotes** — submit origin, destination, weight and volume to get a list of
  fictional carrier quotes with price and delivery time computed by a simple formula.
- **History** — authenticated users can list their previous quotes.
- **Addresses** — full CRUD for addresses saved per user.

## Stack

- Python 3.12 + FastAPI
- PostgreSQL + SQLAlchemy 2.x + Alembic
- JWT authentication (PyJWT) + bcrypt password hashing
- Docker + docker-compose
- Pytest (runs against SQLite, no external services required)

## Project structure

```
app/
  routers/      HTTP layer — one module per domain (auth, quotes, addresses)
  models/       SQLAlchemy ORM models
  schemas/      Pydantic request/response schemas
  services/     business logic, decoupled from the routers
  config.py     environment-driven settings
  database.py   engine / session / declarative base
  security.py   password hashing and JWT helpers
  dependencies.py  shared FastAPI dependencies (current user)
  main.py       application entrypoint
migrations/     Alembic environment and versions
tests/          Pytest suite covering the main endpoints
```

## Configuration

All configuration is provided through environment variables — nothing is hardcoded.
Copy the example file and adjust the values:

```bash
cp .env.example .env
```

| Variable                  | Description                                  |
| ------------------------- | -------------------------------------------- |
| `APP_NAME`                | Application title shown in the OpenAPI docs  |
| `DATABASE_URL`            | SQLAlchemy database URL                       |
| `JWT_SECRET`              | Secret used to sign JWT tokens                |
| `JWT_ALGORITHM`           | JWT signing algorithm (default `HS256`)       |
| `JWT_EXPIRE_MINUTES`      | Token lifetime in minutes                     |
| `FREIGHT_BASE_PRICE`      | Base price applied to every quote             |
| `FREIGHT_PRICE_PER_KG`    | Price added per kilogram                       |
| `FREIGHT_PRICE_PER_M3`    | Price added per cubic meter                    |
| `FREIGHT_DISTANCE_FACTOR` | Weight of the derived distance in the price   |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | Postgres container credentials |

## Running with Docker

The fastest way to run the full stack (API + PostgreSQL):

```bash
cp .env.example .env
docker compose up --build
```

The `app` container runs `alembic upgrade head` before starting the server.
Once it is up:

- API: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs

## Running locally (without Docker)

You need a running PostgreSQL instance and a `DATABASE_URL` pointing to it.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit DATABASE_URL / JWT_SECRET

alembic upgrade head             # apply migrations
uvicorn app.main:app --reload
```

## Running the tests

The test suite uses an in-memory SQLite database, so no PostgreSQL or Docker is
required:

```bash
pip install -r requirements.txt
pytest
```

## Example usage

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","full_name":"Demo","password":"supersecret"}'

# Login -> grab the access_token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"supersecret"}'

# Request a quote
curl -X POST http://localhost:8000/quotes \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"origin":"Sao Paulo","destination":"Rio de Janeiro","weight_kg":10,"volume_m3":0.5}'
```

## How quotes are calculated

Pricing is intentionally simple and deterministic. A pseudo-distance is derived from
the origin/destination strings, then each fictional carrier (Express, Standard,
Economy) applies its own weight and volume multipliers on top of the configurable
base price:

```
price = (base + price_per_kg * weight * carrier_weight_factor
              + price_per_m3 * volume * carrier_volume_factor) * distance_multiplier
```

This is a demo formula — it is not meant to reflect real freight pricing.
