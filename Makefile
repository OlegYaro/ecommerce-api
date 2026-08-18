.PHONY: up down rebuild migrate create_migration downgrade shell psql lint check


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
