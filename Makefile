.PHONY: up down rebuild migrate create_migration downgrade shell psql lint check

# Pull in .env so the credentials live in one place and never reach the repo.
# Leading dash: don't fail on a fresh clone where .env doesn't exist yet.
-include .env
export

TEST_DB_NAME ?= ecommerce_test

up:
	docker compose up

down:
	docker compose down


rebuild:
	docker compose up --build


migrate:
	docker compose up migrations

create_migration:
	docker compose exec app alembic revision --autogenerate -m "$(name)"

downgrade:
	docker compose exec app alembic downgrade -1



shell:
	docker compose exec app sh

psql:
	docker compose exec db psql -U postgres -d ecommerce


lint:
	poetry run ruff check --fix . && poetry run ruff format .

check:
	poetry run ruff check . && poetry run ruff format --check .

seed:
	docker compose exec -T db psql -U postgres -d ecommerce < scripts/seed.sql

fresh:
	docker compose down -v
	docker compose up -d --build
	docker compose exec -T db psql -U postgres -d ecommerce < scripts/seed.sql



test-db:
	@docker compose exec -T db psql -U postgres -tAc \
		"SELECT 1 FROM pg_database WHERE datname='$(TEST_DB_NAME)'" | grep -q 1 \
		|| docker compose exec -T db psql -U postgres -c "CREATE DATABASE $(TEST_DB_NAME)"

test: test-db
	DB_URL=$(TEST_DB_URL) poetry run alembic upgrade head
	DB_URL=$(TEST_DB_URL) poetry run pytest

test-one: test-db
	DB_URL=$(TEST_DB_URL) poetry run pytest -k "$(k)" -vv
