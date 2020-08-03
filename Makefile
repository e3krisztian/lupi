.phony: build clean test test-env default

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
