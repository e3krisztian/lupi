.PHONY: default build clean test test-env initdb shell/*

default: test

test: test-env
	(cd game_server; poetry run pytest)

test-env:
	(cd game_server; poetry install)
	(cd ui; poetry install)

clean:
	git clean -fdX # remove only ignored files, directories

build: clean game_server/requirements.txt ui/requirements.txt
	docker-compose build

game_server/requirements.txt: game_server/pyproject.toml
	(cd game_server; poetry export -f requirements.txt -o requirements.txt)

ui/requirements.txt: ui/pyproject.toml
	(cd ui; poetry export -f requirements.txt -o requirements.txt)

initdb:
	docker-compose run --rm game_server bash -c '/wait && python -m game_server.create_db'

shell/db:
	# sql console for an interactive look around
	docker-compose exec db psql -d lupi -U lupi

shell/ui:
	docker-compose exec --user $$(id -u):$$(id -g) ui bash

shell/game_server:
	docker-compose exec --user $$(id -u):$$(id -g) game_server bash
