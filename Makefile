.PHONY: default build clean test test-env initdb shell/*

default: test

test: test-env
	(cd lupi_game_server; poetry run pytest)

clean:
	git clean -fdX # remove only ignored files, directories

build: clean lupi_game_client lupi_game_server/requirements.txt lupi_ui/requirements.txt
	docker-compose build

initdb:
	docker-compose run --rm game_server bash -c './wait-for-postgres db && python -m lupi_game_server.create_db'

shell/db:
	# sql console for an interactive look around
	docker-compose exec db psql -d lupi -U lupi

shell/ui:
	docker-compose exec --user $$(id -u):$$(id -g) ui bash

shell/game_server:
	docker-compose exec --user $$(id -u):$$(id -g) game_server bash


# ugly details - requires poetry & docker

test-env: lupi_ui/requirements.txt
	(cd lupi_game_server; poetry install)
	(cd lupi_ui; poetry install)

lupi_game_server/requirements.txt: lupi_game_server/pyproject.toml
	(cd lupi_game_server; poetry export -f requirements.txt -o requirements.txt)

lupi_game_client: lupi_game_server/openapi.yaml
	rm -rf lupi_game_client
	docker run --rm --user $$(id -u):$$(id -g) -v $$PWD:/local openapitools/openapi-generator-cli generate -g python --package-name=lupi_game_client -i /local/lupi_game_server/openapi.yaml -o /local/lupi_game_client

lupi_ui/requirements.txt: lupi_ui/pyproject.toml lupi_game_client
	(cd lupi_ui; poetry export -f requirements.txt -o requirements.txt --without-hashes)
	# --without-hashes is sadly required because of having lupi_game_client installed as local package (=editable)
	# (see https://github.com/pypa/pip/issues/4995)
