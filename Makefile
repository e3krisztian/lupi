.PHONY: default build clean test test-env initdb shell/*

default: test

test: test-env
	(cd game_server; poetry run pytest)

clean:
	git clean -fdX # remove only ignored files, directories

build: clean game_client game_server/requirements.txt ui/requirements.txt
	docker-compose build

initdb:
	docker-compose run --rm game_server bash -c '/wait && python -m game_server.create_db'

shell/db:
	# sql console for an interactive look around
	docker-compose exec db psql -d lupi -U lupi

shell/ui:
	docker-compose exec --user $$(id -u):$$(id -g) ui bash

shell/game_server:
	docker-compose exec --user $$(id -u):$$(id -g) game_server bash


# ugly details - requires poetry & docker

test-env: ui/requirements.txt
	(cd game_server; poetry install)
	(cd ui; poetry install)

game_server/requirements.txt: game_server/pyproject.toml
	(cd game_server; poetry export -f requirements.txt -o requirements.txt)

game_client: game_server/openapi.yaml
	rm -rf game_client
	docker run --rm --user $$(id -u):$$(id -g) -v $$PWD:/local openapitools/openapi-generator-cli generate -g python --package-name=game_client -i /local/game_server/openapi.yaml -o /local/game_client

ui/requirements.txt: ui/pyproject.toml game_client
	# generate the game-client package
	(cd game_client; python setup.py build sdist --formats=zip)
	mv game_client/dist/game-client*.zip ui
	# update lock/hash - while it is not in the output
	(cd ui; poetry add ./game-client*.zip)
	(cd ui; poetry export -f requirements.txt -o requirements.txt)
