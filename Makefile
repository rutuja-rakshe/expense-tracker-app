.PHONY: help run migrate migrations shell test lint build up down logs createsuperuser

help:
	@echo "  make run              Start dev server"
	@echo "  make up               Start all Docker services"
	@echo "  make down             Stop all Docker services"
	@echo "  make migrate          Apply migrations"
	@echo "  make migrations       Create migrations"
	@echo "  make shell            Django shell"
	@echo "  make test             Run tests"
	@echo "  make lint             Run linters"
	@echo "  make createsuperuser  Create admin user"

run:
	DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell

test:
	pytest --cov=apps --cov-report=term-missing -v

lint:
	flake8 apps config --max-line-length=120
	isort --check-only apps config
	black --check apps config

format:
	isort apps config
	black apps config

logs:
	docker-compose logs -f web

createsuperuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput