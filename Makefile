.PHONY: help setup dev down clean migrate test wordpress-start wordpress-setup wordpress-logs

help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Pyralys - Makefile Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make setup              - Initial project setup"
	@echo "  make dev                - Start all services"
	@echo "  make wordpress-start    - Start with WordPress"
	@echo "  make wordpress-setup    - Configure WordPress"
	@echo ""
	@echo "🔧 Management:"
	@echo "  make down               - Stop all containers"
	@echo "  make clean              - Clean containers and volumes"
	@echo "  make migrate            - Run database migrations"
	@echo "  make urls               - Show all URLs"
	@echo ""
	@echo "🐛 Debugging:"
	@echo "  make logs               - View all logs"
	@echo "  make wordpress-logs     - WordPress logs only"
	@echo "  make api-logs           - API logs only"
	@echo "  make test               - Run tests"
	@echo ""
	@echo "🔌 WordPress:"
	@echo "  make wp-shell           - WordPress shell"
	@echo "  make wp-plugin-status   - Check plugin status"
	@echo "  make wp-backup          - Backup WordPress DB"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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

# WordPress Commands
wordpress-start:
	@echo "🚀 Démarrage de Pyralys + WordPress..."
	@./start-wordpress-dev.sh

wordpress-setup:
	@echo "🔧 Configuration de WordPress..."
	@./setup-wordpress.sh

wordpress-logs:
	@docker-compose logs -f wordpress

api-logs:
	@docker-compose logs -f backend

wp-shell:
	@docker exec -it pyralys-wordpress bash

wp-plugin-status:
	@docker exec pyralys-wordpress wp plugin list --allow-root

wp-plugin-activate:
	@docker exec pyralys-wordpress wp plugin activate pyralys --allow-root

wp-plugin-deactivate:
	@docker exec pyralys-wordpress wp plugin deactivate pyralys --allow-root

wp-debug-log:
	@docker exec pyralys-wordpress tail -f /var/www/html/wp-content/debug.log

wp-backup:
	@mkdir -p backups
	@docker exec pyralys-wordpress-mysql mysqldump -u wordpress -pwordpress123 wordpress > backups/wordpress-$(shell date +%Y%m%d-%H%M%S).sql
	@echo "✅ Backup créé dans backups/"

urls:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📍 URLs d'accès :"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  WordPress       : http://localhost:8080"
	@echo "  WP Admin        : http://localhost:8080/wp-admin"
	@echo "  API Pyralys     : http://localhost:8000"
	@echo "  API Docs        : http://localhost:8000/docs"
	@echo "  Frontend        : http://localhost:3000"
	@echo "  phpMyAdmin      : http://localhost:8081"
	@echo "  Flower (Celery) : http://localhost:5555"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
