<!--
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
-->

# FastAPI E-Commerce Demo

A small learning project for an e-commerce backend with FastAPI and MySQL. It supports:

- user registration with a default balance
- product inventory CRUD
- product search/filter by name
- purchases that reduce stock and user balance
- info/debug/warning/error logging
- application log file written to `./log/app.log` by default
- Dockerized FastAPI and MySQL containers
- database schema and seed data initialized when the MySQL volume is first created

## Design Choice

This project uses a modular monolith: one FastAPI app split into routers, schemas, models, and services. For learning, this is easier to run and debug than several tiny services on different ports. It still gives you clear future boundaries:

- `users` can become a user service
- `products` can become an inventory/catalog service
- `purchases` can become an order service

In Kubernetes, the current app can start as one Deployment and Service. Later, each router/service layer can move into its own Deployment without changing the API concepts.

## Run With Docker Compose

From the project root:

```bash
cd /Users/shgangop/devops_projects_personal/python_fastapi_project
```

Start the FastAPI app and MySQL database:

```bash
docker compose up --build
```

This builds the FastAPI image, starts MySQL, initializes the schema and seed data, starts the API on port `8091`, and writes application logs to `./log/app.log`.

API docs:

- Swagger UI: http://localhost:8091/docs
- OpenAPI JSON: http://localhost:8091/openapi.json

Health checks:

```bash
curl http://localhost:8091/health
curl http://localhost:8091/health/db
```

Stop the containers:

```bash
docker compose down
```

Stop the containers and delete the MySQL volume so the schema and seed scripts run again on the next startup:

```bash
docker compose down -v
```

## Logging

The app logs to both the console and a rotating file. By default, local runs write to:

```text
./log/app.log
```

The log location is configurable with environment variables:

```text
LOG_LEVEL=DEBUG
LOG_DIR=./log
LOG_FILE_NAME=app.log
```

In `docker-compose.yml`, the app writes logs inside the container to:

```text
/var/log/ecommerce/app.log
```

That directory is bind-mounted to the host:

```yaml
volumes:
  - ./log:/var/log/ecommerce
```

So the same log file is available on the host at:

```text
./log/app.log
```

You can also inspect the API container logs with:

```bash
docker compose logs api
```

## Example API Calls

Create a user:

```bash
curl -X POST http://localhost:8091/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}'
```

Create a product:

```bash
curl -X POST http://localhost:8091/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Noise Cancelling Headphones","description":"Wireless headphones","price":299.99,"stock_quantity":15}'
```

Search products by name:

```bash
curl "http://localhost:8091/products?name=keyboard"
```

List all products:

```bash
curl http://localhost:8091/products
```

Purchase a product:

```bash
curl -X POST http://localhost:8091/purchases \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"product_id":1,"quantity":2}'
```

List purchases for a user:

```bash
curl "http://localhost:8091/purchases?user_id=1"
```

## Tests

The test suite uses FastAPI's `TestClient` and an in-memory SQLite database. This keeps tests fast and means you do not need a running MySQL container for normal CI validation.

Install test dependencies and run tests:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Jenkins CI

The included `Jenkinsfile` defines a multi-stage CI pipeline:

- checkout repository
- create a Python virtual environment
- install application and test dependencies
- run pytest
- build the Docker image
- push both a build-specific tag and `latest` to a Docker registry

The pipeline assumes Jenkins already has username/password credentials named:

```text
docker-registry-credentials
```

Update `REGISTRY_URL`, `REGISTRY_NAMESPACE`, and `IMAGE_NAME` in the `Jenkinsfile` for your registry.

## Database Initialization

Yes, a database container can be set up with tables and seed data beforehand. The MySQL image runs SQL files mounted into `/docker-entrypoint-initdb.d` only when the data directory is empty.

This project uses:

- `db/init/001_schema.sql` for tables and indexes
- `db/init/002_seed_data.sql` for starter products

If you change these scripts after the database volume already exists, recreate the volume:

```bash
docker compose down -v
docker compose up --build
```

For production, prefer schema migration tooling such as Alembic instead of relying only on init scripts.

## Project Structure

```text
app/
  api/          FastAPI routers
  core/         settings and logging
  db/           database engine/session/base
  models/       SQLAlchemy tables
  schemas/      Pydantic request/response models
  services/     business logic
db/init/        MySQL first-run initialization scripts
Dockerfile      multi-stage API image
docker-compose.yml
```

## Future Production Improvements

- Add Alembic migrations.
- Add authentication and password hashing.
- Add request IDs and structured JSON logs.
- Add tests using pytest and a disposable test database.
- Add optimistic locking or row-level locks for high-concurrency purchases.
- Add Kubernetes manifests or Helm charts.
- Split services only when independent scaling, ownership, or deployment cadence justifies it.
