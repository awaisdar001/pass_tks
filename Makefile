PROJECT_SETTINGS=pass_tks.settings
.PHONY: requirements

requirements: ## install local environment requirements
	pip install -qr requirements.txt --exists-action w

update_db: ## install local environment requirements
	python manage.py migrate --settings=$(PROJECT_SETTINGS)

create_su: ## install local environment requirements
	python manage.py createsuperuser --email admin@example.com --username admin --settings=$(PROJECT_SETTINGS)

dev.up: update_db ## install local environment requirements
	python manage.py runserver localhost:9000 --settings=$(PROJECT_SETTINGS)

shell: ## install local environment requirements
	python manage.py shell --settings=$(PROJECT_SETTINGS)

