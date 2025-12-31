.PHONY: help setup dev down clean migrate test

help:
	@echo "Pyralys - Makefile Commands"
	@echo ""
	@echo "  make setup      - Initial project setup"
	@echo "  make dev        - Start development environment"
	@echo "  make down       - Stop all containers"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make migrate    - Run database migrations"
	@echo "  make test       - Run tests"
	@echo "  make logs       - View logs"
	@echo ""

setup:
	@echo "Setting up Pyralys development environment..."
	@cp backend/.env.example backend/.env || true
	@cp frontend/.env.example frontend/.env.local || true
	@echo "✓ Environment files created"
	@echo "⚠️  Please update .env files with your API keys"

dev:
	@echo "Starting Pyralys development environment..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "  Backend API: http://localhost:8000"
	@echo "  Frontend:    http://localhost:3000"
	@echo "  API Docs:    http://localhost:8000/api/docs"
	@echo "  Flower:      http://localhost:5555"

down:
	@echo "Stopping all services..."
	docker-compose down

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	@echo "✓ All containers and volumes removed"

migrate:
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head
	@echo "✓ Migrations completed"

test:
	@echo "Running backend tests..."
	docker-compose exec backend pytest
	@echo "Running frontend tests..."
	docker-compose exec frontend npm test

logs:
	docker-compose logs -f

backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

db-shell:
	docker-compose exec postgres psql -U pyralys -d pyralys_dev
