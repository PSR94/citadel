SHELL := /bin/zsh

.PHONY: bootstrap api-install web-install dev up down seed api-test web-build eval lint

bootstrap:
	./scripts/bootstrap/bootstrap.sh

api-install:
	cd apps/api && python3 -m pip install -e ".[dev,models]"

web-install:
	npm install

dev:
	docker compose up --build

up:
	docker compose up -d --build

down:
	docker compose down -v

seed:
	cd apps/api && python3 -m app.scripts.seed_corpus

api-test:
	cd apps/api && pytest

web-build:
	npm run build:web

eval:
	cd apps/api && python3 -m app.scripts.run_eval --profile ci

lint:
	cd apps/api && ruff check app tests
	npm run lint:web

