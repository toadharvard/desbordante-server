.PHONY: env install-deps compose-up run-worker run-app init run all

## Create .env file from .env.example
env:
	@cp .env.example .env
	@echo >> .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

## Install dependencies
install-deps:
	poetry install
	poetry run pre-commit install

## Up development-only docker containers
compose-up:
	(trap 'docker compose -f dev-docker-compose.yaml down' INT; \
	docker compose -f dev-docker-compose.yaml up --build --force-recreate --remove-orphans)

## Run celery worker in watch mode
run-worker:
	. .venv/bin/activate && watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A app.worker worker --loglevel=info --concurrency=1

## Run application server in watch mode
run-app:
	poetry run uvicorn --port 8000 app.main:app --reload

## Initiate repository
init:
	make env install-deps

## Run full application in watch mode
run:
	make compose-up run-worker run-app

## Run make init run
all:
	make init run

lint:
	poetry run ruff ./tests ./app
	poetry run ruff format --check ./tests ./app
	poetry run black --check ./tests ./app
	poetry run mypy --ignore-missing-imports ./app

.DEFAULT_GOAL := help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
help:
	@echo "$$(tput setaf 2)Available rules:$$(tput sgr0)";sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## /---/;td" -e"s/:.*//;G;s/\\n## /===/;s/\\n//g;p;}" ${MAKEFILE_LIST}|awk -F === -v n=$$(tput cols) -v i=4 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"- %s%s%s\n",a,$$1,z;m=split($$2,w,"---");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;}printf"%*s%s\n",-i," ",w[j];}}'
