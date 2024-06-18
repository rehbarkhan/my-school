.PHONEY: tailwind
tailwind:
	npx tailwindcss -i ./lib/input.css -o ./lib/output.css --watch

.PHONEY: django
django:
	python manage.py runserver 0.0.0.0:8080

.PHONEY: docker-up
docker-up:
	docker compose -f ./docker-compose.dev.yml up
.PHONEY: worker
worker:
	celery -A project worker -l DEBUG
.PHONEY: migrate
migrate:
	python manage.py makemigrations && python manage.py migrate